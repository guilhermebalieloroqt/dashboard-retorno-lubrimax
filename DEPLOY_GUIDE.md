# Guia de Deploy no Streamlit Cloud

## Passo 1: Criar Repositório no GitHub

1. Acesse [GitHub](https://github.com) e faça login
2. Clique em "New repository" (ou acesse https://github.com/new)
3. Preencha:
   - **Repository name**: `dashboard-retorno-lubrimax`
   - **Description**: Dashboard de análise de retorno de mensagens
   - **Visibility**: Private (recomendado) ou Public
   - **NÃO** marque "Initialize with README" (já temos um)
4. Clique em "Create repository"

## Passo 2: Conectar ao Repositório Remoto

Após criar o repositório, execute no PowerShell (na pasta Dashboard_Retorno):

```powershell
git remote add origin https://github.com/SEU_USUARIO/dashboard-retorno-lubrimax.git
git branch -M main
git push -u origin main
```

**Substitua `SEU_USUARIO` pelo seu usuário do GitHub!**

## Passo 3: Deploy no Streamlit Cloud

1. Acesse [Streamlit Cloud](https://share.streamlit.io/)
2. Faça login com sua conta GitHub
3. Clique em "New app"
4. Selecione:
   - **Repository**: `dashboard-retorno-lubrimax`
   - **Branch**: `main`
   - **Main file path**: `dashboard_retorno.py`
5. Clique em "Deploy!"

## Passo 4: Atualizar os Dados

Para atualizar os dados do dashboard:

```powershell
cd "c:\Projetos\Lubrimax\Dashboard_Retorno"

# Copiar arquivos atualizados
Copy-Item "..\historico_envios.json" -Destination "." -Force
Copy-Item "..\Vendas_Lubrimax.xlsx" -Destination "." -Force

# Fazer commit e push
git add historico_envios.json Vendas_Lubrimax.xlsx
git commit -m "Atualização de dados $(Get-Date -Format 'dd/MM/yyyy')"
git push
```

O Streamlit Cloud irá detectar automaticamente as mudanças e atualizar o dashboard!

## Observações Importantes

⚠️ **ATENÇÃO**: O arquivo `Vendas_Lubrimax.xlsx` contém dados sensíveis. Considere:
- Usar repositório PRIVATE no GitHub
- Ou adicionar `Vendas_Lubrimax.xlsx` ao `.gitignore` e usar Streamlit Secrets para dados sensíveis

## Troubleshooting

Se o deploy falhar:
1. Verifique se todos os pacotes estão no `requirements.txt`
2. Teste localmente: `streamlit run dashboard_retorno.py`
3. Veja os logs no Streamlit Cloud para identificar erros
