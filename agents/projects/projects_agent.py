"""
Agente de Projetos (Curadoria e Destaque)
Responsável por escolher e organizar repositórios em destaque
"""

import os
import requests
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from collections import defaultdict


class ProjectsAgent:
    """Agente responsável pela curadoria e destaque de projetos"""

    def __init__(self, username: str, github_token: Optional[str] = None):
        self.username = username
        self.github_token = github_token or os.getenv('GITHUB_TOKEN')
        self.api_base = 'https://api.github.com'
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
        }
        if self.github_token:
            self.headers['Authorization'] = f'token {self.github_token}'

    def get_all_repos(self) -> List[Dict]:
        """Obtém todos os repositórios do usuário"""
        url = f'{self.api_base}/users/{self.username}/repos'
        params = {'sort': 'updated', 'per_page': 100}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def calculate_repo_score(self, repo: Dict) -> float:
        """Calcula score de relevância do repositório"""
        score = 0.0

        # Pontos por estrelas
        score += repo.get('stargazers_count', 0) * 3

        # Pontos por forks
        score += repo.get('forks_count', 0) * 2

        # Pontos por watchers
        score += repo.get('watchers_count', 0) * 1

        # Pontos por issues abertas (indica atividade)
        score += repo.get('open_issues_count', 0) * 0.5

        # Bonus se não for fork
        if not repo.get('fork', False):
            score += 10

        # Bonus se tiver descrição
        if repo.get('description'):
            score += 5

        # Bonus se tiver homepage
        if repo.get('homepage'):
            score += 3

        # Bonus se tiver topics/tags
        score += len(repo.get('topics', [])) * 2

        # Penalidade por inatividade (mais de 1 ano)
        updated_at = datetime.strptime(repo['updated_at'], '%Y-%m-%dT%H:%M:%SZ')
        days_since_update = (datetime.now() - updated_at).days
        if days_since_update > 365:
            score *= 0.5

        return score

    def get_top_repos(self, limit: int = 6) -> List[Dict]:
        """Retorna os top repositórios por score"""
        repos = self.get_all_repos()
        repos_with_score = [
            (repo, self.calculate_repo_score(repo))
            for repo in repos
            if not repo.get('private', False)
        ]

        # Ordena por score
        repos_with_score.sort(key=lambda x: x[1], reverse=True)

        return [repo for repo, score in repos_with_score[:limit]]

    def get_repos_by_language(self) -> Dict[str, List[Dict]]:
        """Agrupa repositórios por linguagem"""
        repos = self.get_all_repos()
        by_language = defaultdict(list)

        for repo in repos:
            if repo.get('private', False) or repo.get('fork', False):
                continue

            language = repo.get('language', 'Other')
            by_language[language].append(repo)

        return dict(by_language)

    def suggest_description_improvements(self, repo: Dict) -> List[str]:
        """Sugere melhorias na descrição do repositório"""
        suggestions = []

        # Verifica se tem descrição
        if not repo.get('description'):
            suggestions.append("⚠️ Adicionar uma descrição clara do projeto")

        # Verifica se tem topics
        if not repo.get('topics') or len(repo.get('topics', [])) == 0:
            suggestions.append("🏷️ Adicionar tags/topics relevantes (ex: javascript, react, python)")

        # Verifica se tem homepage
        if not repo.get('homepage'):
            suggestions.append("🔗 Adicionar link de demo/homepage se disponível")

        # Verifica se tem licença
        if not repo.get('license'):
            suggestions.append("📄 Adicionar uma licença ao projeto")

        return suggestions

    def generate_project_card(self, repo: Dict) -> str:
        """Gera um card visual para o projeto"""
        name = repo['name']
        description = repo.get('description', 'Sem descrição')
        language = repo.get('language', 'N/A')
        stars = repo.get('stargazers_count', 0)
        forks = repo.get('forks_count', 0)
        url = repo['html_url']

        # Mapa de cores por linguagem
        lang_colors = {
            'Python': '3776AB',
            'JavaScript': 'F7DF1E',
            'TypeScript': '007ACC',
            'HTML': 'E34F26',
            'CSS': '1572B6',
            'Java': 'ED8B00',
            'PHP': '777BB4',
            'C++': '00599C',
            'C#': '239120',
            'Go': '00ADD8',
            'Rust': '000000',
            'Ruby': 'CC342D',
        }

        color = lang_colors.get(language, '0e75b6')

        card = f"""
<a href="{url}">
  <img align="center" src="https://github-readme-stats.vercel.app/api/pin/?username={self.username}&repo={name}&theme=radical&bg_color=0D1117&title_color=FFFFFF&text_color=CCCCCC&icon_color={color}" />
</a>
"""
        return card.strip()

    def generate_projects_showcase(self, top_n: int = 6) -> str:
        """Gera showcase de projetos em destaque"""
        top_repos = self.get_top_repos(limit=top_n)

        showcase = [
            "## 🚀 Projetos em Destaque",
            "",
            "<p align=\"center\">"
        ]

        for i, repo in enumerate(top_repos):
            showcase.append(self.generate_project_card(repo))
            # Quebra de linha a cada 2 projetos
            if (i + 1) % 2 == 0 and i < len(top_repos) - 1:
                showcase.append("")

        showcase.append("</p>")

        return "\n".join(showcase)

    def generate_language_stats_section(self) -> str:
        """Gera seção de estatísticas por linguagem"""
        by_language = self.get_repos_by_language()

        # Conta projetos por linguagem
        lang_counts = {lang: len(repos) for lang, repos in by_language.items()}
        sorted_langs = sorted(lang_counts.items(), key=lambda x: x[1], reverse=True)

        section = [
            "## 💻 Projetos por Linguagem",
            ""
        ]

        for lang, count in sorted_langs[:5]:  # Top 5 linguagens
            section.append(f"- **{lang}**: {count} projeto{'s' if count > 1 else ''}")

        return "\n".join(section)

    def generate_portfolio_page(self, output_file: str = 'PORTFOLIO.md'):
        """Gera página completa de portfólio"""
        portfolio = [
            f"# 📂 Portfólio - {self.username}",
            "",
            f"Última atualização: {datetime.now().strftime('%d/%m/%Y às %H:%M')}",
            "",
            "---",
            ""
        ]

        # Projetos em destaque
        portfolio.append(self.generate_projects_showcase(top_n=6))
        portfolio.append("")

        # Estatísticas por linguagem
        portfolio.append(self.generate_language_stats_section())
        portfolio.append("")

        # Todos os projetos
        portfolio.append("## 📋 Todos os Projetos")
        portfolio.append("")

        repos = self.get_all_repos()
        for repo in repos:
            if repo.get('private', False):
                continue

            name = repo['name']
            description = repo.get('description', 'Sem descrição')
            url = repo['html_url']
            language = repo.get('language', 'N/A')
            stars = repo.get('stargazers_count', 0)

            portfolio.append(f"### [{name}]({url})")
            portfolio.append(f"**Linguagem**: {language} | **⭐ Stars**: {stars}")
            portfolio.append(f"{description}")

            # Sugestões de melhoria
            suggestions = self.suggest_description_improvements(repo)
            if suggestions:
                portfolio.append("")
                portfolio.append("**Sugestões de melhoria:**")
                for suggestion in suggestions:
                    portfolio.append(f"- {suggestion}")

            portfolio.append("")

        # Salva arquivo
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(portfolio))

        print(f"✅ Portfólio gerado em {output_file}")

    def analyze_repos_health(self) -> Dict:
        """Analisa a saúde geral dos repositórios"""
        repos = self.get_all_repos()

        stats = {
            'total_repos': len(repos),
            'repos_without_description': 0,
            'repos_without_topics': 0,
            'repos_without_license': 0,
            'inactive_repos': 0,  # Mais de 1 ano sem atualização
            'top_languages': {},
            'total_stars': 0,
            'total_forks': 0
        }

        for repo in repos:
            if repo.get('private', False):
                continue

            # Contadores
            if not repo.get('description'):
                stats['repos_without_description'] += 1

            if not repo.get('topics') or len(repo.get('topics', [])) == 0:
                stats['repos_without_topics'] += 1

            if not repo.get('license'):
                stats['repos_without_license'] += 1

            # Inatividade
            updated_at = datetime.strptime(repo['updated_at'], '%Y-%m-%dT%H:%M:%SZ')
            days_since_update = (datetime.now() - updated_at).days
            if days_since_update > 365:
                stats['inactive_repos'] += 1

            # Linguagens
            lang = repo.get('language', 'Other')
            stats['top_languages'][lang] = stats['top_languages'].get(lang, 0) + 1

            # Totais
            stats['total_stars'] += repo.get('stargazers_count', 0)
            stats['total_forks'] += repo.get('forks_count', 0)

        return stats

    def generate_health_report(self) -> str:
        """Gera relatório de saúde dos repositórios"""
        stats = self.analyze_repos_health()

        report = [
            "# 📊 Relatório de Saúde dos Repositórios",
            "",
            f"**Total de repositórios públicos**: {stats['total_repos']}",
            f"**Total de estrelas**: ⭐ {stats['total_stars']}",
            f"**Total de forks**: 🍴 {stats['total_forks']}",
            "",
            "## ⚠️ Pontos de Atenção",
            "",
            f"- Repositórios sem descrição: **{stats['repos_without_description']}**",
            f"- Repositórios sem tags/topics: **{stats['repos_without_topics']}**",
            f"- Repositórios sem licença: **{stats['repos_without_license']}**",
            f"- Repositórios inativos (+1 ano): **{stats['inactive_repos']}**",
            "",
            "## 💡 Recomendações",
            ""
        ]

        # Recomendações personalizadas
        if stats['repos_without_description'] > 0:
            report.append("- Adicione descrições claras aos seus projetos para melhorar a descoberta")

        if stats['repos_without_topics'] > 0:
            report.append("- Use tags/topics para categorizar seus repositórios")

        if stats['inactive_repos'] > 3:
            report.append("- Considere arquivar repositórios muito antigos ou adicionar um README explicando o status")

        return "\n".join(report)


def main():
    """Função principal para testes"""
    agent = ProjectsAgent('krisalexandre2018')

    print("Gerando portfólio...")
    agent.generate_portfolio_page()

    print("\nGerando relatório de saúde...")
    report = agent.generate_health_report()
    print(report)


if __name__ == '__main__':
    main()
