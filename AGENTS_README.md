# 🤖 Sistema de Agentes Inteligentes para GitHub

Sistema completo de agentes inteligentes para gerenciar, analisar e otimizar seu perfil do GitHub automaticamente.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Agentes Disponíveis](#agentes-disponíveis)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
- [Automação](#automação)
- [Exemplos](#exemplos)
- [Troubleshooting](#troubleshooting)

## 🎯 Visão Geral

Este sistema é composto por 6 agentes especializados que trabalham juntos para:

- ✨ Manter seu perfil sempre atualizado e profissional
- 📊 Gerar relatórios e insights sobre suas atividades
- 📝 Garantir documentação de qualidade em todos os projetos
- 🤝 Aumentar seu engajamento na comunidade
- 🔍 Monitorar qualidade de código
- 🎨 Criar conteúdo visual atraente

## 🤖 Agentes Disponíveis

### 1. 🎨 Agente de Perfil (Bio & Branding)

**Responsabilidade**: Gerenciar e atualizar o README do perfil

**Funcionalidades**:
- Gera bio personalizada em PT-BR e EN
- Adiciona badges de tecnologias automaticamente
- Atualiza estatísticas do GitHub
- Integra animação da cobra de contribuições
- Mantém informações de contato atualizadas

**Como usar**:
```bash
python main.py --agent profile
```

**Arquivos gerados**:
- `README.md` - Perfil atualizado

---

### 2. 📂 Agente de Projetos (Curadoria e Destaque)

**Responsabilidade**: Organizar e destacar seus melhores projetos

**Funcionalidades**:
- Calcula score de relevância dos repositórios
- Cria cards visuais para projetos em destaque
- Gera portfólio completo
- Sugere melhorias em descrições
- Analisa saúde dos repositórios

**Como usar**:
```bash
python main.py --agent projects
```

**Arquivos gerados**:
- `PORTFOLIO.md` - Portfólio completo
- `PROJECTS_HEALTH.md` - Relatório de saúde dos projetos

---

### 3. 📝 Agente de Documentação

**Responsabilidade**: Garantir documentação profissional em todos os projetos

**Funcionalidades**:
- Gera README.md completo para projetos
- Cria CHANGELOG.md automático
- Gera guia de contribuição (CONTRIBUTING.md)
- Traduz documentação para inglês
- Detecta tipo de projeto e adapta template

**Como usar**:
```bash
python main.py --agent docs --repo nome-do-repositorio
```

**Arquivos gerados**:
- `README.md` - Documentação principal
- `README.en.md` - Versão em inglês
- `CHANGELOG.md` - Histórico de mudanças
- `CONTRIBUTING.md` - Guia de contribuição

---

### 4. 🤝 Agente de Engajamento (Social Dev)

**Responsabilidade**: Aumentar engajamento e visibilidade

**Funcionalidades**:
- Analisa atividade recente (commits, PRs, issues)
- Gera posts para LinkedIn
- Cria resumo semanal de conquistas
- Sugere repositórios para contribuir
- Identifica tendências e oportunidades

**Como usar**:
```bash
python main.py --agent engagement
```

**Arquivos gerados**:
- `ENGAGEMENT_REPORT.md` - Relatório completo de engajamento
- `WEEKLY_SUMMARY.md` - Resumo semanal

---

### 5. 📊 Agente de Insights (Analytics & Feedback)

**Responsabilidade**: Monitorar desempenho e gerar analytics

**Funcionalidades**:
- Calcula métricas totais (stars, forks, etc)
- Rastreia crescimento de repositórios
- Compara com comunidade
- Gera relatórios semanais
- Sugere áreas de foco

**Como usar**:
```bash
python main.py --agent insights
```

**Arquivos gerados**:
- `INSIGHTS_DASHBOARD.md` - Dashboard completo de insights

---

### 6. 🔍 Agente de Código e Qualidade

**Responsabilidade**: Revisar código e garantir qualidade

**Funcionalidades**:
- Analisa estrutura de repositórios
- Verifica presença de arquivos importantes
- Gera .gitignore apropriado
- Cria workflows de CI/CD
- Sugere melhorias de código

**Como usar**:
```bash
python main.py --agent quality --repo nome-do-repositorio
```

**Arquivos gerados**:
- `QUALITY_REPORT_{repo}.md` - Relatório de qualidade
- `.gitignore` - Arquivo de exclusões
- `.github/workflows/ci.yml` - Workflow de CI/CD

## 📦 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- Git
- Conta no GitHub
- Token de acesso pessoal do GitHub (opcional, mas recomendado)

### Passo a Passo

1. **Clone o repositório**:
```bash
git clone https://github.com/krisalexandre2018/krisalexandre2018.git
cd krisalexandre2018
```

2. **Instale as dependências**:
```bash
pip install requests
```

3. **Configure o token do GitHub** (opcional mas recomendado):
```bash
# Windows (PowerShell)
$env:GITHUB_TOKEN="seu_token_aqui"

# Linux/Mac
export GITHUB_TOKEN="seu_token_aqui"
```

Para criar um token:
1. Vá em GitHub → Settings → Developer settings → Personal access tokens
2. Clique em "Generate new token (classic)"
3. Selecione os escopos: `repo`, `read:user`, `user:email`
4. Gere e copie o token

## ⚙️ Configuração

Edite o arquivo `config/agents_config.json` com suas informações:

```json
{
  "github": {
    "username": "seu-usuario",
    "token": "${GITHUB_TOKEN}"
  },
  "profile": {
    "language": "pt-br",
    "custom_info": {
      "work_focus": "suas tecnologias",
      "learning": "o que está aprendendo",
      ...
    },
    "technologies": ["Python", "JavaScript", ...],
    "linkedin_url": "seu-linkedin"
  }
}
```

## 🚀 Uso

### Modo Interativo (Recomendado)

Execute o menu interativo:

```bash
python main.py --interactive
```

Você verá um menu como este:

```
🤖 Sistema de Agentes Inteligentes para GitHub
============================================================

Escolha uma opção:
1. 🎨 Atualizar Perfil (README)
2. 📂 Analisar Projetos
3. 📝 Gerar Documentação
4. 🤝 Análise de Engajamento
5. 📊 Gerar Insights
6. 🔍 Verificar Qualidade
7. 🚀 Executar Todos os Agentes
0. ❌ Sair
```

### Modo CLI

Execute agentes específicos via linha de comando:

```bash
# Atualizar perfil
python main.py --agent profile

# Analisar projetos
python main.py --agent projects

# Gerar documentação para um repo
python main.py --agent docs --repo meu-projeto

# Análise de engajamento
python main.py --agent engagement

# Gerar insights
python main.py --agent insights

# Verificar qualidade
python main.py --agent quality --repo meu-projeto

# Executar todos os agentes
python main.py --agent all
```

## 🔄 Automação

O sistema inclui 3 workflows do GitHub Actions para automação:

### 1. Update Profile (update_profile.yml)

**Executa**: Toda segunda-feira às 9h UTC

**Ações**:
- Atualiza README do perfil
- Gera portfólio
- Cria relatórios de engajamento e insights
- Commita mudanças automaticamente

### 2. Weekly Report (weekly_report.yml)

**Executa**: Todo domingo às 20h UTC

**Ações**:
- Gera relatório semanal
- Cria issue com resumo da semana
- Salva reports como artifacts

### 3. Quality Check (quality_check.yml)

**Executa**: Em Pull Requests

**Ações**:
- Verifica qualidade do código
- Comenta PR com sugestões

### Ativar Automação

1. Os workflows já estão configurados em `.github/workflows/`
2. Certifique-se de que o repositório tem permissões para executar Actions
3. (Opcional) Ajuste os horários de execução nos arquivos `.yml`

## 💡 Exemplos

### Exemplo 1: Atualizar Perfil Completo

```bash
# Modo interativo
python main.py --interactive
# Escolha opção 7 (Executar Todos)

# Ou via CLI
python main.py --agent all
```

**Resultado**: README atualizado + 5 relatórios gerados

---

### Exemplo 2: Criar Documentação para Novo Projeto

```bash
python main.py --agent docs --repo meu-novo-projeto
```

**Resultado**: README.md, CHANGELOG.md, CONTRIBUTING.md criados na pasta `./docs`

---

### Exemplo 3: Verificar Saúde dos Projetos

```bash
python main.py --agent projects
```

**Resultado**:
- `PORTFOLIO.md` com projetos em destaque
- `PROJECTS_HEALTH.md` com análise e sugestões

---

### Exemplo 4: Gerar Conteúdo para LinkedIn

```bash
python main.py --agent engagement
```

**Resultado**: `ENGAGEMENT_REPORT.md` com texto pronto para post no LinkedIn

## 🛠️ Troubleshooting

### Erro: "API rate limit exceeded"

**Solução**: Configure o token do GitHub:
```bash
export GITHUB_TOKEN="seu_token"
```

### Erro: "Repository not found"

**Solução**: Verifique se o nome do repositório está correto e é público

### Erro: "Permission denied"

**Solução**: Verifique as permissões do token:
- Precisa ter acesso a `repo`, `read:user`, `user:email`

### Workflows não executam

**Soluções**:
1. Verifique se Actions está habilitado: Settings → Actions → Allow all actions
2. Certifique-se de que há permissões de escrita: Settings → Actions → Workflow permissions → Read and write permissions

### Caracteres especiais no arquivo gerado

**Solução**: Os arquivos são gerados em UTF-8. Use um editor que suporte UTF-8.

## 📚 Estrutura do Projeto

```
krisalexandre2018/
├── agents/                    # Código dos agentes
│   ├── profile/              # Agente de Perfil
│   ├── projects/             # Agente de Projetos
│   ├── documentation/        # Agente de Documentação
│   ├── engagement/           # Agente de Engajamento
│   ├── insights/             # Agente de Insights
│   └── quality/              # Agente de Qualidade
├── config/                    # Configurações
│   └── agents_config.json    # Configuração principal
├── .github/                   # GitHub Actions
│   └── workflows/            # Workflows de automação
├── main.py                   # Orquestrador principal
├── README.md                 # Perfil do GitHub
└── AGENTS_README.md          # Esta documentação
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 📧 Suporte

- **Issues**: [GitHub Issues](https://github.com/krisalexandre2018/krisalexandre2018/issues)
- **Discussões**: [GitHub Discussions](https://github.com/krisalexandre2018/krisalexandre2018/discussions)

---

⭐ Se este projeto foi útil, considere dar uma estrela!

🤖 **Feito com agentes inteligentes**
