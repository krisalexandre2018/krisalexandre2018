"""
Agente de Perfil (Bio & Branding)
Responsável por montar e atualizar automaticamente o README do perfil
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional


class ProfileAgent:
    """Agente responsável pela gestão do perfil do GitHub"""

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
        """Obtém dados do usuário via GitHub API"""
        url = f'{self.api_base}/users/{self.username}'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_user_repos(self) -> List[Dict]:
        """Obtém repositórios do usuário"""
        url = f'{self.api_base}/users/{self.username}/repos'
        params = {'sort': 'updated', 'per_page': 100}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def get_language_stats(self) -> Dict[str, int]:
        """Calcula estatísticas de linguagens usadas"""
        repos = self.get_user_repos()
        languages = {}

        for repo in repos:
            if repo['fork']:
                continue

            lang_url = repo['languages_url']
            response = requests.get(lang_url, headers=self.headers)
            if response.status_code == 200:
                repo_languages = response.json()
                for lang, bytes_count in repo_languages.items():
                    languages[lang] = languages.get(lang, 0) + bytes_count

        return languages

    def generate_bio_pt(self, user_data: Dict, custom_info: Dict) -> str:
        """Gera bio em português"""
        # Usa display_name da config, ou name do GitHub, ou username
        display_name = custom_info.get('display_name') or user_data.get('name') or self.username
        bio_lines = [
            f"# Olá! Eu sou o {display_name} 👋",
            "",
            "## Sobre mim",
            ""
        ]

        # Adiciona informações customizadas
        if custom_info.get('work_focus'):
            bio_lines.append(f"- 🔭 Trabalho e estudo tecnologias voltadas para **{custom_info['work_focus']}**")

        if custom_info.get('learning'):
            bio_lines.append(f"- 🌱 Atualmente estou aprendendo **{custom_info['learning']}**")

        if custom_info.get('collaboration'):
            bio_lines.append(f"- 👯 Busco colaborar em projetos de **{custom_info['collaboration']}**")

        if custom_info.get('looking_for'):
            bio_lines.append(f"- 🤔 Estou em busca de aprender mais sobre **{custom_info['looking_for']}**")

        if custom_info.get('ask_me_about'):
            bio_lines.append(f"- 💬 Pode me perguntar sobre **{custom_info['ask_me_about']}**")

        if custom_info.get('career_goal'):
            bio_lines.append(f"- 🎯 **Meta**: {custom_info['career_goal']}")
            if custom_info.get('current_level'):
                bio_lines[-1] += f" ({custom_info['current_level'].lower()})"

        if custom_info.get('pronouns'):
            bio_lines.append(f"- 😄 Pronomes: **{custom_info['pronouns']}**")

        return "\n".join(bio_lines)

    def generate_bio_en(self, user_data: Dict, custom_info: Dict) -> str:
        """Gera bio em inglês"""
        bio_lines = [
            f"# Hi! I'm {user_data.get('name', self.username)} 👋",
            "",
            "## About me",
            ""
        ]

        # Traduz informações para inglês
        if custom_info.get('work_focus_en'):
            bio_lines.append(f"- 🔭 I'm working and studying technologies related to **{custom_info['work_focus_en']}**")

        if custom_info.get('learning_en'):
            bio_lines.append(f"- 🌱 I'm currently learning **{custom_info['learning_en']}**")

        if custom_info.get('collaboration_en'):
            bio_lines.append(f"- 👯 I'm looking to collaborate on **{custom_info['collaboration_en']}** projects")

        if custom_info.get('looking_for_en'):
            bio_lines.append(f"- 🤔 I'm looking to learn more about **{custom_info['looking_for_en']}**")

        if custom_info.get('ask_me_about_en'):
            bio_lines.append(f"- 💬 Ask me about **{custom_info['ask_me_about_en']}**")

        if custom_info.get('pronouns_en'):
            bio_lines.append(f"- 😄 Pronouns: **{custom_info['pronouns_en']}**")

        return "\n".join(bio_lines)

    def generate_stats_section(self) -> str:
        """Gera seção de estatísticas do GitHub"""
        stats = f"""
## 📊 Estatísticas do GitHub

<p align="center">
  <img height="180em" src="https://github-readme-stats.vercel.app/api?username={self.username}&show_icons=true&theme=radical&bg_color=0D1117&title_color=FFFFFF&text_color=CCCCCC"/>
  <img height="180em" src="https://github-readme-stats.vercel.app/api/top-langs/?username={self.username}&layout=compact&theme=radical&bg_color=0D1117&title_color=FFFFFF&text_color=CCCCCC"/>
</p>
"""
        return stats

    def generate_snake_section(self) -> str:
        """Gera seção da animação da cobra"""
        return f"""

## 🐍 Contribuições no GitHub

![Snake animation](https://github.com/{self.username}/{self.username}/blob/output/github-contribution-grid-snake.svg)
"""

    def generate_tech_badges(self, technologies: List[str]) -> str:
        """Gera badges de tecnologias"""
        badge_map = {
            'HTML5': 'https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white',
            'CSS3': 'https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white',
            'JavaScript': 'https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black',
            'Python': 'https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white',
            'React': 'https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB',
            'Node.js': 'https://img.shields.io/badge/Node.js-43853D?style=for-the-badge&logo=node.js&logoColor=white',
            'TypeScript': 'https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white',
            'PHP': 'https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white',
            'Power BI': 'https://img.shields.io/badge/Power%20BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black',
            'Excel': 'https://img.shields.io/badge/Microsoft%20Excel-217346?style=for-the-badge&logo=microsoft-excel&logoColor=white',
            'Git': 'https://img.shields.io/badge/Git-E34F26?style=for-the-badge&logo=git&logoColor=white',
            'Docker': 'https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white',
            'VS Code': 'https://img.shields.io/badge/VS%20Code-007ACC?style=for-the-badge&logo=visual-studio-code&logoColor=white',
        }

        badges = ["## 🛠️ Tecnologias e Ferramentas", "", "<p align=\"center\">"]
        for tech in technologies:
            if tech in badge_map:
                badges.append(f'  <img src="{badge_map[tech]}" />')
        badges.append("</p>")

        return "\n".join(badges)

    def generate_contact_section(self, linkedin_url: Optional[str] = None) -> str:
        """Gera seção de contatos"""
        contact = [
            "## 📫 Como me encontrar",
            "",
            "<p align=\"center\">",
            f'  <a href="https://github.com/{self.username}">',
            '    <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" />',
            '  </a>'
        ]

        if linkedin_url:
            contact.extend([
                f'  <a href="{linkedin_url}">',
                '    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" />',
                '  </a>'
            ])

        contact.extend([
            "</p>",
            "",
            "---",
            "",
            "<p align=\"center\">",
            f'  <img src="https://komarev.com/ghpvc/?username={self.username}&label=Visualizações&color=0e75b6&style=flat" alt="Profile views" />',
            "</p>"
        ])

        return "\n".join(contact)

    def build_readme(self, config: Dict) -> str:
        """Constrói o README completo"""
        user_data = self.get_user_data()

        sections = []

        # Combina custom_info com display_name do config
        custom_info = config.get('custom_info', {}).copy()
        if config.get('display_name') and 'display_name' not in custom_info:
            custom_info['display_name'] = config['display_name']

        # Bio
        if config.get('language', 'pt-br') == 'pt-br':
            sections.append(self.generate_bio_pt(user_data, custom_info))
        else:
            sections.append(self.generate_bio_en(user_data, custom_info))

        # Estatísticas
        if config.get('include_stats', True):
            sections.append(self.generate_stats_section())

        # Snake animation
        if config.get('include_snake', True):
            sections.append(self.generate_snake_section())

        # Tecnologias
        if config.get('technologies'):
            sections.append(self.generate_tech_badges(config['technologies']))

        # Contatos
        sections.append(self.generate_contact_section(config.get('linkedin_url')))

        return "\n".join(sections)

    def update_readme(self, config: Dict, readme_path: str = 'README.md'):
        """Atualiza o arquivo README.md"""
        readme_content = self.build_readme(config)

        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)

        print(f"✅ README atualizado com sucesso em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


def main():
    """Função principal para testes"""
    # Configuração de exemplo
    config = {
        'language': 'pt-br',
        'custom_info': {
            'work_focus': 'HTML5, CSS3 e JavaScript',
            'learning': 'Python, PHP, React e Power Platform',
            'collaboration': 'desenvolvimento web, automação e inovação tecnológica',
            'looking_for': 'integração de dados e boas práticas de programação',
            'ask_me_about': 'criação de sites, automação com Excel e Power Apps',
            'pronouns': 'ele/dele'
        },
        'technologies': ['HTML5', 'CSS3', 'JavaScript', 'Python', 'React', 'Power BI', 'Excel'],
        'linkedin_url': 'https://www.linkedin.com/in/kristian-alexandre-94442018a/',
        'include_stats': True,
        'include_snake': True
    }

    agent = ProfileAgent('krisalexandre2018')
    agent.update_readme(config)


if __name__ == '__main__':
    main()
