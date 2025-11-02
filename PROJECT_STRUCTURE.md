# 📁 Estrutura do Projeto

## 🌳 Árvore de Diretórios

```
krisalexandre2018/
│
├── 📂 agents/                           # Sistema de Agentes Inteligentes
│   ├── 📂 profile/                      # Agente 1: Bio & Branding
│   │   ├── profile_agent.py            # Gerencia README do perfil
│   │   └── __init__.py
│   │
│   ├── 📂 projects/                     # Agente 2: Curadoria de Projetos
│   │   ├── projects_agent.py           # Analisa e destaca projetos
│   │   └── __init__.py
│   │
│   ├── 📂 documentation/                # Agente 3: Documentação
│   │   ├── documentation_agent.py      # Gera docs profissionais
│   │   └── __init__.py
│   │
│   ├── 📂 engagement/                   # Agente 4: Engajamento Social
│   │   ├── engagement_agent.py         # Análise de atividades
│   │   └── __init__.py
│   │
│   ├── 📂 insights/                     # Agente 5: Analytics & Feedback
│   │   ├── insights_agent.py           # Métricas e insights
│   │   └── __init__.py
│   │
│   ├── 📂 quality/                      # Agente 6: Qualidade de Código
│   │   ├── quality_agent.py            # Revisão e sugestões
│   │   └── __init__.py
│   │
│   └── __init__.py                      # Módulo principal dos agentes
│
├── 📂 config/                           # Configurações
│   └── agents_config.json              # Config central (usuário, perfil, etc)
│
├── 📂 .github/                          # GitHub Actions & Workflows
│   └── 📂 workflows/
│       ├── snake.yml                   # Animação da cobra (12h)
│       ├── update_profile.yml          # Atualização automática (segunda 9h)
│       ├── weekly_report.yml           # Relatório semanal (domingo 20h)
│       └── quality_check.yml           # Check de qualidade em PRs
│
├── 📄 main.py                           # 🎯 Orquestrador Principal
├── 📄 example_usage.py                  # Exemplos de uso programático
│
├── 📄 README.md                         # Perfil do GitHub (público)
├── 📄 CLAUDE.md                         # Guia para Claude Code
├── 📄 AGENTS_README.md                  # Documentação completa dos agentes
├── 📄 QUICKSTART.md                     # Guia de início rápido
├── 📄 PROJECT_STRUCTURE.md              # Este arquivo
│
├── 📄 requirements.txt                  # Dependências Python
└── 📄 .gitignore                        # Arquivos ignorados pelo Git
```

## 📊 Arquivos Gerados (pelos agentes)

Estes arquivos são criados automaticamente pelos agentes:

```
📄 PORTFOLIO.md                  # Gerado por ProjectsAgent
📄 PROJECTS_HEALTH.md            # Gerado por ProjectsAgent
📄 ENGAGEMENT_REPORT.md          # Gerado por EngagementAgent
📄 WEEKLY_SUMMARY.md             # Gerado por EngagementAgent
📄 INSIGHTS_DASHBOARD.md         # Gerado por InsightsAgent
📄 QUALITY_REPORT_{repo}.md      # Gerado por QualityAgent
```

## 🔗 Fluxo de Dados

```
┌─────────────────────────────────────────────────────────────────┐
│                         GitHub API                              │
│                    (dados dos repositórios)                     │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    config/agents_config.json                    │
│                  (configurações personalizadas)                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                          main.py                                │
│                 (orquestrador dos agentes)                      │
└────────┬────────┬────────┬────────┬────────┬────────┬──────────┘
         │        │        │        │        │        │
         ▼        ▼        ▼        ▼        ▼        ▼
    ┌────────┬────────┬────────┬────────┬────────┬────────┐
    │Profile │Projects│  Docs  │Engage  │Insights│Quality │
    │ Agent  │ Agent  │ Agent  │ Agent  │ Agent  │ Agent  │
    └────┬───┴────┬───┴────┬───┴────┬───┴────┬───┴────┬───┘
         │        │        │        │        │        │
         ▼        ▼        ▼        ▼        ▼        ▼
    ┌─────────────────────────────────────────────────────┐
    │              Arquivos Gerados (.md)                 │
    │  README, PORTFOLIO, REPORTS, INSIGHTS, etc          │
    └─────────────────────────────────────────────────────┘
                         │
                         ▼
    ┌─────────────────────────────────────────────────────┐
    │            GitHub Actions (automação)               │
    │  Commits automáticos, Issues, Notificações          │
    └─────────────────────────────────────────────────────┘
```

## 🚀 Como Tudo se Conecta

### 1️⃣ Configuração
- Edite `config/agents_config.json` com suas informações
- Configure `GITHUB_TOKEN` (opcional mas recomendado)

### 2️⃣ Execução Manual
- Execute `python main.py --interactive` para menu
- Ou use comandos CLI: `python main.py --agent profile`

### 3️⃣ Execução Automática
- GitHub Actions executam workflows periodicamente
- `update_profile.yml` → Atualiza tudo semanalmente
- `weekly_report.yml` → Cria relatório semanal
- `quality_check.yml` → Verifica qualidade em PRs

### 4️⃣ Resultados
- README atualizado automaticamente
- Relatórios gerados e commitados
- Issues criadas com resumos
- Notificações de atividade

## 📦 Dependências

### Python
- **requests** (≥2.28.0) - Para chamadas à API do GitHub

### APIs Externas (Gratuitas)
- **GitHub API** - Dados de repositórios e atividades
- **github-readme-stats.vercel.app** - Cards de estatísticas
- **komarev.com** - Contador de visualizações

## 🎨 Personalização

### Adicionar Novo Agente

1. Crie pasta em `agents/novo_agente/`
2. Crie `novo_agente.py` com a classe
3. Adicione `__init__.py`
4. Importe em `agents/__init__.py`
5. Adicione em `main.py`

### Modificar Workflow

1. Edite arquivo em `.github/workflows/`
2. Ajuste schedule (cron), steps ou triggers
3. Commit e push

### Personalizar Relatórios

1. Edite o agente correspondente
2. Modifique os métodos de geração de texto
3. Teste com `python main.py --agent {nome}`

## 🔐 Segurança

### Boas Práticas

✅ **FAZER**:
- Usar variáveis de ambiente para tokens
- Manter `.gitignore` atualizado
- Revisar relatórios antes de commitar dados sensíveis
- Limitar permissões do token aos escopos necessários

❌ **NÃO FAZER**:
- Commitar tokens ou senhas
- Expor API keys em código
- Desabilitar workflows de segurança

## 📈 Métricas e Monitoramento

### O que os Agentes Rastreiam

- **Profile**: Atualidade do README, consistência de branding
- **Projects**: Score de relevância, engajamento (stars, forks)
- **Documentation**: Presença de arquivos essenciais
- **Engagement**: Commits, PRs, issues, atividade por dia
- **Insights**: Crescimento, comparação com comunidade
- **Quality**: Estrutura de arquivos, padrões de código

### Onde Ver os Resultados

- **Arquivos `.md`**: Relatórios detalhados no repositório
- **GitHub Actions**: Logs de execução
- **Issues**: Resumos semanais automatizados
- **README**: Perfil sempre atualizado

## 🎓 Aprendizado

### Conceitos Aplicados

- **Design Pattern**: Agent-based architecture
- **Automação**: GitHub Actions CI/CD
- **API Integration**: GitHub REST API
- **Code Quality**: Linting, estrutura, best practices
- **DevOps**: Workflows, scheduling, artifacts
- **Analytics**: Métricas, insights, reporting

### Tecnologias Usadas

- Python 3.8+
- GitHub API v3
- GitHub Actions
- YAML (workflows)
- JSON (configuração)
- Markdown (relatórios)

---

**📚 Documentação Relacionada:**
- [AGENTS_README.md](AGENTS_README.md) - Documentação completa
- [QUICKSTART.md](QUICKSTART.md) - Guia de início rápido
- [CLAUDE.md](CLAUDE.md) - Guia para Claude Code
- [example_usage.py](example_usage.py) - Exemplos de código

**🔗 Links Úteis:**
- [GitHub API Documentation](https://docs.github.com/en/rest)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Python Requests](https://requests.readthedocs.io/)
