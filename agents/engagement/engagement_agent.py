"""
Agente de Engajamento (Social Dev)
Responsável por fazer o perfil parecer ativo e conectado com a comunidade
"""

import os
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple


class EngagementAgent:
    """Agente responsável pelo engajamento e atividade social no GitHub"""

    def __init__(self, username: str, github_token: Optional[str] = None):
        self.username = username
        self.github_token = github_token or os.getenv('GITHUB_TOKEN')
        self.api_base = 'https://api.github.com'
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
        }
        if self.github_token:
            self.headers['Authorization'] = f'token {self.github_token}'

    def get_user_events(self, days: int = 30) -> List[Dict]:
        """Obtém eventos recentes do usuário"""
        url = f'{self.api_base}/users/{self.username}/events'
        params = {'per_page': 100}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()

        events = response.json()

        # Filtra eventos dos últimos N dias
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_events = []

        for event in events:
            event_date = datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ')
            if event_date >= cutoff_date:
                recent_events.append(event)

        return recent_events

    def analyze_activity(self, days: int = 30) -> Dict:
        """Analisa atividade recente do usuário"""
        events = self.get_user_events(days)

        activity = {
            'total_events': len(events),
            'commits': 0,
            'pull_requests': 0,
            'issues_opened': 0,
            'issues_commented': 0,
            'repos_created': 0,
            'repos_starred': 0,
            'repos_forked': 0,
            'active_days': set(),
            'most_active_repo': None,
            'event_types': {}
        }

        repo_activity = {}

        for event in events:
            event_type = event['type']
            activity['event_types'][event_type] = activity['event_types'].get(event_type, 0) + 1

            # Data de atividade
            event_date = datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ').date()
            activity['active_days'].add(event_date)

            # Conta atividades por tipo
            if event_type == 'PushEvent':
                activity['commits'] += len(event.get('payload', {}).get('commits', []))
            elif event_type == 'PullRequestEvent':
                activity['pull_requests'] += 1
            elif event_type == 'IssuesEvent':
                if event.get('payload', {}).get('action') == 'opened':
                    activity['issues_opened'] += 1
            elif event_type == 'IssueCommentEvent':
                activity['issues_commented'] += 1
            elif event_type == 'CreateEvent':
                if event.get('payload', {}).get('ref_type') == 'repository':
                    activity['repos_created'] += 1
            elif event_type == 'WatchEvent':
                activity['repos_starred'] += 1
            elif event_type == 'ForkEvent':
                activity['repos_forked'] += 1

            # Conta atividade por repositório
            repo_name = event.get('repo', {}).get('name')
            if repo_name:
                repo_activity[repo_name] = repo_activity.get(repo_name, 0) + 1

        # Repositório mais ativo
        if repo_activity:
            activity['most_active_repo'] = max(repo_activity.items(), key=lambda x: x[1])

        activity['active_days_count'] = len(activity['active_days'])
        activity['active_days'] = sorted(list(activity['active_days']), reverse=True)

        return activity

    def get_trending_repos(self, language: Optional[str] = None, since: str = 'daily') -> List[Dict]:
        """
        Obtém repositórios em alta
        Nota: GitHub não tem API oficial para trending. Esta é uma implementação alternativa.
        """
        # Busca por repositórios criados recentemente com muitas estrelas
        date_filter = datetime.now() - timedelta(days=7)
        date_str = date_filter.strftime('%Y-%m-%d')

        query = f'created:>{date_str}'
        if language:
            query += f' language:{language}'

        url = f'{self.api_base}/search/repositories'
        params = {
            'q': query,
            'sort': 'stars',
            'order': 'desc',
            'per_page': 10
        }

        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()

        return response.json().get('items', [])

    def suggest_repos_to_star(self, interests: List[str], limit: int = 10) -> List[Dict]:
        """Sugere repositórios para dar estrela baseado em interesses"""
        suggestions = []

        for interest in interests[:3]:  # Limita a 3 interesses para não exceder rate limit
            url = f'{self.api_base}/search/repositories'
            params = {
                'q': interest,
                'sort': 'stars',
                'order': 'desc',
                'per_page': limit
            }

            try:
                response = requests.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                repos = response.json().get('items', [])
                suggestions.extend(repos[:3])  # Top 3 de cada interesse
            except:
                continue

        # Remove duplicatas
        unique_suggestions = []
        seen_ids = set()
        for repo in suggestions:
            if repo['id'] not in seen_ids:
                unique_suggestions.append(repo)
                seen_ids.add(repo['id'])

        return unique_suggestions[:limit]

    def suggest_repos_to_contribute(self, languages: List[str]) -> List[Dict]:
        """Sugere repositórios para contribuir baseado em linguagens de interesse"""
        suggestions = []

        for language in languages[:2]:
            # Busca por repos com label "good first issue"
            url = f'{self.api_base}/search/issues'
            params = {
                'q': f'language:{language} label:"good first issue" state:open',
                'sort': 'created',
                'order': 'desc',
                'per_page': 5
            }

            try:
                response = requests.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                issues = response.json().get('items', [])

                for issue in issues:
                    repo_url = issue['repository_url']
                    repo_response = requests.get(repo_url, headers=self.headers)
                    if repo_response.status_code == 200:
                        suggestions.append({
                            'repo': repo_response.json(),
                            'issue': issue
                        })
            except:
                continue

        return suggestions

    def generate_achievement_post(self, activity: Dict, period_days: int = 30) -> str:
        """Gera post sobre conquistas recentes"""
        post = [
            f"# 🎉 Conquistas dos Últimos {period_days} Dias",
            "",
            f"📅 Período: {datetime.now().strftime('%d/%m/%Y')}",
            "",
            "## 📊 Estatísticas",
            ""
        ]

        if activity['commits'] > 0:
            post.append(f"- 💻 **{activity['commits']}** commits realizados")

        if activity['pull_requests'] > 0:
            post.append(f"- 🔀 **{activity['pull_requests']}** pull requests")

        if activity['issues_opened'] > 0:
            post.append(f"- 🐛 **{activity['issues_opened']}** issues abertas")

        if activity['repos_created'] > 0:
            post.append(f"- 🆕 **{activity['repos_created']}** novos repositórios criados")

        if activity['repos_starred'] > 0:
            post.append(f"- ⭐ **{activity['repos_starred']}** repositórios favoritados")

        post.extend([
            f"- 📆 **{activity['active_days_count']}** dias ativos",
            ""
        ])

        if activity['most_active_repo']:
            repo_name, count = activity['most_active_repo']
            post.extend([
                "## 🔥 Repositório Mais Ativo",
                "",
                f"[{repo_name}](https://github.com/{repo_name}) - {count} atividades",
                ""
            ])

        # Motivação
        if activity['active_days_count'] >= 20:
            post.append("🏆 Excelente consistência! Continue assim!")
        elif activity['active_days_count'] >= 10:
            post.append("👏 Boa atividade! Mantenha o ritmo!")
        else:
            post.append("💪 Vamos aumentar a consistência!")

        post.extend([
            "",
            "---",
            "",
            f"🤖 Gerado automaticamente em {datetime.now().strftime('%d/%m/%Y às %H:%M')}"
        ])

        return "\n".join(post)

    def generate_weekly_summary(self) -> str:
        """Gera resumo semanal de atividades"""
        activity = self.analyze_activity(days=7)

        summary = [
            "# 📈 Resumo Semanal",
            "",
            f"Semana de {(datetime.now() - timedelta(days=7)).strftime('%d/%m/%Y')} até {datetime.now().strftime('%d/%m/%Y')}",
            "",
            "## Atividades",
            ""
        ]

        total_activity = activity['commits'] + activity['pull_requests'] + activity['issues_opened']

        if total_activity == 0:
            summary.extend([
                "⚠️ Nenhuma atividade registrada esta semana.",
                "",
                "💡 **Dica**: Que tal começar um novo projeto ou contribuir para a comunidade?",
                ""
            ])
        else:
            summary.extend([
                f"- Commits: **{activity['commits']}**",
                f"- Pull Requests: **{activity['pull_requests']}**",
                f"- Issues: **{activity['issues_opened']}**",
                f"- Dias ativos: **{activity['active_days_count']}/7**",
                ""
            ])

            # Insights
            summary.append("## 💡 Insights")
            summary.append("")

            if activity['active_days_count'] == 7:
                summary.append("🔥 **Streak perfeito!** Você foi ativo todos os dias da semana!")
            elif activity['active_days_count'] >= 5:
                summary.append("⭐ Ótima consistência esta semana!")
            elif activity['active_days_count'] >= 3:
                summary.append("👍 Boa atividade! Tente aumentar a consistência.")
            else:
                summary.append("💪 Vamos aumentar a frequência de commits!")

            summary.append("")

        return "\n".join(summary)

    def generate_linkedin_post(self, activity: Dict) -> str:
        """Gera sugestão de post para LinkedIn sobre atividades"""
        post = f"""
🚀 Atualizações de Desenvolvimento - {datetime.now().strftime('%B %Y')}

Nos últimos 30 dias, tenho focado em:

💻 {activity['commits']} commits em projetos ativos
🔀 {activity['pull_requests']} pull requests
🐛 {activity['issues_opened']} issues resolvidas
⭐ {activity['repos_starred']} novos repositórios descobertos

{f"📌 Projeto em destaque: {activity['most_active_repo'][0]}" if activity['most_active_repo'] else ""}

Sempre buscando aprender e contribuir com a comunidade de desenvolvedores! 💙

#Developer #GitHub #Programming #TechCommunity #CodingLife
        """.strip()

        return post

    def create_engagement_report(self, output_file: str = 'ENGAGEMENT_REPORT.md'):
        """Cria relatório completo de engajamento"""
        activity_30d = self.analyze_activity(days=30)
        activity_7d = self.analyze_activity(days=7)

        report = [
            "# 📊 Relatório de Engajamento",
            "",
            f"Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}",
            "",
            "## 📅 Últimos 30 Dias",
            "",
            f"- **Total de eventos**: {activity_30d['total_events']}",
            f"- **Commits**: {activity_30d['commits']}",
            f"- **Pull Requests**: {activity_30d['pull_requests']}",
            f"- **Issues abertas**: {activity_30d['issues_opened']}",
            f"- **Comentários em issues**: {activity_30d['issues_commented']}",
            f"- **Repositórios criados**: {activity_30d['repos_created']}",
            f"- **Dias ativos**: {activity_30d['active_days_count']}/30",
            ""
        ]

        # Atividade semanal
        report.extend([
            "## 📅 Última Semana",
            "",
            f"- **Commits**: {activity_7d['commits']}",
            f"- **Pull Requests**: {activity_7d['pull_requests']}",
            f"- **Dias ativos**: {activity_7d['active_days_count']}/7",
            ""
        ])

        # Posts sugeridos
        report.extend([
            "## 💬 Posts Sugeridos",
            "",
            "### LinkedIn",
            "",
            self.generate_linkedin_post(activity_30d),
            "",
            "### GitHub Profile",
            "",
            self.generate_achievement_post(activity_30d),
            ""
        ])

        # Recomendações
        report.extend([
            "## 🎯 Recomendações",
            ""
        ])

        avg_commits_per_day = activity_30d['commits'] / 30
        if avg_commits_per_day < 1:
            report.append("- 📈 Tente aumentar a frequência de commits para pelo menos 1 por dia")

        if activity_30d['pull_requests'] == 0:
            report.append("- 🔀 Considere contribuir com pull requests em projetos da comunidade")

        if activity_30d['issues_commented'] < 5:
            report.append("- 💬 Participe mais das discussões comentando em issues")

        if activity_30d['repos_starred'] < 10:
            report.append("- ⭐ Explore e favorite mais repositórios interessantes")

        # Salva relatório
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(report))

        print(f"✅ Relatório de engajamento salvo em {output_file}")


def main():
    """Função principal para testes"""
    agent = EngagementAgent('krisalexandre2018')

    print("Analisando atividade...")
    activity = agent.analyze_activity(days=30)

    print(f"\n📊 Estatísticas dos últimos 30 dias:")
    print(f"- Commits: {activity['commits']}")
    print(f"- Pull Requests: {activity['pull_requests']}")
    print(f"- Dias ativos: {activity['active_days_count']}")

    print("\nGerando relatório completo...")
    agent.create_engagement_report()


if __name__ == '__main__':
    main()
