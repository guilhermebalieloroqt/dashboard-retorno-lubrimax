"""
Dashboard Lubrimax - Análise de Retorno das Mensagens
Mostra o comparativo entre mensagens enviadas e clientes que retornaram à loja
"""

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# ==================== CONFIGURAÇÕES ====================
HISTORICO_FILE = "historico_envios.json"
VENDAS_FILE = "Vendas_Lubrimax.xlsx"

# ==================== FUNÇÕES DE DADOS ====================

@st.cache_data(ttl=300)  # Cache por 5 minutos
def carregar_historico():
    """Carrega o histórico de envios"""
    if os.path.exists(HISTORICO_FILE):
        with open(HISTORICO_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


@st.cache_data(ttl=300)
def carregar_vendas():
    """Carrega as vendas do Excel"""
    try:
        df = pd.read_excel(VENDAS_FILE, sheet_name="Sheet1")
        return df
    except Exception as e:
        st.error(f"Erro ao carregar vendas: {e}")
        return pd.DataFrame()


def parse_valor(valor):
    """Converte string de valor (ex: '1654,3') para float"""
    try:
        if isinstance(valor, (int, float)):
            return float(valor)
        if isinstance(valor, str):
            # Remove R$ e espacos, substitui virgula por ponto
            valor_limpo = valor.replace('R$', '').strip().replace(',', '.')
            if not valor_limpo:
                return 0.0
            return float(valor_limpo)
    except:
        pass
    return 0.0


def parse_data_emissao(emissao):
    """Converte data de emissão para datetime"""
    try:
        if pd.isna(emissao):
            return None
        if isinstance(emissao, str):
            parts = emissao.split('/')
            if len(parts) == 3:
                day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
                return datetime(year, month, day)
        elif isinstance(emissao, datetime):
            return emissao
    except:
        pass
    return None


def analisar_retorno(historico: dict, df_vendas: pd.DataFrame) -> pd.DataFrame:
    """
    Analisa quais clientes que receberam mensagem voltaram à loja.
    Considera retorno se houve venda após a data de envio da mensagem.
    """
    resultados = []
    
    for mes_ano, envios in historico.items():
        for placa, dados in envios.items():
            # Data de envio da mensagem
            data_envio_str = dados.get('data_envio', '')
            try:
                data_envio = datetime.strptime(data_envio_str, "%Y-%m-%d %H:%M:%S")
            except:
                continue
            
            # Busca vendas desta placa após a data de envio
            vendas_placa = df_vendas[
                df_vendas['IDENTIFICAÇÃO'].astype(str).str.upper().str.contains(placa, na=False) |
                df_vendas['OBSERVAÇÃO'].astype(str).str.upper().str.contains(placa, na=False)
            ].copy()
            
            # Filtra vendas após o envio da mensagem
            vendas_apos = []
            valor_total = 0
            
            for _, venda in vendas_placa.iterrows():
                data_venda = parse_data_emissao(venda.get('EMISSÃO'))
                if data_venda and data_venda > data_envio:
                    valor_venda = parse_valor(venda.get('TOTAL VENDA', 0))
                    vendas_apos.append({
                        'data': data_venda,
                        'valor': valor_venda,
                        'cliente': venda.get('CLIENTE', '')
                    })
                    valor_total += valor_venda
            
            retornou = len(vendas_apos) > 0
            dias_ate_retorno = None
            
            if retornou:
                primeira_venda = min(v['data'] for v in vendas_apos)
                dias_ate_retorno = (primeira_venda - data_envio).days
            
            resultados.append({
                'mes_referencia': mes_ano,
                'placa': placa,
                'nome': dados.get('nome', ''),
                'telefone': dados.get('fone', ''),
                'data_envio': data_envio,
                'retornou': retornou,
                'qtd_retornos': len(vendas_apos),
                'valor_gerado': valor_total,
                'dias_ate_retorno': dias_ate_retorno
            })
    
    return pd.DataFrame(resultados)


# ==================== INTERFACE STREAMLIT ====================

def main():
    st.set_page_config(
        page_title="Lubrimax - Dashboard de Retorno",
        page_icon="🚗",
        layout="wide"
    )
    
    # CSS customizado para visual moderno
    st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    .stMetric {
        background: linear-gradient(135deg, #2d3436 0%, #000000 100%);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #4a4a4a;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    .stMetric label {
        color: #a8dadc !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #f1faee !important;
        font-size: 2rem !important;
    }
    .stMetric [data-testid="stMetricDelta"] {
        color: #52b788 !important;
    }
    h1, h2, h3 {
        color: #f8f9fa !important;
    }
    .stSubheader {
        background: linear-gradient(90deg, #00b4d8, #0077b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🚗 Lubrimax - Dashboard de Retorno")
    st.markdown("### 📊 Análise de efetividade das mensagens de lembrete de troca de óleo")
    
    # Carrega dados
    historico = carregar_historico()
    df_vendas = carregar_vendas()
    
    if not historico:
        st.warning("⚠️ Nenhum histórico de envios encontrado. Execute a automação primeiro.")
        return
    
    if df_vendas.empty:
        st.warning("⚠️ Não foi possível carregar o arquivo de vendas.")
        return
    
    # Análise de retorno
    df_analise = analisar_retorno(historico, df_vendas)
    
    if df_analise.empty:
        st.warning("⚠️ Nenhum dado para análise.")
        return
    
    # ==================== MÉTRICAS PRINCIPAIS ====================
    st.markdown("---")
    st.subheader("📊 Métricas Principais")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_enviados = len(df_analise)
    total_retornos = df_analise['retornou'].sum()
    taxa_retorno = (total_retornos / total_enviados * 100) if total_enviados > 0 else 0
    valor_total_gerado = df_analise['valor_gerado'].sum()
    media_dias_retorno = df_analise[df_analise['retornou']]['dias_ate_retorno'].mean()
    
    with col1:
        st.metric(
            label="📤 Mensagens Enviadas",
            value=f"{total_enviados:,}"
        )
    
    with col2:
        st.metric(
            label="✅ Clientes Retornaram",
            value=f"{total_retornos:,}",
            delta=f"{taxa_retorno:.1f}%"
        )
    
    with col3:
        st.metric(
            label="📈 Taxa de Retorno",
            value=f"{taxa_retorno:.1f}%"
        )
    
    with col4:
        st.metric(
            label="💰 Valor Gerado",
            value=f"R$ {valor_total_gerado:,.2f}"
        )
    
    with col5:
        st.metric(
            label="⏱️ Média Dias p/ Retorno",
            value=f"{media_dias_retorno:.0f}" if pd.notna(media_dias_retorno) else "N/A"
        )
    
    # ==================== GRÁFICOS ====================
    st.markdown("---")
    
    col_graf1, col_graf2 = st.columns(2)
    
    with col_graf1:
        st.subheader("📊 Retorno vs Não Retorno")
        
        df_pizza = pd.DataFrame({
            'Status': ['Retornou ✅', 'Não Retornou ❌'],
            'Quantidade': [total_retornos, total_enviados - total_retornos]
        })
        
        fig_pizza = px.pie(
            df_pizza, 
            values='Quantidade', 
            names='Status',
            color='Status',
            color_discrete_map={'Retornou ✅': '#00b894', 'Não Retornou ❌': '#e17055'},
            hole=0.5
        )
        fig_pizza.update_traces(
            textposition='inside', 
            textinfo='percent+value',
            textfont_size=14,
            textfont_color='white',
            marker=dict(
                line=dict(color='#2d3436', width=3)
            ),
            pull=[0.05, 0]
        )
        fig_pizza.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=12),
            legend=dict(
                bgcolor='rgba(45,52,54,0.8)',
                bordercolor='#4a4a4a',
                borderwidth=1,
                font=dict(color='white')
            ),
            margin=dict(t=30, b=30, l=30, r=30),
            annotations=[dict(
                text=f'<b>{total_retornos}</b><br>Retornos',
                x=0.5, y=0.5,
                font_size=16,
                font_color='#00b894',
                showarrow=False
            )]
        )
        st.plotly_chart(fig_pizza, width='stretch')
    
    with col_graf2:
        st.subheader("💰 Valor Gerado por Mês")
        
        if 'mes_referencia' in df_analise.columns:
            df_valor_mes = df_analise.groupby('mes_referencia').agg({
                'valor_gerado': 'sum',
                'retornou': 'sum'
            }).reset_index()
            df_valor_mes.columns = ['Mês', 'Valor Gerado', 'Retornos']
            
            # Formata mês para exibição amigável (2025-12 -> Dez/2025)
            meses_pt = {
                '01': 'Jan', '02': 'Fev', '03': 'Mar', '04': 'Abr',
                '05': 'Mai', '06': 'Jun', '07': 'Jul', '08': 'Ago',
                '09': 'Set', '10': 'Out', '11': 'Nov', '12': 'Dez'
            }
            df_valor_mes['Mês_Formatado'] = df_valor_mes['Mês'].apply(
                lambda x: f"{meses_pt.get(x.split('-')[1], x.split('-')[1])}/{x.split('-')[0]}" if '-' in str(x) else str(x)
            )
            
            fig_barras = go.Figure()
            
            fig_barras.add_trace(go.Bar(
                x=df_valor_mes['Mês_Formatado'],
                y=df_valor_mes['Valor Gerado'],
                text=[f'R$ {v:,.0f}' for v in df_valor_mes['Valor Gerado']],
                textposition='outside',
                textfont=dict(color='#00b894', size=14, family='Arial Black'),
                marker=dict(
                    color=['#0077b6', '#00b4d8', '#00b894', '#48cae4', '#90e0ef'][:len(df_valor_mes)],
                    line=dict(color='#2d3436', width=2)
                ),
                hovertemplate='<b>%{x}</b><br>Valor: R$ %{y:,.2f}<br>Retornos: %{customdata}<extra></extra>',
                customdata=df_valor_mes['Retornos']
            ))
            
            fig_barras.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', size=12),
                xaxis=dict(
                    title=dict(text='Mês de Referência', font=dict(color='#a8dadc')),
                    tickfont=dict(color='white', size=14),
                    gridcolor='rgba(255,255,255,0.1)',
                    showgrid=False,
                    type='category'  # Força como categoria/texto
                ),
                yaxis=dict(
                    title=dict(text='Valor Gerado (R$)', font=dict(color='#a8dadc')),
                    tickfont=dict(color='white'),
                    gridcolor='rgba(255,255,255,0.1)',
                    tickformat=',.0f'
                ),
                margin=dict(t=50, b=50, l=70, r=30),
                showlegend=False
            )
            st.plotly_chart(fig_barras, width='stretch')
    
    # ==================== DISTRIBUIÇÃO DE DIAS ATÉ RETORNO ====================
    st.markdown("---")
    st.subheader("⏱️ Distribuição de Dias até o Retorno")
    
    df_retornos = df_analise[df_analise['retornou'] == True]
    
    if not df_retornos.empty:
        fig_hist = go.Figure()
        
        fig_hist.add_trace(go.Histogram(
            x=df_retornos['dias_ate_retorno'],
            nbinsx=20,
            marker=dict(
                color='rgba(0, 180, 216, 0.7)',
                line=dict(color='#00b4d8', width=2)
            ),
            hovertemplate='<b>%{x} dias</b><br>Clientes: %{y}<extra></extra>'
        ))
        
        # Adiciona linha de média
        media = df_retornos['dias_ate_retorno'].mean()
        fig_hist.add_vline(
            x=media, 
            line_dash="dash", 
            line_color="#e17055",
            annotation_text=f"Média: {media:.0f} dias",
            annotation_position="top",
            annotation_font_color="#e17055"
        )
        
        fig_hist.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=12),
            xaxis=dict(
                title=dict(text='Dias após receber a mensagem', font=dict(color='#a8dadc', size=14)),
                tickfont=dict(color='white'),
                gridcolor='rgba(255,255,255,0.1)',
                zeroline=False
            ),
            yaxis=dict(
                title=dict(text='Quantidade de clientes', font=dict(color='#a8dadc', size=14)),
                tickfont=dict(color='white'),
                gridcolor='rgba(255,255,255,0.1)',
                zeroline=False
            ),
            bargap=0.1,
            margin=dict(t=50, b=50, l=50, r=30)
        )
        st.plotly_chart(fig_hist, width='stretch')
    else:
        st.info("Ainda não há dados de retorno para exibir o histograma.")
    
    # ==================== TABELA DE CLIENTES ====================
    st.markdown("---")
    st.subheader("📋 Detalhamento por Cliente")
    
    # Filtros
    col_filtro1, col_filtro2, col_filtro3 = st.columns(3)
    
    with col_filtro1:
        filtro_status = st.selectbox(
            "Status de Retorno",
            options=["Todos", "Retornou", "Não Retornou"]
        )
    
    with col_filtro2:
        meses_disponiveis = ["Todos"] + sorted(df_analise['mes_referencia'].unique().tolist())
        filtro_mes = st.selectbox("Mês de Referência", options=meses_disponiveis)
    
    with col_filtro3:
        busca_nome = st.text_input("🔍 Buscar por Nome/Placa")
    
    # Aplica filtros
    df_filtrado = df_analise.copy()
    
    if filtro_status == "Retornou":
        df_filtrado = df_filtrado[df_filtrado['retornou'] == True]
    elif filtro_status == "Não Retornou":
        df_filtrado = df_filtrado[df_filtrado['retornou'] == False]
    
    if filtro_mes != "Todos":
        df_filtrado = df_filtrado[df_filtrado['mes_referencia'] == filtro_mes]
    
    if busca_nome:
        df_filtrado = df_filtrado[
            df_filtrado['nome'].str.contains(busca_nome, case=False, na=False) |
            df_filtrado['placa'].str.contains(busca_nome, case=False, na=False)
        ]
    
    # Formata para exibição
    df_exibir = df_filtrado[[
        'nome', 'placa', 'telefone', 'data_envio', 'retornou', 
        'qtd_retornos', 'valor_gerado', 'dias_ate_retorno'
    ]].copy()
    
    df_exibir.columns = [
        'Cliente', 'Placa', 'Telefone', 'Data Envio', 'Retornou?',
        'Qtd. Visitas', 'Valor Gerado (R$)', 'Dias até Retorno'
    ]
    
    df_exibir['Retornou?'] = df_exibir['Retornou?'].apply(lambda x: '✅ Sim' if x else '❌ Não')
    df_exibir['Data Envio'] = pd.to_datetime(df_exibir['Data Envio']).dt.strftime('%d/%m/%Y %H:%M')
    df_exibir['Valor Gerado (R$)'] = df_exibir['Valor Gerado (R$)'].apply(lambda x: f"R$ {x:,.2f}")
    
    st.dataframe(
        df_exibir,
        width='stretch',
        hide_index=True,
        height=400
    )
    
    # Download
    st.download_button(
        label="📥 Baixar Relatório Completo (Excel)",
        data=df_filtrado.to_csv(index=False).encode('utf-8'),
        file_name=f"relatorio_retorno_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
    
    # ==================== RESUMO EXECUTIVO ====================
    st.markdown("---")
    st.subheader("📝 Resumo Executivo")
    
    custo_estimado_por_msg = 0.05  # Custo estimado por mensagem (ajustar conforme necessidade)
    custo_total = total_enviados * custo_estimado_por_msg
    roi = ((valor_total_gerado - custo_total) / custo_total * 100) if custo_total > 0 else 0
    
    st.markdown(f"""
    ### Análise de Retorno sobre Investimento (ROI)
    
    | Métrica | Valor |
    |---------|-------|
    | **Total de mensagens enviadas** | {total_enviados:,} |
    | **Clientes que retornaram** | {total_retornos:,} ({taxa_retorno:.1f}%) |
    | **Valor total gerado pelos retornos** | R$ {valor_total_gerado:,.2f} |
    | **Média de dias até o retorno** | {media_dias_retorno:.0f} dias |
    | **Valor médio por retorno** | R$ {(valor_total_gerado/total_retornos if total_retornos > 0 else 0):,.2f} |
    
    ---
    
    #### 💡 Insights
    
    - **Taxa de conversão de {taxa_retorno:.1f}%** - A cada 100 mensagens enviadas, aproximadamente {taxa_retorno:.0f} clientes retornam à loja.
    - Os clientes que retornam levam em média **{media_dias_retorno:.0f} dias** após receberem a mensagem.
    - O sistema está gerando um valor de **R$ {(valor_total_gerado/total_enviados if total_enviados > 0 else 0):,.2f} por mensagem enviada**.
    
    #### ✅ Conclusão
    
    O sistema de lembretes está {"**funcionando bem**" if taxa_retorno >= 5 else "**com potencial de melhoria**"}, 
    trazendo clientes de volta à loja e gerando receita adicional de **R$ {valor_total_gerado:,.2f}**.
    """)
    
    # Footer
    st.markdown("---")
    st.caption(f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")


if __name__ == "__main__":
    main()
