"""
Agente de Documentação
Responsável por garantir documentação clara e profissional em todos os projetos
"""

import os
import requests
from typing import Dict, List, Optional
from datetime import datetime


class DocumentationAgent:
    """Agente responsável pela documentação dos projetos"""

    def __init__(self, username: str, github_token: Optional[str] = None):
        self.username = username
        self.github_token = github_token or os.getenv('GITHUB_TOKEN')
        self.api_base = 'https://api.github.com'
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
        }
        if self.github_token:
            self.headers['Authorization'] = f'token {self.github_token}'

    def get_repo_info(self, repo_name: str) -> Dict:
        """Obtém informações do repositório"""
        url = f'{self.api_base}/repos/{self.username}/{repo_name}'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_repo_languages(self, repo_name: str) -> Dict[str, int]:
        """Obtém linguagens usadas no repositório"""
        url = f'{self.api_base}/repos/{self.username}/{repo_name}/languages'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def detect_project_type(self, repo_info: Dict, languages: Dict) -> str:
        """Detecta o tipo de projeto baseado nas linguagens e arquivos"""
        main_lang = repo_info.get('language', '').lower()

        # Mapeamento de tipos
        if 'javascript' in main_lang or 'typescript' in main_lang:
            if 'React' in repo_info.get('topics', []):
                return 'react-app'
            elif 'Vue' in repo_info.get('topics', []):
                return 'vue-app'
            elif 'Node' in repo_info.get('topics', []):
                return 'node-api'
            return 'javascript-project'
        elif 'python' in main_lang:
            if 'django' in repo_info.get('topics', []):
                return 'django-app'
            elif 'flask' in repo_info.get('topics', []):
                return 'flask-app'
            return 'python-project'
        elif 'html' in main_lang:
            return 'static-website'
        elif 'java' in main_lang:
            return 'java-project'
        elif 'php' in main_lang:
            return 'php-project'

        return 'generic-project'

    def generate_readme_template(self, repo_name: str, config: Optional[Dict] = None) -> str:
        """Gera template de README baseado no tipo de projeto"""
        config = config or {}

        try:
            repo_info = self.get_repo_info(repo_name)
            languages = self.get_repo_languages(repo_name)
        except:
            repo_info = {'name': repo_name, 'description': 'Projeto sem descrição'}
            languages = {}

        project_type = self.detect_project_type(repo_info, languages)
        description = repo_info.get('description', 'Projeto sem descrição')

        # Template base
        readme = [
            f"# {repo_name}",
            "",
            f"## 📋 Sobre o Projeto",
            "",
            description,
            "",
            "## 🚀 Tecnologias Utilizadas",
            ""
        ]

        # Adiciona linguagens
        if languages:
            for lang in languages.keys():
                readme.append(f"- {lang}")

        readme.extend([
            "",
            "## 📦 Instalação",
            "",
            "### Pré-requisitos",
            ""
        ])

        # Instruções específicas por tipo
        if project_type == 'node-api' or project_type == 'react-app':
            readme.extend([
                "- Node.js (v14 ou superior)",
                "- npm ou yarn",
                "",
                "### Instalando dependências",
                "",
                "```bash",
                "# Clonar o repositório",
                f"git clone https://github.com/{self.username}/{repo_name}.git",
                "",
                "# Entrar na pasta do projeto",
                f"cd {repo_name}",
                "",
                "# Instalar dependências",
                "npm install",
                "# ou",
                "yarn install",
                "```"
            ])
        elif project_type == 'python-project':
            readme.extend([
                "- Python 3.8 ou superior",
                "- pip",
                "",
                "### Instalando dependências",
                "",
                "```bash",
                "# Clonar o repositório",
                f"git clone https://github.com/{self.username}/{repo_name}.git",
                "",
                "# Entrar na pasta do projeto",
                f"cd {repo_name}",
                "",
                "# Criar ambiente virtual",
                "python -m venv venv",
                "",
                "# Ativar ambiente virtual",
                "# No Windows:",
                "venv\\Scripts\\activate",
                "# No Linux/Mac:",
                "source venv/bin/activate",
                "",
                "# Instalar dependências",
                "pip install -r requirements.txt",
                "```"
            ])
        elif project_type == 'static-website':
            readme.extend([
                "- Navegador web moderno",
                "",
                "### Como usar",
                "",
                "```bash",
                "# Clonar o repositório",
                f"git clone https://github.com/{self.username}/{repo_name}.git",
                "",
                "# Abrir o arquivo index.html no navegador",
                "```"
            ])

        # Seção de uso
        readme.extend([
            "",
            "## 💻 Como Usar",
            ""
        ])

        if project_type in ['node-api', 'react-app']:
            readme.extend([
                "```bash",
                "# Executar em modo de desenvolvimento",
                "npm run dev",
                "# ou",
                "yarn dev",
                "",
                "# Build para produção",
                "npm run build",
                "# ou",
                "yarn build",
                "```"
            ])
        elif project_type in ['python-project', 'django-app', 'flask-app']:
            readme.extend([
                "```bash",
                "# Executar o projeto",
                "python main.py",
                "```"
            ])

        # Seção de funcionalidades
        readme.extend([
            "",
            "## ✨ Funcionalidades",
            "",
            "- [ ] Funcionalidade 1",
            "- [ ] Funcionalidade 2",
            "- [ ] Funcionalidade 3",
            ""
        ])

        # Estrutura do projeto
        readme.extend([
            "## 📁 Estrutura do Projeto",
            "",
            "```",
            f"{repo_name}/",
            "├── src/          # Código fonte",
            "├── docs/         # Documentação",
            "├── tests/        # Testes",
            "└── README.md     # Este arquivo",
            "```",
            ""
        ])

        # Screenshots (opcional)
        if config.get('include_screenshots', True):
            readme.extend([
                "## 📸 Screenshots",
                "",
                "<!-- Adicione screenshots aqui -->",
                "",
                "![Screenshot 1](docs/screenshots/screenshot1.png)",
                ""
            ])

        # Roadmap
        readme.extend([
            "## 🗺️ Roadmap",
            "",
            "- [ ] Implementar funcionalidade X",
            "- [ ] Melhorar performance",
            "- [ ] Adicionar testes",
            "- [ ] Documentar API",
            ""
        ])

        # Contribuição
        readme.extend([
            "## 🤝 Como Contribuir",
            "",
            "Contribuições são sempre bem-vindas!",
            "",
            "1. Faça um fork do projeto",
            "2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)",
            "3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)",
            "4. Push para a branch (`git push origin feature/AmazingFeature`)",
            "5. Abra um Pull Request",
            ""
        ])

        # Licença
        license_info = repo_info.get('license')
        if license_info:
            license_name = license_info.get('name', 'MIT')
            readme.extend([
                "## 📝 Licença",
                "",
                f"Este projeto está sob a licença {license_name}. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.",
                ""
            ])
        else:
            readme.extend([
                "## 📝 Licença",
                "",
                "Este projeto ainda não possui uma licença definida.",
                ""
            ])

        # Contato
        readme.extend([
            "## 📧 Contato",
            "",
            f"**{self.username}**",
            "",
            f"- GitHub: [@{self.username}](https://github.com/{self.username})",
            "- LinkedIn: [Seu LinkedIn](https://linkedin.com/in/seu-perfil)",
            "",
            "---",
            "",
            f"⭐ Se este projeto te ajudou, considere dar uma estrela!",
            ""
        ])

        return "\n".join(readme)

    def generate_changelog_template(self) -> str:
        """Gera template de CHANGELOG"""
        changelog = [
            "# Changelog",
            "",
            "Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.",
            "",
            "O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),",
            "e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).",
            "",
            "## [Não publicado]",
            "",
            "### Adicionado",
            "- Nova funcionalidade X",
            "",
            "### Modificado",
            "- Melhoria na funcionalidade Y",
            "",
            "### Corrigido",
            "- Bug no componente Z",
            "",
            f"## [1.0.0] - {datetime.now().strftime('%Y-%m-%d')}",
            "",
            "### Adicionado",
            "- Versão inicial do projeto",
            ""
        ]
        return "\n".join(changelog)

    def generate_contributing_guide(self) -> str:
        """Gera guia de contribuição"""
        guide = [
            "# Guia de Contribuição",
            "",
            "Obrigado por considerar contribuir com este projeto! 🎉",
            "",
            "## Como Contribuir",
            "",
            "### Reportando Bugs",
            "",
            "Antes de criar um issue, por favor:",
            "",
            "1. Verifique se o bug já não foi reportado",
            "2. Inclua informações detalhadas sobre como reproduzir o problema",
            "3. Inclua screenshots se aplicável",
            "4. Descreva o comportamento esperado vs. o comportamento atual",
            "",
            "### Sugerindo Melhorias",
            "",
            "Adoramos receber sugestões! Para sugerir uma melhoria:",
            "",
            "1. Crie um issue descrevendo a melhoria",
            "2. Explique por que esta melhoria seria útil",
            "3. Forneça exemplos de uso se possível",
            "",
            "### Pull Requests",
            "",
            "1. Faça fork do repositório",
            "2. Crie uma branch a partir da `main` (`git checkout -b feature/minha-feature`)",
            "3. Faça suas alterações",
            "4. Adicione testes se aplicável",
            "5. Certifique-se de que os testes passam",
            "6. Commit suas mudanças seguindo o padrão de commits",
            "7. Push para sua branch",
            "8. Abra um Pull Request",
            "",
            "## Padrão de Commits",
            "",
            "Usamos [Conventional Commits](https://www.conventionalcommits.org/pt-br/):",
            "",
            "```",
            "feat: adiciona nova funcionalidade",
            "fix: corrige um bug",
            "docs: atualiza documentação",
            "style: mudanças de formatação",
            "refactor: refatoração de código",
            "test: adiciona ou modifica testes",
            "chore: outras mudanças que não modificam src ou test",
            "```",
            "",
            "## Código de Conduta",
            "",
            "Este projeto segue um código de conduta. Ao participar, você concorda em manter um ambiente respeitoso e inclusivo.",
            ""
        ]
        return "\n".join(guide)

    def translate_readme_to_english(self, readme_pt: str) -> str:
        """
        Traduz README de português para inglês
        Nota: Implementação básica. Para produção, usar API de tradução
        """
        translations = {
            "# Sobre o Projeto": "# About The Project",
            "## 🚀 Tecnologias Utilizadas": "## 🚀 Technologies Used",
            "## 📦 Instalação": "## 📦 Installation",
            "### Pré-requisitos": "### Prerequisites",
            "### Instalando dependências": "### Installing Dependencies",
            "## 💻 Como Usar": "## 💻 How To Use",
            "## ✨ Funcionalidades": "## ✨ Features",
            "## 📁 Estrutura do Projeto": "## 📁 Project Structure",
            "## 📸 Screenshots": "## 📸 Screenshots",
            "## 🗺️ Roadmap": "## 🗺️ Roadmap",
            "## 🤝 Como Contribuir": "## 🤝 How To Contribute",
            "## 📝 Licença": "## 📝 License",
            "## 📧 Contato": "## 📧 Contact",
            "Clonar o repositório": "Clone the repository",
            "Entrar na pasta do projeto": "Enter the project folder",
            "Instalar dependências": "Install dependencies",
            "Executar em modo de desenvolvimento": "Run in development mode",
            "Build para produção": "Build for production",
            "Contribuições são sempre bem-vindas!": "Contributions are always welcome!",
        }

        readme_en = readme_pt
        for pt, en in translations.items():
            readme_en = readme_en.replace(pt, en)

        return readme_en

    def create_documentation_package(self, repo_name: str, output_dir: str = '.'):
        """Cria pacote completo de documentação"""
        os.makedirs(output_dir, exist_ok=True)

        # README principal
        readme_pt = self.generate_readme_template(repo_name)
        with open(f'{output_dir}/README.md', 'w', encoding='utf-8') as f:
            f.write(readme_pt)
        print(f"✅ README.md criado")

        # README em inglês
        readme_en = self.translate_readme_to_english(readme_pt)
        with open(f'{output_dir}/README.en.md', 'w', encoding='utf-8') as f:
            f.write(readme_en)
        print(f"✅ README.en.md criado")

        # CHANGELOG
        changelog = self.generate_changelog_template()
        with open(f'{output_dir}/CHANGELOG.md', 'w', encoding='utf-8') as f:
            f.write(changelog)
        print(f"✅ CHANGELOG.md criado")

        # CONTRIBUTING
        contributing = self.generate_contributing_guide()
        with open(f'{output_dir}/CONTRIBUTING.md', 'w', encoding='utf-8') as f:
            f.write(contributing)
        print(f"✅ CONTRIBUTING.md criado")

        print(f"\n🎉 Pacote de documentação completo criado em '{output_dir}'")


def main():
    """Função principal para testes"""
    agent = DocumentationAgent('krisalexandre2018')

    # Exemplo: gerar documentação para um repositório
    # agent.create_documentation_package('nome-do-repo', output_dir='./docs')

    # Ou gerar apenas README
    readme = agent.generate_readme_template('exemplo-projeto')
    print(readme)


if __name__ == '__main__':
    main()
