"""
Agente de Insights (Analytics & Feedback)
Responsável por monitorar desempenho e gerar relatórios analíticos
"""

import os
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict, Counter


class InsightsAgent:
    """Agente responsável por analytics e insights do perfil"""

    def __init__(self, username: str, github_token: Optional[str] = None):
        self.username = username
        self.github_token = github_token or os.getenv('GITHUB_TOKEN')
        self.api_base = 'https://api.github.com'
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
        }
        if self.github_token:
            self.headers['Authorization'] = f'token {self.github_token}'

    def get_user_data(self) -> Dict:
        """Obtém dados do usuário"""
        url = f'{self.api_base}/users/{self.username}'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_all_repos(self) -> List[Dict]:
        """Obtém todos os repositórios"""
        url = f'{self.api_base}/users/{self.username}/repos'
        params = {'per_page': 100}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def calculate_total_metrics(self) -> Dict:
        """Calcula métricas totais do perfil"""
        repos = self.get_all_repos()

        metrics = {
            'total_repos': 0,
            'total_stars': 0,
            'total_forks': 0,
            'total_watchers': 0,
            'total_open_issues': 0,
            'languages': Counter(),
            'topics': Counter(),
            'repos_with_stars': 0,
            'repos_with_forks': 0,
            'most_starred_repo': None,
            'most_forked_repo': None,
            'newest_repo': None,
            'oldest_repo': None,
            'avg_stars_per_repo': 0,
            'total_size': 0  # em KB
        }

        for repo in repos:
            if repo.get('private', False):
                continue

            metrics['total_repos'] += 1
            stars = repo.get('stargazers_count', 0)
            forks = repo.get('forks_count', 0)

            metrics['total_stars'] += stars
            metrics['total_forks'] += forks
            metrics['total_watchers'] += repo.get('watchers_count', 0)
            metrics['total_open_issues'] += repo.get('open_issues_count', 0)
            metrics['total_size'] += repo.get('size', 0)

            # Linguagens
            if repo.get('language'):
                metrics['languages'][repo['language']] += 1

            # Topics
            for topic in repo.get('topics', []):
                metrics['topics'][topic] += 1

            # Repos com engajamento
            if stars > 0:
                metrics['repos_with_stars'] += 1
            if forks > 0:
                metrics['repos_with_forks'] += 1

            # Repo mais estrelado
            if metrics['most_starred_repo'] is None or stars > metrics['most_starred_repo']['stars']:
                metrics['most_starred_repo'] = {
                    'name': repo['name'],
                    'stars': stars,
                    'url': repo['html_url']
                }

            # Repo mais forkado
            if metrics['most_forked_repo'] is None or forks > metrics['most_forked_repo']['forks']:
                metrics['most_forked_repo'] = {
                    'name': repo['name'],
                    'forks': forks,
                    'url': repo['html_url']
                }

            # Repo mais novo
            created_at = datetime.strptime(repo['created_at'], '%Y-%m-%dT%H:%M:%SZ')
            if metrics['newest_repo'] is None or created_at > metrics['newest_repo']['date']:
                metrics['newest_repo'] = {
                    'name': repo['name'],
                    'date': created_at,
                    'url': repo['html_url']
                }

            # Repo mais antigo
            if metrics['oldest_repo'] is None or created_at < metrics['oldest_repo']['date']:
                metrics['oldest_repo'] = {
                    'name': repo['name'],
                    'date': created_at,
                    'url': repo['html_url']
                }

        # Médias
        if metrics['total_repos'] > 0:
            metrics['avg_stars_per_repo'] = round(metrics['total_stars'] / metrics['total_repos'], 2)

        return metrics

    def track_repo_growth(self, repo_name: str, days: int = 30) -> Dict:
        """
        Rastreia crescimento de um repositório específico
        Nota: GitHub API não fornece histórico direto. Esta implementação é limitada.
        """
        url = f'{self.api_base}/repos/{self.username}/{repo_name}'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        repo = response.json()

        # Dados atuais
        growth = {
            'repo_name': repo_name,
            'current_stars': repo.get('stargazers_count', 0),
            'current_forks': repo.get('forks_count', 0),
            'current_watchers': repo.get('watchers_count', 0),
            'open_issues': repo.get('open_issues_count', 0),
            'created_at': repo['created_at'],
            'updated_at': repo['updated_at'],
            'language': repo.get('language'),
            'size': repo.get('size', 0)
        }

        # Calcula dias desde criação
        created_date = datetime.strptime(repo['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        age_days = (datetime.now() - created_date).days

        growth['age_days'] = age_days
        growth['stars_per_day'] = round(growth['current_stars'] / max(age_days, 1), 2)

        return growth

    def compare_with_community(self, language: Optional[str] = None) -> Dict:
        """Compara métricas com a comunidade"""
        metrics = self.calculate_total_metrics()

        comparison = {
            'your_total_stars': metrics['total_stars'],
            'your_total_repos': metrics['total_repos'],
            'your_avg_stars': metrics['avg_stars_per_repo'],
            'top_language': metrics['languages'].most_common(1)[0] if metrics['languages'] else ('N/A', 0),
            'insights': []
        }

        # Insights baseados em benchmarks gerais
        if metrics['avg_stars_per_repo'] >= 10:
            comparison['insights'].append("🌟 Excelente! Seus repos têm média de estrelas acima da comunidade")
        elif metrics['avg_stars_per_repo'] >= 5:
            comparison['insights'].append("⭐ Boa média de estrelas por repositório")
        else:
            comparison['insights'].append("💡 Dica: Foque na qualidade e divulgação dos projetos para ganhar mais estrelas")

        if metrics['total_repos'] >= 20:
            comparison['insights'].append("📚 Ótimo portfólio com muitos projetos")
        elif metrics['total_repos'] >= 10:
            comparison['insights'].append("📂 Bom número de projetos no portfólio")
        else:
            comparison['insights'].append("🚀 Continue criando mais projetos para expandir seu portfólio")

        # Diversidade de linguagens
        lang_count = len(metrics['languages'])
        if lang_count >= 5:
            comparison['insights'].append("🎨 Excelente diversidade de linguagens")
        elif lang_count >= 3:
            comparison['insights'].append("💻 Boa variedade de tecnologias")
        else:
            comparison['insights'].append("🔧 Considere explorar mais linguagens e tecnologias")

        return comparison

    def generate_weekly_report(self) -> str:
        """Gera relatório semanal"""
        metrics = self.calculate_total_metrics()
        user_data = self.get_user_data()

        report = [
            "# 📊 Relatório Semanal de Insights",
            "",
            f"**Período**: {datetime.now().strftime('%d/%m/%Y')}",
            f"**Perfil**: @{self.username}",
            "",
            "## 📈 Métricas Gerais",
            "",
            f"- 📦 **Repositórios públicos**: {metrics['total_repos']}",
            f"- ⭐ **Total de estrelas**: {metrics['total_stars']}",
            f"- 🍴 **Total de forks**: {metrics['total_forks']}",
            f"- 👀 **Total de watchers**: {metrics['total_watchers']}",
            f"- 📊 **Média de estrelas por repo**: {metrics['avg_stars_per_repo']}",
            f"- 👥 **Seguidores**: {user_data.get('followers', 0)}",
            f"- 💾 **Tamanho total dos repos**: {round(metrics['total_size'] / 1024, 2)} MB",
            ""
        ]

        # Destaques
        if metrics['most_starred_repo']:
            report.extend([
                "## 🌟 Projeto Mais Popular",
                "",
                f"[{metrics['most_starred_repo']['name']}]({metrics['most_starred_repo']['url']}) - ⭐ {metrics['most_starred_repo']['stars']} estrelas",
                ""
            ])

        # Top linguagens
        if metrics['languages']:
            report.extend([
                "## 💻 Top Linguagens",
                ""
            ])
            for lang, count in metrics['languages'].most_common(5):
                percentage = round((count / metrics['total_repos']) * 100, 1)
                report.append(f"- **{lang}**: {count} repos ({percentage}%)")
            report.append("")

        # Topics mais usados
        if metrics['topics']:
            report.extend([
                "## 🏷️ Topics Mais Usados",
                ""
            ])
            for topic, count in metrics['topics'].most_common(5):
                report.append(f"- `{topic}` ({count})")
            report.append("")

        # Comparação com comunidade
        comparison = self.compare_with_community()
        report.extend([
            "## 🎯 Insights e Recomendações",
            ""
        ])
        for insight in comparison['insights']:
            report.append(f"- {insight}")

        report.extend([
            "",
            "---",
            "",
            f"🤖 Gerado automaticamente em {datetime.now().strftime('%d/%m/%Y às %H:%M')}"
        ])

        return "\n".join(report)

    def generate_repo_spotlight(self, repo_name: str) -> str:
        """Gera spotlight detalhado de um repositório"""
        growth = self.track_repo_growth(repo_name)

        spotlight = [
            f"# 🔦 Spotlight: {repo_name}",
            "",
            f"## 📊 Métricas",
            "",
            f"- ⭐ **Estrelas**: {growth['current_stars']}",
            f"- 🍴 **Forks**: {growth['current_forks']}",
            f"- 👀 **Watchers**: {growth['current_watchers']}",
            f"- 🐛 **Issues abertas**: {growth['open_issues']}",
            f"- 📅 **Idade**: {growth['age_days']} dias",
            f"- 📈 **Taxa de crescimento**: {growth['stars_per_day']} estrelas/dia",
            f"- 💻 **Linguagem principal**: {growth['language']}",
            "",
            "## 💡 Análise",
            ""
        ]

        # Análises
        if growth['stars_per_day'] >= 1:
            spotlight.append("🚀 Crescimento excepcional! Projeto com alta tração.")
        elif growth['stars_per_day'] >= 0.1:
            spotlight.append("⭐ Bom crescimento orgânico.")
        else:
            spotlight.append("💡 Considere estratégias de divulgação para aumentar visibilidade.")

        spotlight.append("")

        if growth['current_forks'] > growth['current_stars'] * 0.3:
            spotlight.append("🔥 Alto engajamento! Muitas pessoas estão contribuindo ou usando o código.")
            spotlight.append("")

        if growth['open_issues'] > 10:
            spotlight.append("⚠️ Muitas issues abertas. Considere priorizar resolução ou convidar colaboradores.")
            spotlight.append("")

        return "\n".join(spotlight)

    def suggest_focus_areas(self) -> List[str]:
        """Sugere áreas de foco baseadas em análise"""
        metrics = self.calculate_total_metrics()
        suggestions = []

        # Análise de engajamento
        if metrics['total_repos'] > 0:
            engagement_rate = (metrics['repos_with_stars'] / metrics['total_repos']) * 100

            if engagement_rate < 30:
                suggestions.append(
                    "📢 **Divulgação**: Apenas {:.0f}% dos seus repos têm estrelas. "
                    "Considere compartilhar mais seus projetos nas redes sociais.".format(engagement_rate)
                )

        # Análise de documentação
        repos = self.get_all_repos()
        repos_without_description = sum(1 for r in repos if not r.get('description') and not r.get('private'))

        if repos_without_description > 0:
            suggestions.append(
                f"📝 **Documentação**: {repos_without_description} repositórios sem descrição. "
                "Adicione descrições claras para melhorar descoberta."
            )

        # Análise de linguagens
        if len(metrics['languages']) < 3:
            suggestions.append(
                "🎨 **Diversificação**: Você usa principalmente {0}. "
                "Explorar novas linguagens pode expandir suas oportunidades.".format(
                    metrics['languages'].most_common(1)[0][0] if metrics['languages'] else 'N/A'
                )
            )

        # Análise de atividade
        if metrics['newest_repo']:
            days_since_last = (datetime.now() - metrics['newest_repo']['date']).days
            if days_since_last > 90:
                suggestions.append(
                    f"🚀 **Novos Projetos**: Seu último repositório foi criado há {days_since_last} dias. "
                    "Que tal começar algo novo?"
                )

        # Sugestão de colaboração
        if metrics['total_forks'] < metrics['total_stars'] * 0.1:
            suggestions.append(
                "🤝 **Colaboração**: Seus projetos têm poucas forks. "
                "Incentive contribuições adicionando CONTRIBUTING.md e issues marcadas como 'good first issue'."
            )

        return suggestions

    def create_insights_dashboard(self, output_file: str = 'INSIGHTS_DASHBOARD.md'):
        """Cria dashboard completo de insights"""
        metrics = self.calculate_total_metrics()

        dashboard = [
            "# 📊 Dashboard de Insights",
            "",
            f"Última atualização: {datetime.now().strftime('%d/%m/%Y às %H:%M')}",
            "",
            "## 🎯 Visão Geral",
            "",
            self.generate_weekly_report(),
            "",
            "## 💡 Áreas de Foco Sugeridas",
            ""
        ]

        suggestions = self.suggest_focus_areas()
        for suggestion in suggestions:
            dashboard.append(f"### {suggestion}")
            dashboard.append("")

        # Tabela de todos os repos com métricas
        dashboard.extend([
            "## 📋 Tabela de Repositórios",
            "",
            "| Repositório | ⭐ Stars | 🍴 Forks | Linguagem | Atualizado |",
            "|------------|---------|---------|-----------|------------|"
        ])

        repos = self.get_all_repos()
        for repo in sorted(repos, key=lambda x: x.get('stargazers_count', 0), reverse=True)[:20]:
            if repo.get('private'):
                continue

            name = repo['name']
            stars = repo.get('stargazers_count', 0)
            forks = repo.get('forks_count', 0)
            lang = repo.get('language', 'N/A')
            updated = datetime.strptime(repo['updated_at'], '%Y-%m-%dT%H:%M:%SZ').strftime('%d/%m/%Y')

            dashboard.append(f"| [{name}]({repo['html_url']}) | {stars} | {forks} | {lang} | {updated} |")

        # Salva dashboard
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(dashboard))

        print(f"✅ Dashboard de insights salvo em {output_file}")


def main():
    """Função principal para testes"""
    agent = InsightsAgent('krisalexandre2018')

    print("Calculando métricas...")
    metrics = agent.calculate_total_metrics()

    print(f"\n📊 Métricas Totais:")
    print(f"- Repositórios: {metrics['total_repos']}")
    print(f"- Total de estrelas: {metrics['total_stars']}")
    print(f"- Média de estrelas: {metrics['avg_stars_per_repo']}")

    print("\nGerando dashboard completo...")
    agent.create_insights_dashboard()


if __name__ == '__main__':
    main()
