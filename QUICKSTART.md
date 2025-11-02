# 🚀 Quick Start - Sistema de Agentes

Guia rápido para começar a usar os agentes em 5 minutos!

## ⚡ Instalação Rápida

```bash
# 1. Clone o repositório
git clone https://github.com/krisalexandre2018/krisalexandre2018.git
cd krisalexandre2018

# 2. Instale dependências
pip install -r requirements.txt

# 3. Configure seu token do GitHub (opcional)
export GITHUB_TOKEN="seu_token_aqui"

# 4. Execute!
python main.py --interactive
```

## 🎯 Uso Rápido

### Atualizar Perfil Agora

```bash
python main.py --agent profile
```

Resultado: Seu `README.md` será atualizado com as informações mais recentes!

### Gerar Todos os Relatórios

```bash
python main.py --agent all
```

Resultado: 6 arquivos criados com análises completas!

### Menu Interativo

```bash
python main.py --interactive
```

Navegue pelo menu e escolha o que deseja fazer.

## ⚙️ Configuração Básica

Edite `config/agents_config.json` e altere:

```json
{
  "github": {
    "username": "SEU-USUARIO-AQUI"
  },
  "profile": {
    "custom_info": {
      "work_focus": "Suas tecnologias",
      "learning": "O que está aprendendo"
    },
    "technologies": ["Python", "JavaScript"],
    "linkedin_url": "seu-linkedin"
  }
}
```

## 📋 Comandos Úteis

| Comando | O que faz |
|---------|-----------|
| `python main.py --agent profile` | Atualiza README do perfil |
| `python main.py --agent projects` | Analisa seus projetos |
| `python main.py --agent engagement` | Gera relatório de engajamento |
| `python main.py --agent insights` | Cria dashboard de insights |
| `python main.py --agent all` | Executa tudo! |

## 🤔 Dúvidas?

Leia a documentação completa em [AGENTS_README.md](AGENTS_README.md)

## 🎉 Pronto!

Agora você tem um sistema completo de agentes gerenciando seu perfil do GitHub automaticamente!
