# Guia de Automação - Dashboard de Retorno

## 📋 Sobre

Este guia explica como configurar a atualização automática diária dos dados do dashboard.

## 🔧 Arquivos de Automação

- `atualizar_dashboard.py` - Script Python que copia arquivos e faz push para GitHub
- `atualizar_dashboard.bat` - Script batch para executar facilmente

## 🚀 Como Funciona

O script automaticamente:
1. ✅ Copia `historico_envios.json` da pasta pai
2. ✅ Copia `Vendas_Lubrimax.xlsx` da pasta pai
3. ✅ Faz commit das alterações no Git
4. ✅ Faz push para o GitHub
5. ✅ O Streamlit Cloud detecta e atualiza automaticamente

## 🧪 Testar Manualmente

Antes de agendar, teste se funciona:

```powershell
cd "c:\Projetos\Lubrimax\Dashboard_Retorno"
python atualizar_dashboard.py
```

Ou simplesmente clique duas vezes em `atualizar_dashboard.bat`

## ⏰ Agendar Execução Diária (Windows Task Scheduler)

### Passo 1: Abrir Agendador de Tarefas

1. Pressione `Win + R`
2. Digite: `taskschd.msc`
3. Pressione Enter

### Passo 2: Criar Nova Tarefa

1. No painel direito, clique em **"Criar Tarefa..."**
2. Na aba **Geral**:
   - Nome: `Dashboard Lubrimax - Atualização Diária`
   - Descrição: `Atualiza dados do dashboard de retorno diariamente`
   - Marque: **"Executar estando o usuário conectado ou não"**
   - Configure para: **Windows 10**

### Passo 3: Configurar Gatilho (Horário)

1. Vá para aba **Disparadores**
2. Clique em **"Novo..."**
3. Configure:
   - Iniciar a tarefa: **Diariamente**
   - Iniciar em: (data de hoje)
   - Horário: **05:00:00** (ou horário de sua preferência)
   - Recorrer a cada: **1 dias**
   - Marque: **"Habilitada"**
4. Clique em **OK**

### Passo 4: Configurar Ação

1. Vá para aba **Ações**
2. Clique em **"Novo..."**
3. Configure:
   - Ação: **Iniciar um programa**
   - Programa/script: 
     ```
     C:\Projetos\Lubrimax\Dashboard_Retorno\atualizar_dashboard.bat
     ```
   - Iniciar em (opcional):
     ```
     C:\Projetos\Lubrimax\Dashboard_Retorno
     ```
4. Clique em **OK**

### Passo 5: Configurações Adicionais

1. Vá para aba **Condições**:
   - Desmarque: **"Iniciar tarefa apenas se o computador estiver conectado à energia CA"**
   - Marque: **"Ativar tarefa quando houver conexão de rede"**

2. Vá para aba **Configurações**:
   - Marque: **"Permitir que a tarefa seja executada sob demanda"**
   - Marque: **"Executar tarefa assim que possível após perda de agendamento"**
   - Se a tarefa falhar, reiniciar a cada: **10 minutos**

3. Clique em **OK**

### Passo 6: Testar Agendamento

1. Na lista de tarefas, encontre sua tarefa
2. Clique com botão direito → **"Executar"**
3. Verifique se executou com sucesso
4. Verifique no GitHub se houve novo commit

## 📊 Verificar Execução

Para ver se a tarefa executou:

1. Abra o Agendador de Tarefas
2. Encontre sua tarefa
3. Verifique a coluna **"Última Execução"** e **"Resultado da Última Execução"**
4. Código 0x0 = Sucesso ✅

## 🔍 Logs

Os logs aparecem durante a execução do script. Para salvar logs permanentes, modifique o arquivo `.bat`:

```batch
python atualizar_dashboard.py >> logs\atualizacao_%date:~-4,4%%date:~-7,2%%date:~-10,2%.log 2>&1
```

## 🛠️ Troubleshooting

### Erro de autenticação Git

Se der erro de autenticação, configure credenciais:

```powershell
cd "c:\Projetos\Lubrimax\Dashboard_Retorno"
git config credential.helper store
git push
# Digite usuário e senha quando solicitado (só precisa uma vez)
```

### Tarefa não executa

1. Verifique se o caminho dos arquivos está correto
2. Teste manualmente antes: `atualizar_dashboard.bat`
3. Veja os logs no Agendador de Tarefas

## 🎯 Horários Recomendados

- **05:00** - Antes do expediente
- **23:00** - Fim do dia após todas as vendas
- **A cada 6 horas** - Para atualizações mais frequentes

## ⚠️ Importante

- Certifique-se de que o PC esteja ligado no horário agendado
- Mantenha conexão com internet
- Certifique-se de que o Git está autenticado
