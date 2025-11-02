"""
Exemplos de uso dos agentes
Este arquivo demonstra como usar cada agente programaticamente
"""

import os
from agents import (
    ProfileAgent,
    ProjectsAgent,
    DocumentationAgent,
    EngagementAgent,
    InsightsAgent,
    QualityAgent
)

# Configure seu token do GitHub (opcional mas recomendado)
# os.environ['GITHUB_TOKEN'] = 'seu_token_aqui'

USERNAME = 'krisalexandre2018'


def exemplo_profile_agent():
    """Exemplo: Atualizar perfil do GitHub"""
    print("\n" + "="*60)
    print("📝 Exemplo: Profile Agent")
    print("="*60)

    agent = ProfileAgent(USERNAME)

    # Configuração personalizada
    config = {
        'language': 'pt-br',
        'custom_info': {
            'work_focus': 'HTML5, CSS3 e JavaScript',
            'learning': 'Python, PHP, React',
            'collaboration': 'desenvolvimento web',
            'pronouns': 'ele/dele'
        },
        'technologies': ['HTML5', 'CSS3', 'JavaScript', 'Python'],
        'linkedin_url': 'https://linkedin.com/in/seu-perfil',
        'include_stats': True,
        'include_snake': True
    }

    # Atualiza README
    agent.update_readme(config, readme_path='README_EXEMPLO.md')
    print("✅ README_EXEMPLO.md criado!")


def exemplo_projects_agent():
    """Exemplo: Analisar projetos"""
    print("\n" + "="*60)
    print("📂 Exemplo: Projects Agent")
    print("="*60)

    agent = ProjectsAgent(USERNAME)

    # Obtém top projetos
    top_repos = agent.get_top_repos(limit=5)
    print(f"\n🌟 Top 5 Projetos:")
    for i, repo in enumerate(top_repos, 1):
        print(f"{i}. {repo['name']} - ⭐ {repo['stargazers_count']} stars")

    # Gera portfólio
    agent.generate_portfolio_page('PORTFOLIO_EXEMPLO.md')
    print("\n✅ PORTFOLIO_EXEMPLO.md criado!")

    # Análise de saúde
    report = agent.generate_health_report()
    print("\n📊 Relatório de Saúde:")
    print(report[:500] + "...")


def exemplo_documentation_agent():
    """Exemplo: Gerar documentação"""
    print("\n" + "="*60)
    print("📝 Exemplo: Documentation Agent")
    print("="*60)

    agent = DocumentationAgent(USERNAME)

    # Gera README template
    readme = agent.generate_readme_template('meu-projeto-exemplo')
    print("\n📄 Preview do README gerado:")
    print(readme[:300] + "...")

    # Gera CHANGELOG
    changelog = agent.generate_changelog_template()
    print("\n📅 Preview do CHANGELOG:")
    print(changelog[:200] + "...")


def exemplo_engagement_agent():
    """Exemplo: Análise de engajamento"""
    print("\n" + "="*60)
    print("🤝 Exemplo: Engagement Agent")
    print("="*60)

    agent = EngagementAgent(USERNAME)

    # Analisa atividade
    activity = agent.analyze_activity(days=30)
    print(f"\n📊 Atividade nos últimos 30 dias:")
    print(f"- Commits: {activity['commits']}")
    print(f"- Pull Requests: {activity['pull_requests']}")
    print(f"- Issues abertas: {activity['issues_opened']}")
    print(f"- Dias ativos: {activity['active_days_count']}")

    # Gera post para LinkedIn
    linkedin_post = agent.generate_linkedin_post(activity)
    print("\n💼 Post sugerido para LinkedIn:")
    print(linkedin_post)


def exemplo_insights_agent():
    """Exemplo: Gerar insights"""
    print("\n" + "="*60)
    print("📊 Exemplo: Insights Agent")
    print("="*60)

    agent = InsightsAgent(USERNAME)

    # Calcula métricas totais
    metrics = agent.calculate_total_metrics()
    print(f"\n📈 Métricas Totais:")
    print(f"- Repositórios: {metrics['total_repos']}")
    print(f"- Total de estrelas: {metrics['total_stars']}")
    print(f"- Média de estrelas: {metrics['avg_stars_per_repo']}")
    print(f"- Total de forks: {metrics['total_forks']}")

    # Top linguagens
    if metrics['languages']:
        print(f"\n💻 Top 3 Linguagens:")
        for lang, count in metrics['languages'].most_common(3):
            print(f"- {lang}: {count} repos")

    # Sugestões de foco
    suggestions = agent.suggest_focus_areas()
    print(f"\n💡 Sugestões de Foco:")
    for suggestion in suggestions[:3]:
        print(f"- {suggestion}")


def exemplo_quality_agent():
    """Exemplo: Verificar qualidade"""
    print("\n" + "="*60)
    print("🔍 Exemplo: Quality Agent")
    print("="*60)

    agent = QualityAgent(USERNAME)

    # Gera .gitignore
    gitignore = agent.suggest_gitignore('python')
    print("\n📄 .gitignore sugerido para Python:")
    print(gitignore[:200] + "...")

    # Gera workflow de CI/CD
    workflow = agent.suggest_github_actions_workflow('python')
    print("\n⚙️ GitHub Actions workflow sugerido:")
    print(workflow[:300] + "...")

    # Template de revisão de PR
    pr_template = agent.generate_pr_review_template()
    print("\n✅ Template de revisão de PR:")
    print(pr_template[:300] + "...")


def exemplo_completo():
    """Exemplo: Usar múltiplos agentes juntos"""
    print("\n" + "="*60)
    print("🚀 Exemplo: Workflow Completo")
    print("="*60)

    # 1. Atualiza perfil
    print("\n1️⃣ Atualizando perfil...")
    profile = ProfileAgent(USERNAME)
    # profile.update_readme(config)

    # 2. Analisa projetos
    print("2️⃣ Analisando projetos...")
    projects = ProjectsAgent(USERNAME)
    top_repos = projects.get_top_repos(limit=3)
    print(f"   Top projeto: {top_repos[0]['name'] if top_repos else 'N/A'}")

    # 3. Verifica engajamento
    print("3️⃣ Verificando engajamento...")
    engagement = EngagementAgent(USERNAME)
    activity = engagement.analyze_activity(days=7)
    print(f"   Commits esta semana: {activity['commits']}")

    # 4. Gera insights
    print("4️⃣ Gerando insights...")
    insights = InsightsAgent(USERNAME)
    metrics = insights.calculate_total_metrics()
    print(f"   Total de estrelas: {metrics['total_stars']}")

    print("\n✅ Workflow completo executado!")


def menu():
    """Menu interativo de exemplos"""
    while True:
        print("\n" + "="*60)
        print("🎯 Exemplos de Uso dos Agentes")
        print("="*60)
        print("\n1. Profile Agent - Atualizar perfil")
        print("2. Projects Agent - Analisar projetos")
        print("3. Documentation Agent - Gerar documentação")
        print("4. Engagement Agent - Análise de engajamento")
        print("5. Insights Agent - Gerar insights")
        print("6. Quality Agent - Verificar qualidade")
        print("7. Workflow Completo - Todos os agentes")
        print("0. Sair")

        choice = input("\nEscolha um exemplo (0-7): ").strip()

        try:
            if choice == '0':
                print("\n👋 Até logo!")
                break
            elif choice == '1':
                exemplo_profile_agent()
            elif choice == '2':
                exemplo_projects_agent()
            elif choice == '3':
                exemplo_documentation_agent()
            elif choice == '4':
                exemplo_engagement_agent()
            elif choice == '5':
                exemplo_insights_agent()
            elif choice == '6':
                exemplo_quality_agent()
            elif choice == '7':
                exemplo_completo()
            else:
                print("❌ Opção inválida!")
        except Exception as e:
            print(f"\n❌ Erro ao executar exemplo: {e}")
            print("   Certifique-se de que o token do GitHub está configurado se necessário")

        input("\nPressione ENTER para continuar...")


if __name__ == '__main__':
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║       🤖 Exemplos de Uso - Sistema de Agentes              ║
║                                                              ║
║  Este script demonstra como usar cada agente               ║
║  programaticamente em seus próprios scripts.                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)

    # Verifica token
    if not os.getenv('GITHUB_TOKEN'):
        print("⚠️  AVISO: GITHUB_TOKEN não configurado")
        print("   Alguns exemplos podem ter limitações de rate limit")
        print("   Configure: export GITHUB_TOKEN='seu_token'\n")

    menu()
