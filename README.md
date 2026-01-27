# Dashboard de Retorno - Lubrimax

Dashboard para análise da efetividade das mensagens de lembrete de troca de óleo.

## Funcionalidades

- 📊 Análise de retorno dos clientes após receberem mensagens
- 💰 Cálculo de valor gerado pelas mensagens
- 📈 Gráficos interativos de taxa de conversão
- ⏱️ Análise de tempo médio até o retorno

## Deploy no Streamlit Cloud

1. Faça push deste repositório para o GitHub
2. Acesse [Streamlit Cloud](https://streamlit.io/cloud)
3. Conecte seu repositório GitHub
4. Selecione o arquivo `dashboard_retorno.py`
5. Deploy!

## Como Executar Localmente

```bash
streamlit run dashboard_retorno.py
```

## Arquivos Necessários

- `dashboard_retorno.py` - Aplicação principal
- `historico_envios.json` - Histórico de mensagens enviadas
- `Vendas_Lubrimax.xlsx` - Base de vendas da Lubrimax
- `requirements.txt` - Dependências Python
