# CLAUDE.md

Este arquivo fornece orientações ao Claude Code (claude.ai/code) ao trabalhar com código neste repositório.

## Visão Geral do Repositório

Este é um repositório de perfil do GitHub (krisalexandre2018/krisalexandre2018) que é exibido na página de perfil do usuário. O repositório contém:

- **README.md**: Conteúdo da página de perfil em português, apresentando habilidades, tecnologias, estatísticas do GitHub e informações de contato
- **Sistema de Agentes Inteligentes**: 6 agentes Python que automatizam gerenciamento do perfil, análise de projetos, documentação, engajamento, insights e qualidade de código
- **GitHub Actions workflows**: Automação de atualização de perfil, relatórios semanais, verificação de qualidade e animação de cobra de contribuições

## Componentes Principais

### Estrutura do README.md
O README do perfil segue este layout:
1. Introdução e seção "Sobre mim" em português
2. Cards de estatísticas do GitHub (stats e linguagens mais usadas)
3. Animação de cobra das contribuições
4. Badges de tecnologias (HTML5, CSS3, JavaScript, Python, React, Power BI, Excel)
5. Links de contato (GitHub, LinkedIn)
6. Contador de visualizações do perfil

### Sistema de Agentes Inteligentes

O repositório contém 6 agentes Python especializados:

1. **ProfileAgent** (`agents/profile/`) - Gerencia bio e branding do perfil
2. **ProjectsAgent** (`agents/projects/`) - Curadoria e destaque de projetos
3. **DocumentationAgent** (`agents/documentation/`) - Gera documentação profissional
4. **EngagementAgent** (`agents/engagement/`) - Análise de engajamento social
5. **InsightsAgent** (`agents/insights/`) - Analytics e feedback de desempenho
6. **QualityAgent** (`agents/quality/`) - Revisão de código e qualidade

**Orquestração**: O arquivo `main.py` coordena todos os agentes
**Configuração**: `config/agents_config.json` contém todas as configurações
**Documentação completa**: Veja `AGENTS_README.md` e `QUICKSTART.md`

### GitHub Actions Workflows

#### 1. Snake Animation (.github/workflows/snake.yml)
- **Propósito**: Gera cobra animada em SVG das contribuições
- **Agendamento**: A cada 12 horas (`0 */12 * * *`)
- **Saída**: Branch `output`

#### 2. Update Profile (.github/workflows/update_profile.yml)
- **Propósito**: Atualiza perfil e gera relatórios automaticamente
- **Agendamento**: Toda segunda-feira às 9h UTC
- **Executa**: Agentes de Profile, Projects, Engagement e Insights

#### 3. Weekly Report (.github/workflows/weekly_report.yml)
- **Propósito**: Gera relatório semanal e cria issue
- **Agendamento**: Todo domingo às 20h UTC

#### 4. Quality Check (.github/workflows/quality_check.yml)
- **Propósito**: Verifica qualidade em Pull Requests
- **Trigger**: Em PRs para main/develop

## Tarefas Comuns

### Executar Sistema de Agentes

```bash
# Modo interativo (recomendado)
python main.py --interactive

# Atualizar perfil
python main.py --agent profile

# Executar todos os agentes
python main.py --agent all

# Gerar documentação para um repo
python main.py --agent docs --repo nome-do-repo

# Verificar qualidade de um repo
python main.py --agent quality --repo nome-do-repo
```

### Configurar Agentes

Edite `config/agents_config.json` para personalizar:
- Informações de perfil (bio, tecnologias, links)
- Configurações dos agentes
- Frequência de automação

### Testar Workflows

```bash
# Disparar workflow de atualização de perfil
gh workflow run update_profile.yml

# Disparar workflow de relatório semanal
gh workflow run weekly_report.yml

# Disparar workflow da cobra
gh workflow run snake.yml

# Ver status dos workflows
gh run list

# Ver logs de um workflow
gh run view --log
```

### Atualizar Conteúdo do Perfil Manualmente

Edite o README.md diretamente ou use o ProfileAgent:
```bash
python main.py --agent profile
```

## Notas Importantes

### Geral
- Todo o conteúdo está em português (pt-BR)
- O nome de usuário está codificado em vários lugares: `krisalexandre2018`
- Requer Python 3.8+ e a biblioteca `requests`

### Sistema de Agentes
- **Token GitHub**: Configure `GITHUB_TOKEN` como variável de ambiente para evitar rate limits
- **Configuração**: Todas as configurações estão em `config/agents_config.json`
- **Relatórios**: Os agentes geram arquivos `.md` que podem ser commitados ou ignorados (ver `.gitignore`)
- **Automação**: Os workflows executam automaticamente, mas podem ser disparados manualmente

### APIs e Serviços Externos
- **github-readme-stats.vercel.app**: Gera cards de estatísticas
- **komarev.com**: Contador de visualizações do perfil
- **GitHub API**: Usada por todos os agentes (rate limit: 60 req/hora sem token, 5000 com token)

### Estrutura de Arquivos
```
krisalexandre2018/
├── agents/              # Código dos 6 agentes
├── config/              # Configurações
├── .github/workflows/   # Automação
├── main.py             # Orquestrador
├── README.md           # Perfil (gerado/atualizado pelos agentes)
├── AGENTS_README.md    # Documentação completa dos agentes
└── QUICKSTART.md       # Guia rápido
```

### Desenvolvimento
- Para modificar agentes: edite arquivos em `agents/{nome_agente}/`
- Para adicionar novos agentes: crie pasta em `agents/` e adicione em `main.py`
- Para ajustar automação: edite workflows em `.github/workflows/`
