"""
🚀 PLATAFORMA INTERATIVA DE BACKTEST - ESTRATÉGIA QUANTITATIVA SPY
Desenvolvida com Streamlit para análise em tempo real
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import yfinance as yf
import warnings

warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURAÇÃO DE PÁGINA
# ============================================================================

st.set_page_config(
    page_title="🚀 Backtest Platform - SPY",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# CLASSE DO BACKTESTER (SIMPLIFICADA)
# ============================================================================

class StrategyBacktester:
    """Sistema de backtest com interface web"""
    
    def __init__(self, ticker='SPY', days=90):
        self.ticker = ticker
        self.days = days
        self.data = None
        self.results = {}
    
    def fetch_data(self):
        """Buscar dados com fallback para dados simulados"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=self.days)
            
            self.data = yf.download(
                self.ticker,
                start=start_date,
                end=end_date,
                progress=False
            )
            
            if self.data is None or len(self.data) == 0:
                raise Exception("Sem dados")
            
        except:
            # Gerar dados simulados realistas
            self.data = self._generate_realistic_data()
        
        return self.data
    
    def _generate_realistic_data(self):
        """Gerar dados simulados realistas"""
        dates = pd.date_range(
            end=datetime.now(),
            periods=self.days,
            freq='B'
        )
        
        preco_inicial = 550
        drift = 0.0005
        volatilidade = 0.012
        
        np.random.seed(42)
        retornos = np.random.normal(drift, volatilidade, len(dates))
        precos = preco_inicial * np.exp(np.cumsum(retornos))
        
        data_dict = {
            'Open': [],
            'High': [],
            'Low': [],
            'Close': [],
            'Volume': []
        }
        
        for preco in precos:
            open_price = preco * np.random.uniform(0.99, 1.01)
            close_price = preco * np.random.uniform(0.99, 1.01)
            high_price = max(open_price, close_price) * np.random.uniform(1.0, 1.015)
            low_price = min(open_price, close_price) * np.random.uniform(0.985, 1.0)
            
            data_dict['Open'].append(open_price)
            data_dict['High'].append(high_price)
            data_dict['Low'].append(low_price)
            data_dict['Close'].append(close_price)
            data_dict['Volume'].append(np.random.randint(50_000_000, 100_000_000))
        
        return pd.DataFrame(data_dict, index=dates)
    
   def calculate_variation(self):
    """Calcular variação percentual diária"""
    self.data['pct_change'] = (
        (self.data['Close'] - self.data['Close'].shift(1)) / 
        self.data['Close'].shift(1) * 100
    )
    return self.data


def run_strategy(self, queda_percentual):
    """Executar estratégia para um parâmetro"""
    trades = []
    
    for i in range(1, len(self.data)):
        current_date = self.data.index[i]
        prev_pct_change = self.data['pct_change'].iloc[i]
        
        if prev_pct_change <= queda_percentual:
            entry_price = self.data['Open'].iloc[i]
            exit_price = self.data['Close'].iloc[i]
            retorno = ((exit_price - entry_price) / entry_price) * 100
            
            retorno = float(retorno)

            trade = {
                'data': current_date,
                'queda_trigger': prev_pct_change,
                'entrada_preco': entry_price,
                'saida_preco': exit_price,
                'retorno_percentual': retorno,
                'lucro': 1 if retorno > 0 else (-1 if retorno < 0 else 0)
            }
            
            trades.append(trade)
    
    return trades


def calculate_metrics(self, trades):
    """Calcular métricas de performance"""
    if not trades:
        return {
            'total_trades': 0,
            'acertos': 0,
            'erros': 0,
            'taxa_acerto': 0.0,
            'taxa_erro': 0.0,
            'maior_seq_acertos': 0,
            'maior_seq_erros': 0,
            'drawdown_maximo': 0.0,
            'retorno_acumulado': 0.0,
            'retorno_medio': 0.0,
            'maior_ganho': 0.0,
            'maior_perda': 0.0
            }
        
        df_trades = pd.DataFrame(trades)
        
        total_trades = len(df_trades)
        acertos = len(df_trades[df_trades['lucro'] > 0])
        erros = len(df_trades[df_trades['lucro'] < 0])
        
        taxa_acerto = (acertos / total_trades * 100) if total_trades > 0 else 0.0
        taxa_erro = (erros / total_trades * 100) if total_trades > 0 else 0.0
        
        maior_seq_acertos = self._maior_sequencia(df_trades['lucro'], 1)
        maior_seq_erros = self._maior_sequencia(df_trades['lucro'], -1)
        
        retornos = df_trades['retorno_percentual'].values
        capital_curva = np.cumprod(1 + retornos / 100) * 100
        
        cummax = np.maximum.accumulate(capital_curva)
        drawdown = (capital_curva - cummax) / cummax * 100
        drawdown_maximo = drawdown.min()
        
        retorno_acumulado = capital_curva[-1] - 100
        retorno_medio = df_trades['retorno_percentual'].mean()
        maior_ganho = df_trades['retorno_percentual'].max()
        maior_perda = df_trades['retorno_percentual'].min()
        
        return {
            'total_trades': total_trades,
            'acertos': acertos,
            'erros': erros,
            'taxa_acerto': taxa_acerto,
            'taxa_erro': taxa_erro,
            'maior_seq_acertos': maior_seq_acertos,
            'maior_seq_erros': maior_seq_erros,
            'drawdown_maximo': drawdown_maximo,
            'retorno_acumulado': retorno_acumulado,
            'retorno_medio': retorno_medio,
            'maior_ganho': maior_ganho,
            'maior_perda': maior_perda,
            'capital_curva': capital_curva,
            'trades_df': df_trades
        }
    
    def _maior_sequencia(self, series, valor):
        """Calcular maior sequência"""
        max_seq = 0
        current_seq = 0
        for v in series:
            if v == valor:
                current_seq += 1
                max_seq = max(max_seq, current_seq)
            else:
                current_seq = 0
        return max_seq
    
    def get_buy_hold_benchmark(self):
        """Retorno buy & hold"""
        preco_inicial = self.data['Close'].iloc[0]
        preco_final = self.data['Close'].iloc[-1]
        return ((preco_final - preco_inicial) / preco_inicial) * 100


# ============================================================================
# HEADER
# ============================================================================

st.markdown("# 🚀 Plataforma Interativa de Backtest")
st.markdown("## Estratégia Quantitativa - SPY (S&P 500 ETF)")

# ============================================================================
# SIDEBAR - CONTROLES
# ============================================================================

st.sidebar.markdown("## ⚙️ Configurações")

col1, col2 = st.sidebar.columns(2)

with col1:
    ticker = st.selectbox(
        "📈 Ativo",
        ["SPY", "QQQ", "IWM", "DIA"],
        help="Escolha o índice/ETF para análise"
    )

with col2:
    dias = st.number_input(
        "📅 Período (dias)",
        min_value=30,
        max_value=365,
        value=90,
        step=10,
        help="Número de dias históricos"
    )

st.sidebar.markdown("---")

st.sidebar.markdown("### 📊 Parâmetros da Estratégia")

# Modo de entrada
modo_entrada = st.sidebar.radio(
    "Modo de Teste",
    ["Teste Rápido", "Teste Customizado"],
    help="Escolha entre preset ou customizado"
)

if modo_entrada == "Teste Rápido":
    st.sidebar.markdown("**Presets Pré-configurados:**")
    preset = st.sidebar.selectbox(
        "Escolha um preset",
        [
            "Conservador (-1.0%)",
            "Moderado (-0.5%)",
            "Agressivo (-0.25%)",
            "Muito Agressivo (-0.1%)",
            "Personalizado"
        ]
    )
    
    preset_map = {
        "Conservador (-1.0%)": [-1.0],
        "Moderado (-0.5%)": [-0.5],
        "Agressivo (-0.25%)": [-0.25],
        "Muito Agressivo (-0.1%)": [-0.1],
        "Personalizado": None
    }
    
    quedas = preset_map.get(preset)
    
    if quedas is None:
        # Customizado dentro do preset
        queda_min = st.sidebar.slider(
            "Queda Mínima (%)",
            -5.0, 0.0, -0.5, 0.1
        )
        queda_max = st.sidebar.slider(
            "Queda Máxima (%)",
            -5.0, 0.0, 0.0, 0.1
        )
        queda_step = st.sidebar.slider(
            "Step (%)",
            0.1, 1.0, 0.25, 0.1
        )
        
        quedas = list(np.arange(queda_min, queda_max + queda_step, queda_step))
        quedas = [round(q, 2) for q in quedas]

else:  # Teste Customizado
    st.sidebar.markdown("**Configuração Manual:**")
    
    num_parametros = st.sidebar.number_input(
        "Número de thresholds",
        min_value=1,
        max_value=10,
        value=5
    )
    
    quedas = []
    for i in range(num_parametros):
        queda = st.sidebar.number_input(
            f"Threshold {i+1} (%)",
            min_value=-10.0,
            max_value=0.0,
            value=-0.5 - (i * 0.5),
            step=0.1
        )
        quedas.append(round(queda, 2))

# Remover duplicatas e ordenar
quedas = sorted(list(set(quedas)))

st.sidebar.markdown("---")

# Botão de execução
st.sidebar.markdown("### 🎬 Ações")
executar = st.sidebar.button(
    "▶️ Executar Backtest",
    use_container_width=True,
    type="primary"
)

# ============================================================================
# EXECUÇÃO DO BACKTEST
# ============================================================================

if executar:
    with st.spinner("⏳ Carregando dados e executando backtest..."):
        
        # Inicializar backtester
        backtester = StrategyBacktester(ticker=ticker, days=dias)
        backtester.fetch_data()
        backtester.calculate_variation()
        
        # Executar para cada threshold
        resultados_lista = []
        
        for queda in quedas:
            trades = backtester.run_strategy(queda)
            metricas = backtester.calculate_metrics(trades)
            
            backtester.results[queda] = metricas
            
            resultados_lista.append({
                'Queda %': queda,
                'Nº Trades': metricas['total_trades'],
                'Acertos': metricas['acertos'],
                'Erros': metricas['erros'],
                'Taxa Acerto %': f"{metricas['taxa_acerto']:.1f}%",
                'Taxa Erro %': f"{metricas['taxa_erro']:.1f}%",
                'Seq. Acertos': metricas['maior_seq_acertos'],
                'Seq. Erros': metricas['maior_seq_erros'],
                'Retorno %': f"{metricas['retorno_acumulado']:.2f}%",
                'Retorno Médio %': f"{metricas['retorno_medio']:.2f}%",
                'Drawdown Máx %': f"{metricas['drawdown_maximo']:.2f}%",
                'Maior Ganho %': f"{metricas['maior_ganho']:.2f}%",
                'Maior Perda %': f"{metricas['maior_perda']:.2f}%"
            })
        
        # Armazenar resultados em session state
        st.session_state['resultados_df'] = pd.DataFrame(resultados_lista)
        st.session_state['backtester'] = backtester
        st.session_state['quedas'] = quedas
        
        st.success("✅ Backtest executado com sucesso!")

# ============================================================================
# EXIBIÇÃO DE RESULTADOS
# ============================================================================

if 'resultados_df' in st.session_state:
    
    backtester = st.session_state['backtester']
    quedas = st.session_state['quedas']
    resultados_df = st.session_state['resultados_df']
    
    # ========================================================================
    # SEÇÃO 1: RESUMO EXECUTIVO
    # ========================================================================
    
    st.markdown("---")
    st.markdown("## 📊 Resumo Executivo")
    
    # Benchmark
    retorno_bh = backtester.get_buy_hold_benchmark()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📈 Buy & Hold",
            value=f"{retorno_bh:+.2f}%",
            delta=None,
            delta_color="normal"
        )
    
    with col2:
        best_return = resultados_df['Retorno %'].str.replace('%', '').astype(float).max()
        st.metric(
            label="🏆 Melhor Retorno",
            value=f"{best_return:+.2f}%",
            delta=f"{best_return - retorno_bh:+.2f}% vs B&H"
        )
    
    with col3:
        total_trades = resultados_df['Nº Trades'].sum()
        st.metric(
            label="📋 Total de Trades",
            value=int(total_trades)
        )
    
    with col4:
        avg_taxa_acerto = resultados_df['Taxa Acerto %'].str.replace('%', '').astype(float).mean()
        st.metric(
            label="🎯 Taxa de Acerto Média",
            value=f"{avg_taxa_acerto:.1f}%"
        )
    
    st.markdown("---")
    
    # ========================================================================
    # SEÇÃO 2: TABELA DE RESULTADOS
    # ========================================================================
    
    st.markdown("## 📈 Resultados Detalhados")
    
    # Configurar display da tabela
    st.dataframe(
        resultados_df,
        use_container_width=True,
        hide_index=True,
        height=250
    )
    
    # ========================================================================
    # SEÇÃO 3: GRÁFICOS
    # ========================================================================
    
    st.markdown("---")
    st.markdown("## 📊 Análise Gráfica")
    
    # Tabs para diferentes visualizações
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📈 Curva de Capital", "📊 Comparação", "📉 Distribuição", "🎯 Métricas", "💰 Trades"]
    )
    
    # ========================================================================
    # TAB 1: CURVA DE CAPITAL
    # ========================================================================
    
    with tab1:
        st.markdown("### Evolução da Curva de Capital")
        
        # Seletor de threshold
        queda_selecionada = st.selectbox(
            "Selecione o threshold",
            quedas,
            key="queda_curva"
        )
        
        # Gráfico de curva de capital
        metricas = backtester.results[queda_selecionada]
        capital_curva = metricas['capital_curva']
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            y=capital_curva,
            mode='lines+markers',
            name='Estratégia',
            line=dict(color='#2E86AB', width=2),
            fill='tozeroy',
            fillcolor='rgba(46, 134, 171, 0.2)',
            hovertemplate='<b>Trade %{x+1}</b><br>Capital: $%{y:.2f}<extra></extra>'
        ))
        
        fig.add_hline(
            y=100,
            line_dash="dash",
            line_color="#A23B72",
            annotation_text="Capital Inicial",
            annotation_position="right"
        )
        
        fig.update_layout(
            title=f"Curva de Capital - Queda {queda_selecionada}%",
            xaxis_title="Número do Trade",
            yaxis_title="Capital Acumulado ($)",
            hovermode='x unified',
            height=500,
            template='plotly_white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Estatísticas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Retorno Total",
                f"{metricas['retorno_acumulado']:+.2f}%"
            )
        
        with col2:
            st.metric(
                "Drawdown Máximo",
                f"{metricas['drawdown_maximo']:.2f}%"
            )
        
        with col3:
            st.metric(
                "Maior Ganho",
                f"{metricas['maior_ganho']:+.2f}%"
            )
        
        with col4:
            st.metric(
                "Maior Perda",
                f"{metricas['maior_perda']:+.2f}%"
            )
    
    # ========================================================================
    # TAB 2: COMPARAÇÃO
    # ========================================================================
    
    with tab2:
        st.markdown("### Estratégia vs Buy & Hold")
        
        queda_comparacao = st.selectbox(
            "Selecione o threshold",
            quedas,
            key="queda_comparacao"
        )
        
        metricas = backtester.results[queda_comparacao]
        capital_curva = metricas['capital_curva']
        
        # Normalizar preços para comparação
        precos = backtester.data['Close'].values
        precos_normalizados = precos / precos[0] * 100
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            y=capital_curva,
            mode='lines',
            name='Estratégia',
            line=dict(color='#2E86AB', width=2.5)
        ))
        
        fig.add_trace(go.Scatter(
            y=precos_normalizados,
            mode='lines',
            name='Buy & Hold',
            line=dict(color='#A23B72', width=2.5, dash='dash')
        ))
        
        fig.add_hline(
            y=100,
            line_dash=":",
            line_color="gray",
            opacity=0.5
        )
        
        fig.update_layout(
            title=f"Estratégia vs Buy & Hold - Queda {queda_comparacao}%",
            xaxis_title="Data (índice)",
            yaxis_title="Capital Acumulado ($)",
            hovermode='x unified',
            height=500,
            template='plotly_white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Resumo comparativo
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Estratégia",
                f"{metricas['retorno_acumulado']:+.2f}%",
                f"{metricas['total_trades']} trades"
            )
        
        with col2:
            st.metric(
                "Buy & Hold",
                f"{retorno_bh:+.2f}%",
                "Hold 90d"
            )
        
        with col3:
            outperf = metricas['retorno_acumulado'] - retorno_bh
            st.metric(
                "Outperformance",
                f"{outperf:+.2f}%",
                "pontos %"
            )
    
    # ========================================================================
    # TAB 3: DISTRIBUIÇÃO DE RETORNOS
    # ========================================================================
    
    with tab3:
        st.markdown("### Distribuição de Retornos por Trade")
        
        queda_dist = st.selectbox(
            "Selecione o threshold",
            quedas,
            key="queda_dist"
        )
        
        trades_df = backtester.results[queda_dist]['trades_df']
        
        if trades_df is not None and len(trades_df) > 0:
            retornos = trades_df['retorno_percentual'].values
            
            fig = go.Figure()
            
            # Cores baseadas em ganho/perda
            cores = ['#06A77D' if r > 0 else '#D62828' for r in retornos]
            
            fig.add_trace(go.Bar(
                y=retornos,
                x=[f"Trade {i+1}" for i in range(len(retornos))],
                marker_color=cores,
                hovertemplate='<b>%{x}</b><br>Retorno: %{y:.2f}%<extra></extra>',
                name='Retorno'
            ))
            
            # Adicionar média
            media = np.mean(retornos)
            fig.add_hline(
                y=media,
                line_dash="dash",
                line_color="#F77F00",
                annotation_text=f"Média: {media:.2f}%",
                annotation_position="right"
            )
            
            fig.update_layout(
                title=f"Distribuição de Retornos - Queda {queda_dist}%",
                xaxis_title="Trade",
                yaxis_title="Retorno (%)",
                height=500,
                template='plotly_white',
                showlegend=False,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Estatísticas da distribuição
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("Média", f"{np.mean(retornos):.2f}%")
            
            with col2:
                st.metric("Mediana", f"{np.median(retornos):.2f}%")
            
            with col3:
                st.metric("Desvio Padrão", f"{np.std(retornos):.2f}%")
            
            with col4:
                st.metric("Mínimo", f"{np.min(retornos):.2f}%")
            
            with col5:
                st.metric("Máximo", f"{np.max(retornos):.2f}%")
        
        else:
            st.warning("Nenhum trade executado para este threshold")
    
    # ========================================================================
    # TAB 4: ANÁLISE DE MÉTRICAS
    # ========================================================================
    
    with tab4:
        st.markdown("### Comparação de Métricas")
        
        # Preparar dados para gráficos
        df_analysis = pd.DataFrame({
            'Threshold': quedas,
            'Taxa Acerto': resultados_df['Taxa Acerto %'].str.replace('%', '').astype(float),
            'Retorno': resultados_df['Retorno %'].str.replace('%', '').astype(float),
            'Num Trades': resultados_df['Nº Trades'],
            'Drawdown': resultados_df['Drawdown Máx %'].str.replace('%', '').astype(float)
        })
        
        # Gráficos em subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=("Taxa de Acerto", "Retorno Acumulado", 
                          "Número de Trades", "Drawdown Máximo"),
            specs=[[{}, {}], [{}, {}]]
        )
        
        # Taxa de acerto
        fig.add_trace(
            go.Scatter(
                x=df_analysis['Threshold'],
                y=df_analysis['Taxa Acerto'],
                mode='lines+markers',
                name='Taxa Acerto',
                line=dict(color='#2E86AB', width=2),
                marker=dict(size=8)
            ),
            row=1, col=1
        )
        
        # Retorno
        fig.add_trace(
            go.Scatter(
                x=df_analysis['Threshold'],
                y=df_analysis['Retorno'],
                mode='lines+markers',
                name='Retorno',
                line=dict(color='#06A77D', width=2),
                marker=dict(size=8)
            ),
            row=1, col=2
        )
        
        # Número de trades
        fig.add_trace(
            go.Bar(
                x=df_analysis['Threshold'],
                y=df_analysis['Num Trades'],
                name='Nº Trades',
                marker_color='#F77F00'
            ),
            row=2, col=1
        )
        
        # Drawdown
        fig.add_trace(
            go.Scatter(
                x=df_analysis['Threshold'],
                y=df_analysis['Drawdown'],
                mode='lines+markers',
                name='Drawdown',
                line=dict(color='#D62828', width=2),
                marker=dict(size=8)
            ),
            row=2, col=2
        )
        
        # Atualizar layouts
        fig.update_xaxes(title_text="Threshold (%)", row=1, col=1)
        fig.update_xaxes(title_text="Threshold (%)", row=1, col=2)
        fig.update_xaxes(title_text="Threshold (%)", row=2, col=1)
        fig.update_xaxes(title_text="Threshold (%)", row=2, col=2)
        
        fig.update_yaxes(title_text="Taxa (%)", row=1, col=1)
        fig.update_yaxes(title_text="Retorno (%)", row=1, col=2)
        fig.update_yaxes(title_text="Quantidade", row=2, col=1)
        fig.update_yaxes(title_text="Drawdown (%)", row=2, col=2)
        
        fig.update_layout(height=600, showlegend=False, template='plotly_white')
        
        st.plotly_chart(fig, use_container_width=True)
    
    # ========================================================================
    # TAB 5: DETALHES DOS TRADES
    # ========================================================================
    
    with tab5:
        st.markdown("### Lista Detalhada de Trades")
        
        queda_trades = st.selectbox(
            "Selecione o threshold",
            quedas,
            key="queda_trades"
        )
        
        trades_df = backtester.results[queda_trades]['trades_df']
        
        if trades_df is not None and len(trades_df) > 0:
            # Formatar para exibição
            display_df = trades_df.copy()
            display_df['data'] = display_df['data'].dt.strftime('%Y-%m-%d')
            display_df['queda_trigger'] = display_df['queda_trigger'].apply(lambda x: f"{x:.2f}%")
            display_df['entrada_preco'] = display_df['entrada_preco'].apply(lambda x: f"${x:.2f}")
            display_df['saida_preco'] = display_df['saida_preco'].apply(lambda x: f"${x:.2f}")
            display_df['retorno_percentual'] = display_df['retorno_percentual'].apply(lambda x: f"{x:+.2f}%")
            
            # Renomear colunas
            display_df = display_df.rename(columns={
                'data': 'Data',
                'queda_trigger': 'Queda Trigger',
                'entrada_preco': 'Preço Entrada',
                'saida_preco': 'Preço Saída',
                'retorno_percentual': 'Retorno',
                'lucro': 'Resultado'
            })
            
            # Exibir dataframe
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
                height=400
            )
            
            # Opção de download
            csv = display_df.to_csv(index=False)
            st.download_button(
                label="📥 Baixar como CSV",
                data=csv,
                file_name=f"trades_queda_{queda_trades}.csv",
                mime="text/csv"
            )
        
        else:
            st.warning("Nenhum trade executado para este threshold")
    
    st.markdown("---")
    
    # ========================================================================
    # SEÇÃO: INSIGHTS E RECOMENDAÇÕES
    # ========================================================================
    
    st.markdown("## 💡 Insights e Recomendações")
    
    # Análise automática
    best_idx = resultados_df['Retorno %'].str.replace('%', '').astype(float).idxmax()
    best_queda = resultados_df.loc[best_idx, 'Queda %']
    best_return = resultados_df.loc[best_idx, 'Retorno %']
    best_taxa = resultados_df.loc[best_idx, 'Taxa Acerto %']
    
    menor_dd_idx = resultados_df['Drawdown Máx %'].str.replace('%', '').astype(float).idxmin()
    menor_dd_queda = resultados_df.loc[menor_dd_idx, 'Queda %']
    menor_dd = resultados_df.loc[menor_dd_idx, 'Drawdown Máx %']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏆 Melhor Performance")
        st.success(f"""
        **Threshold:** {best_queda}%  
        **Retorno:** {best_return}  
        **Taxa de Acerto:** {best_taxa}  
        **Outperformance:** +{float(best_return.strip('%')) - retorno_bh:+.2f}% vs B&H
        """)
    
    with col2:
        st.markdown("### 🛡️ Menor Risco")
        st.info(f"""
        **Threshold:** {menor_dd_queda}%  
        **Drawdown Máx:** {menor_dd}  
        **Trades:** {int(resultados_df.loc[menor_dd_idx, 'Nº Trades'])}  
        **Taxa Acerto:** {resultados_df.loc[menor_dd_idx, 'Taxa Acerto %']}
        """)
    
    st.markdown("### 📌 Recomendações")
    
    recomendacoes = []
    
    if float(best_return.strip('%')) > retorno_bh:
        recomendacoes.append(f"✅ Estratégia supera o benchmark em {float(best_return.strip('%')) - retorno_bh:+.2f}%")
    else:
        recomendacoes.append(f"⚠️ Estratégia underperforma o benchmark em {float(best_return.strip('%')) - retorno_bh:+.2f}%")
    
    best_taxa_float = float(best_taxa.strip('%'))
    if best_taxa_float > 60:
        recomendacoes.append("✅ Taxa de acerto acima de 60% indica padrão robusto")
    elif best_taxa_float > 50:
        recomendacoes.append("⚠️ Taxa de acerto próxima a 50%, verifique significância estatística")
    else:
        recomendacoes.append("❌ Taxa de acerto abaixo de 50%, padrão pode ser aleatório")
    
    if abs(float(menor_dd.strip('%'))) < 5:
        recomendacoes.append("✅ Drawdown controlado (< 5%)")
    else:
        recomendacoes.append(f"⚠️ Drawdown significativo ({menor_dd})")
    
    for rec in recomendacoes:
        st.write(rec)

else:
    st.info("👈 Configure os parâmetros na barra lateral e clique em 'Executar Backtest' para começar")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 12px;'>
    <p>📊 Plataforma de Backtest Quantitativo v1.0 | Desenvolvido com Streamlit</p>
    <p>⚠️ Para fins educacionais e de pesquisa. Não é recomendação de investimento.</p>
    <p>Dados simulados quando acesso ao Yahoo Finance não está disponível</p>
</div>
""", unsafe_allow_html=True)
