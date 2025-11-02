"""
Sistema Principal de Orquestração dos Agentes
Execute este arquivo para rodar todos os agentes
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# Configurar encoding UTF-8 para Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'ignore')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'ignore')

from agents import (
    ProfileAgent,
    ProjectsAgent,
    DocumentationAgent,
    EngagementAgent,
    InsightsAgent,
    QualityAgent
)


class AgentOrchestrator:
    """Orquestrador principal dos agentes"""

    def __init__(self, config_path: str = 'config/agents_config.json'):
        self.config = self.load_config(config_path)
        self.username = self.config['github']['username']
        self.github_token = os.getenv('GITHUB_TOKEN', self.config['github'].get('token'))

        # Inicializa agentes
        self.profile_agent = ProfileAgent(self.username, self.github_token)
        self.projects_agent = ProjectsAgent(self.username, self.github_token)
        self.documentation_agent = DocumentationAgent(self.username, self.github_token)
        self.engagement_agent = EngagementAgent(self.username, self.github_token)
        self.insights_agent = InsightsAgent(self.username, self.github_token)
        self.quality_agent = QualityAgent(self.username, self.github_token)

    def load_config(self, config_path: str) -> dict:
        """Carrega configuração"""
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        # Substitui variáveis de ambiente
        if '${GITHUB_TOKEN}' in str(config):
            config_str = json.dumps(config)
            config_str = config_str.replace('${GITHUB_TOKEN}', os.getenv('GITHUB_TOKEN', ''))
            config = json.loads(config_str)

        return config

    def run_profile_update(self):
        """Executa atualização do perfil"""
        print("\n🎨 Executando Agente de Perfil...")
        try:
            self.profile_agent.update_readme(self.config['profile'])
            print("✅ Perfil atualizado com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao atualizar perfil: {e}")

    def run_projects_analysis(self):
        """Executa análise de projetos"""
        print("\n📂 Executando Agente de Projetos...")
        try:
            self.projects_agent.generate_portfolio_page('PORTFOLIO.md')
            report = self.projects_agent.generate_health_report()
            with open('PROJECTS_HEALTH.md', 'w', encoding='utf-8') as f:
                f.write(report)
            print("✅ Análise de projetos concluída!")
        except Exception as e:
            print(f"❌ Erro na análise de projetos: {e}")

    def run_documentation_check(self, repo_name: str = None):
        """Executa verificação de documentação"""
        print("\n📝 Executando Agente de Documentação...")
        try:
            if repo_name:
                self.documentation_agent.create_documentation_package(repo_name, './docs')
                print(f"✅ Documentação gerada para {repo_name}!")
            else:
                print("ℹ️  Especifique um repositório com --repo para gerar documentação")
        except Exception as e:
            print(f"❌ Erro ao gerar documentação: {e}")

    def run_engagement_analysis(self):
        """Executa análise de engajamento"""
        print("\n🤝 Executando Agente de Engajamento...")
        try:
            self.engagement_agent.create_engagement_report('ENGAGEMENT_REPORT.md')
            weekly = self.engagement_agent.generate_weekly_summary()
            with open('WEEKLY_SUMMARY.md', 'w', encoding='utf-8') as f:
                f.write(weekly)
            print("✅ Análise de engajamento concluída!")
        except Exception as e:
            print(f"❌ Erro na análise de engajamento: {e}")

    def run_insights_generation(self):
        """Executa geração de insights"""
        print("\n📊 Executando Agente de Insights...")
        try:
            self.insights_agent.create_insights_dashboard('INSIGHTS_DASHBOARD.md')
            print("✅ Dashboard de insights gerado!")
        except Exception as e:
            print(f"❌ Erro ao gerar insights: {e}")

    def run_quality_check(self, repo_name: str = None):
        """Executa verificação de qualidade"""
        print("\n🔍 Executando Agente de Qualidade...")
        try:
            if repo_name:
                report = self.quality_agent.generate_quality_report(repo_name)
                with open(f'QUALITY_REPORT_{repo_name}.md', 'w', encoding='utf-8') as f:
                    f.write(report)
                print(f"✅ Relatório de qualidade gerado para {repo_name}!")
            else:
                print("ℹ️  Especifique um repositório com --repo para verificar qualidade")
        except Exception as e:
            print(f"❌ Erro ao verificar qualidade: {e}")

    def run_all(self):
        """Executa todos os agentes"""
        print("🚀 Iniciando execução de todos os agentes...")
        print(f"⏰ Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

        self.run_profile_update()
        self.run_projects_analysis()
        self.run_engagement_analysis()
        self.run_insights_generation()

        print("\n✨ Execução completa de todos os agentes!")
        print("📁 Arquivos gerados:")
        print("  - README.md (atualizado)")
        print("  - PORTFOLIO.md")
        print("  - PROJECTS_HEALTH.md")
        print("  - ENGAGEMENT_REPORT.md")
        print("  - WEEKLY_SUMMARY.md")
        print("  - INSIGHTS_DASHBOARD.md")

    def interactive_menu(self):
        """Menu interativo"""
        while True:
            print("\n" + "=" * 60)
            print("🤖 Sistema de Agentes Inteligentes para GitHub")
            print("=" * 60)
            print("\nEscolha uma opção:")
            print("1. 🎨 Atualizar Perfil (README)")
            print("2. 📂 Analisar Projetos")
            print("3. 📝 Gerar Documentação")
            print("4. 🤝 Análise de Engajamento")
            print("5. 📊 Gerar Insights")
            print("6. 🔍 Verificar Qualidade")
            print("7. 🚀 Executar Todos os Agentes")
            print("0. ❌ Sair")
            print("\n" + "=" * 60)

            choice = input("\nDigite sua escolha: ").strip()

            if choice == '0':
                print("\n👋 Até logo!")
                break
            elif choice == '1':
                self.run_profile_update()
            elif choice == '2':
                self.run_projects_analysis()
            elif choice == '3':
                repo = input("Digite o nome do repositório: ").strip()
                self.run_documentation_check(repo if repo else None)
            elif choice == '4':
                self.run_engagement_analysis()
            elif choice == '5':
                self.run_insights_generation()
            elif choice == '6':
                repo = input("Digite o nome do repositório: ").strip()
                self.run_quality_check(repo if repo else None)
            elif choice == '7':
                self.run_all()
            else:
                print("❌ Opção inválida!")

            input("\nPressione ENTER para continuar...")


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description='Sistema de Agentes Inteligentes para GitHub Profile'
    )
    parser.add_argument(
        '--agent',
        choices=['profile', 'projects', 'docs', 'engagement', 'insights', 'quality', 'all'],
        help='Agente específico para executar'
    )
    parser.add_argument(
        '--repo',
        help='Nome do repositório (para docs e quality)'
    )
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Modo interativo'
    )
    parser.add_argument(
        '--config',
        default='config/agents_config.json',
        help='Caminho para arquivo de configuração'
    )

    args = parser.parse_args()

    # Verifica se existe token do GitHub
    if not os.getenv('GITHUB_TOKEN'):
        print("⚠️  AVISO: Variável de ambiente GITHUB_TOKEN não encontrada")
        print("   Algumas funcionalidades podem ter limitações de rate limit")
        print("   Configure: export GITHUB_TOKEN=seu_token_aqui\n")

    # Inicializa orquestrador
    orchestrator = AgentOrchestrator(args.config)

    # Modo interativo
    if args.interactive:
        orchestrator.interactive_menu()
        return

    # Modo CLI
    if args.agent == 'profile':
        orchestrator.run_profile_update()
    elif args.agent == 'projects':
        orchestrator.run_projects_analysis()
    elif args.agent == 'docs':
        orchestrator.run_documentation_check(args.repo)
    elif args.agent == 'engagement':
        orchestrator.run_engagement_analysis()
    elif args.agent == 'insights':
        orchestrator.run_insights_generation()
    elif args.agent == 'quality':
        orchestrator.run_quality_check(args.repo)
    elif args.agent == 'all':
        orchestrator.run_all()
    else:
        # Se nenhum agente especificado, mostra menu
        orchestrator.interactive_menu()


if __name__ == '__main__':
    main()
