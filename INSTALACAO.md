# 🔧 Guia de Instalação Completo

## ⚠️ Pré-requisito: Instalar Python

Você precisa instalar o Python primeiro para executar os agentes.

### Windows

**Opção 1: Instalador Oficial (Recomendado)**

1. Acesse: https://www.python.org/downloads/
2. Baixe a versão mais recente do Python (3.8 ou superior)
3. Execute o instalador
4. ⚠️ **IMPORTANTE**: Marque a opção "Add Python to PATH"
5. Clique em "Install Now"

**Opção 2: Microsoft Store**

1. Abra a Microsoft Store
2. Busque por "Python 3.11" (ou versão mais recente)
3. Clique em "Instalar"

### Verificar Instalação

Abra o PowerShell ou CMD e execute:

```bash
python --version
# Deve mostrar: Python 3.x.x
```

Se aparecer "Python não foi encontrado", reinicie o terminal após a instalação.

---

## 📦 Instalar Dependências do Projeto

Depois de instalar o Python:

```bash
# Navegue até a pasta do projeto
cd "E:\Todos os projetos\git profile\krisalexandre2018"

# Instale as dependências
pip install -r requirements.txt
```

---

## 🔑 Configurar Token do GitHub

### Opção 1: Variável de Ambiente (Recomendado)

**PowerShell:**
```powershell
$env:GITHUB_TOKEN="SEU_TOKEN_AQUI"
```

**CMD:**
```cmd
set GITHUB_TOKEN=SEU_TOKEN_AQUI
```

### Opção 2: Configuração Permanente

**Windows:**
1. Pressione `Win + X` e escolha "Sistema"
2. Clique em "Configurações avançadas do sistema"
3. Clique em "Variáveis de Ambiente"
4. Em "Variáveis do usuário", clique em "Novo"
5. Nome: `GITHUB_TOKEN`
6. Valor: `SEU_TOKEN_AQUI`
7. Clique em OK
8. Reinicie o terminal

---

## 🚀 Executar os Agentes

### Modo Interativo (Mais Fácil)

```bash
python main.py --interactive
```

Você verá um menu com opções:

```
1. 🎨 Atualizar Perfil (README)
2. 📂 Analisar Projetos
3. 📝 Gerar Documentação
4. 🤝 Análise de Engajamento
5. 📊 Gerar Insights
6. 🔍 Verificar Qualidade
7. 🚀 Executar Todos os Agentes
0. ❌ Sair
```

### Comandos Diretos

```bash
# Atualizar perfil
python main.py --agent profile

# Analisar projetos
python main.py --agent projects

# Gerar todos os relatórios
python main.py --agent all
```

---

## ✅ Testar Instalação

Execute este comando para testar:

```bash
python main.py --agent profile
```

Se funcionar, você verá:
```
🎨 Executando Agente de Perfil...
✅ Perfil atualizado com sucesso!
```

---

## 🐛 Problemas Comuns

### "python não é reconhecido"

**Solução**: Python não está no PATH
1. Reinstale o Python marcando "Add to PATH"
2. Ou adicione manualmente:
   - Encontre onde o Python está instalado (ex: `C:\Python311`)
   - Adicione às variáveis de ambiente PATH

### "No module named 'requests'"

**Solução**: Instale as dependências
```bash
pip install requests
```

### "API rate limit exceeded"

**Solução**: Configure o token do GitHub
```bash
set GITHUB_TOKEN=seu_token_aqui
```

### "Permission denied"

**Solução**: Execute o PowerShell/CMD como Administrador

---

## 📚 Próximos Passos

Após a instalação:

1. ✅ Execute `python main.py --interactive`
2. ✅ Escolha opção 1 para atualizar seu perfil
3. ✅ Explore os outros agentes
4. ✅ Configure os workflows do GitHub Actions (já estão prontos!)

---

## 🆘 Precisa de Ajuda?

- Leia: `QUICKSTART.md`
- Documentação completa: `AGENTS_README.md`
- Exemplos: `example_usage.py`

---

## 📝 Resumo Rápido

```bash
# 1. Instalar Python
# Baixe de: https://www.python.org/downloads/

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Configurar token
set GITHUB_TOKEN=SEU_TOKEN_AQUI

# 4. Executar
python main.py --interactive

# 5. Escolher opção 1 (Atualizar Perfil)
```

Pronto! 🎉
