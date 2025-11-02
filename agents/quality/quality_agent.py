"""
Agente de Código e Qualidade
Responsável por revisar código e sugerir melhorias de qualidade
"""

import os
import re
import requests
from typing import Dict, List, Optional, Tuple
from pathlib import Path


class QualityAgent:
    """Agente responsável pela qualidade de código"""

    def __init__(self, username: str, github_token: Optional[str] = None):
        self.username = username
        self.github_token = github_token or os.getenv('GITHUB_TOKEN')
        self.api_base = 'https://api.github.com'
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
        }
        if self.github_token:
            self.headers['Authorization'] = f'token {self.github_token}'

    def analyze_repo_structure(self, repo_name: str) -> Dict:
        """Analisa estrutura do repositório"""
        url = f'{self.api_base}/repos/{self.username}/{repo_name}/contents'
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            return {'error': 'Não foi possível acessar o repositório'}

        contents = response.json()

        analysis = {
            'has_readme': False,
            'has_license': False,
            'has_gitignore': False,
            'has_contributing': False,
            'has_changelog': False,
            'has_tests': False,
            'has_ci_cd': False,
            'has_package_json': False,
            'has_requirements': False,
            'has_dockerfile': False,
            'file_count': len(contents),
            'suggestions': []
        }

        filenames = [item['name'].lower() for item in contents]

        # Verifica arquivos importantes
        analysis['has_readme'] = any('readme' in f for f in filenames)
        analysis['has_license'] = any('license' in f for f in filenames)
        analysis['has_gitignore'] = '.gitignore' in filenames
        analysis['has_contributing'] = any('contributing' in f for f in filenames)
        analysis['has_changelog'] = any('changelog' in f for f in filenames)
        analysis['has_package_json'] = 'package.json' in filenames
        analysis['has_requirements'] = 'requirements.txt' in filenames
        analysis['has_dockerfile'] = any('dockerfile' in f for f in filenames)

        # Verifica testes
        analysis['has_tests'] = any(
            'test' in f or '__tests__' in f or 'spec' in f
            for item in contents
            for f in [item['name'].lower(), item.get('type', '')]
        )

        # Verifica CI/CD (GitHub Actions, etc)
        github_dir = next((item for item in contents if item['name'] == '.github'), None)
        if github_dir:
            workflows_url = f"{github_dir['url']}/workflows"
            workflows_response = requests.get(workflows_url, headers=self.headers)
            if workflows_response.status_code == 200:
                analysis['has_ci_cd'] = True

        # Gera sugestões
        if not analysis['has_readme']:
            analysis['suggestions'].append("📄 Adicionar README.md com documentação do projeto")

        if not analysis['has_license']:
            analysis['suggestions'].append("⚖️ Adicionar arquivo LICENSE")

        if not analysis['has_gitignore']:
            analysis['suggestions'].append("🚫 Adicionar .gitignore para ignorar arquivos desnecessários")

        if not analysis['has_tests']:
            analysis['suggestions'].append("🧪 Adicionar testes automatizados")

        if not analysis['has_ci_cd']:
            analysis['suggestions'].append("🔄 Configurar CI/CD com GitHub Actions")

        if not analysis['has_contributing']:
            analysis['suggestions'].append("🤝 Adicionar CONTRIBUTING.md para guiar colaboradores")

        return analysis

    def check_code_quality_patterns(self, code: str, language: str) -> List[str]:
        """Verifica padrões básicos de qualidade no código"""
        issues = []

        # Checks gerais
        lines = code.split('\n')

        # Linhas muito longas (>120 caracteres)
        long_lines = [i + 1 for i, line in enumerate(lines) if len(line) > 120]
        if long_lines:
            issues.append(f"⚠️ Linhas muito longas encontradas (>120 chars): linhas {long_lines[:5]}")

        # Tabs vs spaces (consistência)
        has_tabs = any('\t' in line for line in lines)
        has_spaces = any(re.match(r'^[ ]{2,}', line) for line in lines)
        if has_tabs and has_spaces:
            issues.append("⚠️ Mistura de tabs e espaços para indentação")

        # Checks específicos por linguagem
        if language.lower() in ['javascript', 'typescript']:
            # Var usage
            if 'var ' in code:
                issues.append("💡 Considere usar 'let' ou 'const' ao invés de 'var'")

            # Console.log em produção
            if 'console.log' in code:
                issues.append("🔍 console.log encontrado - considere remover em produção")

            # == ao invés de ===
            if '==' in code and '===' not in code:
                issues.append("⚡ Use '===' ao invés de '==' para comparações estritas")

        elif language.lower() == 'python':
            # Imports não organizados
            import_lines = [line for line in lines if line.startswith('import ') or line.startswith('from ')]
            if len(import_lines) > 5:
                issues.append("📦 Considere organizar imports com isort ou similar")

            # Print statements
            if 'print(' in code:
                issues.append("🔍 print() encontrado - considere usar logging em produção")

        elif language.lower() in ['java', 'c#', 'csharp']:
            # Falta de modificadores de acesso
            if re.search(r'\n\s*(class|interface)\s+\w+', code):
                if not re.search(r'\n\s*(public|private|protected)\s+(class|interface)', code):
                    issues.append("🔒 Considere adicionar modificadores de acesso explícitos")

        return issues

    def generate_quality_report(self, repo_name: str) -> str:
        """Gera relatório de qualidade para um repositório"""
        analysis = self.analyze_repo_structure(repo_name)

        if 'error' in analysis:
            return f"❌ Erro ao analisar repositório: {analysis['error']}"

        report = [
            f"# 🔍 Relatório de Qualidade: {repo_name}",
            "",
            "## 📋 Checklist de Qualidade",
            ""
        ]

        # Checklist visual
        checklist_items = [
            ("README.md", analysis['has_readme']),
            ("LICENSE", analysis['has_license']),
            (".gitignore", analysis['has_gitignore']),
            ("Testes", analysis['has_tests']),
            ("CI/CD", analysis['has_ci_cd']),
            ("CONTRIBUTING.md", analysis['has_contributing']),
            ("CHANGELOG.md", analysis['has_changelog'])
        ]

        for item, has_it in checklist_items:
            icon = "✅" if has_it else "❌"
            report.append(f"{icon} {item}")

        report.append("")

        # Score de qualidade
        total_checks = len(checklist_items)
        passed_checks = sum(1 for _, has_it in checklist_items if has_it)
        quality_score = round((passed_checks / total_checks) * 100, 1)

        report.extend([
            f"## 📊 Score de Qualidade: {quality_score}%",
            ""
        ])

        if quality_score >= 80:
            report.append("🌟 Excelente! Projeto bem estruturado.")
        elif quality_score >= 60:
            report.append("👍 Bom, mas há espaço para melhorias.")
        elif quality_score >= 40:
            report.append("⚠️ Precisa de atenção em várias áreas.")
        else:
            report.append("🚨 Requer melhorias significativas.")

        report.append("")

        # Sugestões
        if analysis['suggestions']:
            report.extend([
                "## 💡 Sugestões de Melhoria",
                ""
            ])
            for suggestion in analysis['suggestions']:
                report.append(f"- {suggestion}")
            report.append("")

        # Detecção de tecnologia
        tech_detected = []
        if analysis['has_package_json']:
            tech_detected.append("Node.js/JavaScript")
        if analysis['has_requirements']:
            tech_detected.append("Python")
        if analysis['has_dockerfile']:
            tech_detected.append("Docker")

        if tech_detected:
            report.extend([
                "## 🔧 Tecnologias Detectadas",
                ""
            ])
            for tech in tech_detected:
                report.append(f"- {tech}")
            report.append("")

        return "\n".join(report)

    def suggest_gitignore(self, language: str) -> str:
        """Sugere conteúdo de .gitignore baseado na linguagem"""
        gitignore_templates = {
            'python': """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.env
.venv
pip-log.txt
pip-delete-this-directory.txt
.pytest_cache/
*.egg-info/
dist/
build/
""",
            'javascript': """# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.npm
.yarn
.pnp.*

# Build
dist/
build/
*.tsbuildinfo

# Environment
.env
.env.local
.env.development
.env.test
.env.production

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
""",
            'java': """# Java
*.class
*.log
*.jar
*.war
*.ear
target/
.classpath
.project
.settings/
bin/

# IDE
.idea/
*.iml
*.iws
""",
            'generic': """# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
*.swo

# Build
dist/
build/
*.log

# Environment
.env
"""
        }

        return gitignore_templates.get(language.lower(), gitignore_templates['generic'])

    def suggest_github_actions_workflow(self, language: str) -> str:
        """Sugere workflow do GitHub Actions baseado na linguagem"""
        workflows = {
            'python': """name: Python CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov flake8

    - name: Lint with flake8
      run: |
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

    - name: Run tests
      run: |
        pytest --cov=./ --cov-report=xml
""",
            'javascript': """name: Node.js CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        node-version: [14.x, 16.x, 18.x]

    steps:
    - uses: actions/checkout@v3

    - name: Use Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v3
      with:
        node-version: ${{ matrix.node-version }}

    - name: Install dependencies
      run: npm ci

    - name: Run linter
      run: npm run lint

    - name: Run tests
      run: npm test

    - name: Build
      run: npm run build --if-present
"""
        }

        return workflows.get(language.lower(), workflows['javascript'])

    def create_quality_package(self, repo_name: str, language: str, output_dir: str = '.'):
        """Cria pacote completo de arquivos de qualidade"""
        os.makedirs(output_dir, exist_ok=True)

        # Relatório de qualidade
        report = self.generate_quality_report(repo_name)
        with open(f'{output_dir}/QUALITY_REPORT.md', 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"✅ QUALITY_REPORT.md criado")

        # .gitignore
        gitignore = self.suggest_gitignore(language)
        with open(f'{output_dir}/.gitignore', 'w', encoding='utf-8') as f:
            f.write(gitignore)
        print(f"✅ .gitignore criado")

        # GitHub Actions workflow
        workflow = self.suggest_github_actions_workflow(language)
        workflows_dir = f'{output_dir}/.github/workflows'
        os.makedirs(workflows_dir, exist_ok=True)
        with open(f'{workflows_dir}/ci.yml', 'w', encoding='utf-8') as f:
            f.write(workflow)
        print(f"✅ GitHub Actions workflow criado")

        print(f"\n🎉 Pacote de qualidade completo criado em '{output_dir}'")

    def generate_pr_review_template(self) -> str:
        """Gera template de revisão de PR"""
        template = """# 🔍 Checklist de Revisão de Pull Request

## 📋 Checklist Geral
- [ ] O código está limpo e bem formatado
- [ ] Variáveis e funções têm nomes descritivos
- [ ] Não há código comentado desnecessário
- [ ] Não há console.log/print statements de debug
- [ ] Não há segredos (API keys, senhas) no código

## 🧪 Testes
- [ ] Testes foram adicionados ou atualizados
- [ ] Todos os testes estão passando
- [ ] Cobertura de testes é adequada

## 📝 Documentação
- [ ] README foi atualizado se necessário
- [ ] Comentários foram adicionados em código complexo
- [ ] CHANGELOG foi atualizado

## 🔒 Segurança
- [ ] Input do usuário é validado
- [ ] Não há vulnerabilidades conhecidas
- [ ] Dependências estão atualizadas

## 🎯 Funcionalidade
- [ ] As mudanças atendem aos requisitos
- [ ] Não há breaking changes não documentadas
- [ ] Performance é aceitável

## 💡 Sugestões de Melhoria
<!-- Adicione sugestões aqui -->

## ✅ Aprovação
- [ ] Aprovado para merge
"""
        return template


def main():
    """Função principal para testes"""
    agent = QualityAgent('krisalexandre2018')

    # Exemplo: analisar um repositório
    # report = agent.generate_quality_report('nome-do-repo')
    # print(report)

    # Ou criar pacote completo
    # agent.create_quality_package('nome-do-repo', 'python', output_dir='./quality')

    print("Agente de Qualidade pronto!")
    print("\nFunções disponíveis:")
    print("- analyze_repo_structure(repo_name)")
    print("- generate_quality_report(repo_name)")
    print("- create_quality_package(repo_name, language)")
    print("- suggest_gitignore(language)")
    print("- suggest_github_actions_workflow(language)")


if __name__ == '__main__':
    main()
