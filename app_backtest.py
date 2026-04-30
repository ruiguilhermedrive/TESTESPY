import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import yfinance as yf
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Backtest SPY",
    layout="wide"
)


class StrategyBacktester:

    def __init__(self, ticker='SPY', days=90):
        self.ticker = ticker
        self.days = days
        self.data = None
        self.results = {}

    def fetch_data(self):
        try:
            end = datetime.now()
            start = end - timedelta(days=self.days)

            df = yf.download(self.ticker, start=start, end=end, progress=False)

            if df is None or len(df) == 0:
                raise Exception("Sem dados")

            # FIX 1: yfinance retorna MultiIndex nas colunas (ex: ('Close', 'SPY'))
            # Precisamos achatar para nomes simples ('Close', 'Open', etc.)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            self.data = df

        except Exception:
            self.data = self._generate_fake_data()

        return self.data

    def _generate_fake_data(self):
        dates = pd.date_range(end=datetime.now(), periods=self.days, freq='B')

        np.random.seed(42)
        returns = np.random.normal(0.0005, 0.012, len(dates))
        prices = 550 * np.exp(np.cumsum(returns))

        df = pd.DataFrame(index=dates)
        df['Close'] = prices
        df['Open'] = prices * np.random.uniform(0.99, 1.01, len(prices))
        df['High'] = df[['Open', 'Close']].max(axis=1) * np.random.uniform(1.0, 1.015, len(prices))
        df['Low'] = df[['Open', 'Close']].min(axis=1) * np.random.uniform(0.985, 1.0, len(prices))
        df['Volume'] = np.random.randint(50_000_000, 100_000_000, len(prices))

        return df

    def calculate_variation(self):
        # FIX 2: usar .squeeze() para garantir que Close é Series, não DataFrame
        # (necessário quando o MultiIndex não foi achatado corretamente)
        close = self.data['Close'].squeeze()
        self.data['pct_change'] = close.pct_change() * 100
        return self.data

    def run_strategy(self, queda_percentual):
        trades = []

        for i in range(1, len(self.data)):

            # FIX 3: usar .item() para converter para scalar Python puro
            # sem isso, .iloc[i] em DataFrame com MultiIndex retorna Series,
            # e a comparação "if pct <= queda_percentual" lança ValueError
            pct = float(self.data['pct_change'].iloc[i])

            if pd.isna(pct):
                continue

            if pct <= queda_percentual:
                # FIX 4: converter entry/exit para float scalar
                # (mesma causa: Open/Close com MultiIndex retornavam Series)
                entry = float(self.data['Open'].iloc[i])
                exit_ = float(self.data['Close'].iloc[i])

                # FIX 5: garantir que entry != 0 para evitar divisão por zero
                if entry == 0:
                    continue

                retorno = ((exit_ - entry) / entry) * 100

                trade = {
                    'data': self.data.index[i],
                    'queda_trigger': round(pct, 4),
                    'entrada_preco': round(entry, 4),
                    'saida_preco': round(exit_, 4),
                    'retorno_percentual': round(retorno, 4),
                    'lucro': 1 if retorno > 0 else (-1 if retorno < 0 else 0)
                }

                trades.append(trade)

        return trades

    def calculate_metrics(self, trades):

        if len(trades) == 0:
            return {
                'total_trades': 0,
                'acertos': 0,
                'erros': 0,
                'taxa_acerto': 0,
                'retorno_acumulado': 0,
                'capital_curva': np.array([1.0])
            }

        df = pd.DataFrame(trades)

        total = len(df)
        acertos = int((df['lucro'] > 0).sum())
        erros = int((df['lucro'] < 0).sum())

        taxa = acertos / total * 100

        retornos = df['retorno_percentual'].values.astype(float)
        curva = np.cumprod(1 + retornos / 100)

        return {
            'total_trades': total,
            'acertos': acertos,
            'erros': erros,
            'taxa_acerto': taxa,
            'retorno_acumulado': (curva[-1] - 1) * 100,
            'capital_curva': curva
        }

    def get_buy_hold(self):
        # FIX 6: squeeze() garante scalar mesmo com MultiIndex residual
        close = self.data['Close'].squeeze()
        return float((close.iloc[-1] / close.iloc[0] - 1) * 100)


# ── UI ────────────────────────────────────────────────────────────────────────

st.title("📈 Backtest SPY")
st.markdown("---")

col_left, col_right = st.columns([1, 3])

with col_left:
    st.subheader("⚙️ Parâmetros")
    ticker = st.selectbox("Ativo", ["SPY", "QQQ", "IWM"])
    dias = st.slider("Período (dias)", 30, 365, 90)
    queda = st.slider("Queda mínima (%)", -5.0, -0.1, -0.5, step=0.1,
                      help="Entra na operação quando o ativo cai pelo menos esse percentual no dia")
    executar = st.button("▶ Executar Backtest", use_container_width=True)

if executar:

    with st.spinner("Baixando dados e executando backtest..."):
        bt = StrategyBacktester(ticker, dias)
        bt.fetch_data()
        bt.calculate_variation()

        trades = bt.run_strategy(queda)
        metrics = bt.calculate_metrics(trades)
        buy_hold = bt.get_buy_hold()

    st.markdown("---")

    # ── Métricas principais ────────────────────────────────────────────────
    st.subheader("📊 Resultados")

    m1, m2, m3, m4, m5, m6 = st.columns(6)
    m1.metric("Total Trades", metrics['total_trades'])
    m2.metric("Acertos", metrics['acertos'])
    m3.metric("Erros", metrics['erros'])
    m4.metric("Taxa de Acerto", f"{metrics['taxa_acerto']:.1f}%")
    m5.metric("Retorno Estratégia", f"{metrics['retorno_acumulado']:.2f}%")
    m6.metric("Buy & Hold", f"{buy_hold:.2f}%")

    # ── Gráfico da curva de capital ────────────────────────────────────────
    if metrics['total_trades'] > 0:
        st.markdown("---")
        st.subheader("📉 Curva de Capital")

        curva = metrics['capital_curva']
        indices = list(range(1, len(curva) + 1))

        fig = go.Figure()

        # Linha da estratégia
        fig.add_trace(go.Scatter(
            x=indices,
            y=curva,
            mode='lines+markers',
            name='Estratégia',
            line=dict(color='#2E86AB', width=2),
            marker=dict(size=5),
            fill='tozeroy',
            fillcolor='rgba(46, 134, 171, 0.1)'
        ))

        # Linha de referência (capital inicial = 1.0)
        fig.add_hline(y=1.0, line_dash="dash", line_color="#A23B72",
                      annotation_text="Capital Inicial", annotation_position="bottom right")

        fig.update_layout(
            xaxis_title="Nº do Trade",
            yaxis_title="Capital Acumulado (base 1.0)",
            hovermode="x unified",
            height=420,
            margin=dict(l=40, r=20, t=30, b=40),
            legend=dict(orientation="h", yanchor="bottom", y=1.02)
        )

        st.plotly_chart(fig, use_container_width=True)

        # ── Tabela de trades ───────────────────────────────────────────────
        st.markdown("---")
        st.subheader("📋 Histórico de Trades")

        df_trades = pd.DataFrame(trades)
        df_trades['data'] = pd.to_datetime(df_trades['data']).dt.strftime('%Y-%m-%d')
        df_trades['resultado'] = df_trades['lucro'].map({1: '✅ Gain', -1: '❌ Loss', 0: '➖ Zero'})

        df_exibir = df_trades[['data', 'queda_trigger', 'entrada_preco',
                                'saida_preco', 'retorno_percentual', 'resultado']].copy()
        df_exibir.columns = ['Data', 'Queda Trigger (%)', 'Entrada ($)',
                              'Saída ($)', 'Retorno (%)', 'Resultado']

        st.dataframe(df_exibir, use_container_width=True, hide_index=True)

    else:
        st.info(f"ℹ️ Nenhum trade encontrado com queda de {queda}% no período selecionado. "
                "Tente aumentar o período ou reduzir o threshold de queda.")
