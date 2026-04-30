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

            self.data = yf.download(self.ticker, start=start, end=end, progress=False)

            if self.data is None or len(self.data) == 0:
                raise Exception("Sem dados")

        except:
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
        self.data['pct_change'] = self.data['Close'].pct_change() * 100
        return self.data

    def run_strategy(self, queda_percentual):
        trades = []

        for i in range(1, len(self.data)):

            pct = self.data['pct_change'].iloc[i]

            if pct <= queda_percentual:
                entry = self.data['Open'].iloc[i]
                exit_ = self.data['Close'].iloc[i]

                retorno = ((exit_ - entry) / entry) * 100

                trade = {
                    'data': self.data.index[i],
                    'queda_trigger': pct,
                    'entrada_preco': entry,
                    'saida_preco': exit_,
                    'retorno_percentual': retorno,
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
                'retorno_acumulado': 0
            }

        df = pd.DataFrame(trades)

        total = len(df)
        acertos = (df['lucro'] > 0).sum()
        erros = (df['lucro'] < 0).sum()

        taxa = acertos / total * 100

        retornos = df['retorno_percentual'].values
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
        return (self.data['Close'].iloc[-1] / self.data['Close'].iloc[0] - 1) * 100


st.title("Backtest SPY")

ticker = st.selectbox("Ativo", ["SPY", "QQQ", "IWM"])
dias = st.slider("Dias", 30, 365, 90)
queda = st.slider("Queda (%)", -5.0, 0.0, -0.5)

if st.button("Executar"):

    bt = StrategyBacktester(ticker, dias)
    bt.fetch_data()
    bt.calculate_variation()

    trades = bt.run_strategy(queda)
    metrics = bt.calculate_metrics(trades)

    st.write("Trades:", metrics['total_trades'])
    st.write("Acertos:", metrics['acertos'])
    st.write("Erros:", metrics['erros'])
    st.write("Taxa de acerto:", f"{metrics['taxa_acerto']:.2f}%")
    st.write("Retorno:", f"{metrics['retorno_acumulado']:.2f}%")
    st.write("Buy & Hold:", f"{bt.get_buy_hold():.2f}%")

    if metrics['total_trades'] > 0:
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=metrics['capital_curva'], mode='lines'))
        st.plotly_chart(fig, use_container_width=True)
