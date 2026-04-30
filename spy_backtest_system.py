"""
Sistema de Backtest para Estratégia Quantitativa - SPY
Desenvolvido com dados do Yahoo Finance
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import yfinance as yf

warnings.filterwarnings('ignore')

# ============================================================================
# CLASSE PRINCIPAL DO BACKTEST
# ============================================================================

class StrategyBacktester:
    """
    Sistema completo de backtest para estratégia de queda de preço intraday
    """
    
    def __init__(self, ticker: str = 'SPY', days: int = 90):
        """
        Inicializa o backtester
        
        Args:
            ticker (str): Símbolo do ativo (padrão: SPY)
            days (int): Número de dias históricos (padrão: 90)
        """
        self.ticker = ticker
        self.days = days
        self.data = None
        self.trades = None
        self.results = {}
        
    def fetch_data(self) -> pd.DataFrame:
        """
        Baixa dados históricos do Yahoo Finance (com fallback para dados simulados)
        
        Returns:
            pd.DataFrame: DataFrame com dados OHLCV
        """
        print(f"📥 Baixando dados para {self.ticker} (últimos {self.days} dias)...")
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=self.days)
        
        try:
            # Tentar baixar do Yahoo Finance
            self.data = yf.download(
                self.ticker,
                start=start_date,
                end=end_date,
                progress=False
            )
            
            if self.data is None or len(self.data) == 0:
                raise Exception("Nenhum dado retornado")
            
            # Remover hora do índice se existir
            if isinstance(self.data.index, pd.DatetimeIndex):
                self.data.index = self.data.index.normalize()
            
            print(f"✅ {len(self.data)} registros baixados")
            
        except Exception as e:
            # Usar dados simulados realistas se falhar
            print(f"⚠️  Usando dados simulados (acesso à internet indisponível)")
            self.data = self._generate_realistic_data(start_date, end_date)
            print(f"✅ {len(self.data)} registros simulados gerados")
        
        print(f"   Período: {self.data.index[0].date()} a {self.data.index[-1].date()}\n")
        
        return self.data
    
    def _generate_realistic_data(self, start_date, end_date) -> pd.DataFrame:
        """
        Gera dados simulados realistas baseados em histórico do SPY
        
        Args:
            start_date: Data de início
            end_date: Data de fim
        
        Returns:
            pd.DataFrame: DataFrame com dados OHLCV simulados
        """
        dates = pd.date_range(start=start_date, end=end_date, freq='B')  # B = dias úteis
        
        # Parâmetros realistas do SPY (baseado em histórico)
        preco_inicial = 550  # Próximo ao preço real do SPY
        drift = 0.0005  # Tendência diária
        volatilidade = 0.012  # Volatilidade diária (~1.2%)
        
        # Gerar retornos com random seed para reprodutibilidade
        np.random.seed(42)
        retornos = np.random.normal(drift, volatilidade, len(dates))
        
        # Gerar preços
        precos = preco_inicial * np.exp(np.cumsum(retornos))
        
        # Gerar OHLCV
        data_dict = {
            'Open': [],
            'High': [],
            'Low': [],
            'Close': [],
            'Volume': []
        }
        
        for i, preco in enumerate(precos):
            # Simular intraday com realismo
            open_price = preco * np.random.uniform(0.99, 1.01)
            close_price = preco * np.random.uniform(0.99, 1.01)
            high_price = max(open_price, close_price) * np.random.uniform(1.0, 1.015)
            low_price = min(open_price, close_price) * np.random.uniform(0.985, 1.0)
            
            data_dict['Open'].append(open_price)
            data_dict['High'].append(high_price)
            data_dict['Low'].append(low_price)
            data_dict['Close'].append(close_price)
            data_dict['Volume'].append(np.random.randint(50_000_000, 100_000_000))
        
        df = pd.DataFrame(data_dict, index=dates)
        df.index.name = 'Date'
        
        return df
    
    def calculate_variation(self) -> pd.DataFrame:
        """
        Calcula a variação percentual diária
        
        Returns:
            pd.DataFrame: DataFrame com coluna de variação percentual
        """
        self.data['pct_change'] = (
            (self.data['Close'] - self.data['Close'].shift(1)) / 
            self.data['Close'].shift(1) * 100
        )
        
        return self.data
    
    def run_strategy(self, queda_percentual: float) -> List[Dict]:
        """
        Executa a estratégia para um parâmetro específico
        
        Args:
            queda_percentual (float): Queda percentual para entrada (ex: -1.0, -2.0)
        
        Returns:
            List[Dict]: Lista de trades realizados
        """
        trades = []
        
        # Iterar sobre os dados (começando do segundo dia)
        for i in range(1, len(self.data)):
            current_date = self.data.index[i]
            prev_pct_change = self.data['pct_change'].iloc[i]
            
            # Verificar condição de entrada: queda >= queda_percentual
            if prev_pct_change <= queda_percentual:
                entry_price = self.data['Open'].iloc[i]
                exit_price = self.data['Close'].iloc[i]
                
                # Calcular retorno percentual
                retorno = ((exit_price - entry_price) / entry_price) * 100
                
                # Criar registro do trade
                trade = {
                    'data': current_date,
                    'dia_semana': current_date.strftime('%A'),
                    'queda_trigger': prev_pct_change,
                    'entrada_preco': entry_price,
                    'saida_preco': exit_price,
                    'retorno_percentual': retorno,
                    'lucro': 1 if retorno > 0 else (-1 if retorno < 0 else 0)
                }
                
                trades.append(trade)
        
        return trades
    
    def calculate_metrics(self, trades: List[Dict]) -> Dict:
        """
        Calcula métricas de performance
        
        Args:
            trades (List[Dict]): Lista de trades executados
        
        Returns:
            Dict: Dicionário com métricas de performance
        """
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
        
        # Contadores básicos
        total_trades = len(df_trades)
        acertos = len(df_trades[df_trades['lucro'] > 0])
        erros = len(df_trades[df_trades['lucro'] < 0])
        
        taxa_acerto = (acertos / total_trades * 100) if total_trades > 0 else 0.0
        taxa_erro = (erros / total_trades * 100) if total_trades > 0 else 0.0
        
        # Maiores sequências
        maior_seq_acertos = self._maior_sequencia(df_trades['lucro'], 1)
        maior_seq_erros = self._maior_sequencia(df_trades['lucro'], -1)
        
        # Drawdown máximo e retorno acumulado
        retornos = df_trades['retorno_percentual'].values
        capital_curva = self._calcular_curva_capital(retornos)
        drawdown_maximo = self._calcular_drawdown_maximo(capital_curva)
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
            'capital_curva': capital_curva
        }
    
    def _maior_sequencia(self, series: pd.Series, valor: int) -> int:
        """
        Calcula a maior sequência de um valor específico
        
        Args:
            series (pd.Series): Série de valores
            valor (int): Valor a buscar
        
        Returns:
            int: Comprimento da maior sequência
        """
        max_seq = 0
        current_seq = 0
        
        for v in series:
            if v == valor:
                current_seq += 1
                max_seq = max(max_seq, current_seq)
            else:
                current_seq = 0
        
        return max_seq
    
    def _calcular_curva_capital(self, retornos: np.ndarray) -> np.ndarray:
        """
        Calcula a curva de capital acumulada
        
        Args:
            retornos (np.ndarray): Array de retornos percentuais
        
        Returns:
            np.ndarray: Curva de capital normalizada (começando em 100)
        """
        capital = np.cumprod(1 + retornos / 100) * 100
        return capital
    
    def _calcular_drawdown_maximo(self, capital_curva: np.ndarray) -> float:
        """
        Calcula o drawdown máximo
        
        Args:
            capital_curva (np.ndarray): Curva de capital acumulada
        
        Returns:
            float: Drawdown máximo em percentual
        """
        cummax = np.maximum.accumulate(capital_curva)
        drawdown = (capital_curva - cummax) / cummax * 100
        return drawdown.min()
    
    def backtest_parametros(self, quedas: List[float]) -> pd.DataFrame:
        """
        Executa backtest para múltiplos parâmetros
        
        Args:
            quedas (List[float]): Lista de valores de queda percentual
        
        Returns:
            pd.DataFrame: Tabela de resultados
        """
        self.fetch_data()
        self.calculate_variation()
        
        print("🔄 Executando backtests para múltiplos parâmetros...\n")
        
        resultados = []
        
        for queda in quedas:
            print(f"⚙️  Testando queda_percentual = {queda}%")
            trades = self.run_strategy(queda)
            metricas = self.calculate_metrics(trades)
            
            metricas['queda_percentual'] = queda
            metricas['trades_df'] = pd.DataFrame(trades) if trades else None
            
            self.results[queda] = metricas
            resultados.append({
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
        
        df_resultados = pd.DataFrame(resultados)
        print(f"\n✅ Backtest completo!\n")
        
        return df_resultados
    
    def get_buy_hold_benchmark(self) -> float:
        """
        Calcula retorno de buy and hold no período
        
        Returns:
            float: Retorno percentual acumulado
        """
        preco_inicial = self.data['Close'].iloc[0]
        preco_final = self.data['Close'].iloc[-1]
        retorno = ((preco_final - preco_inicial) / preco_inicial) * 100
        
        return retorno
    
    def plot_equity_curve(self, queda_percentual: float, ax=None):
        """
        Plota a curva de capital para um parâmetro específico
        
        Args:
            queda_percentual (float): Valor de queda percentual
            ax: Subplot matplotlib (opcional)
        """
        if queda_percentual not in self.results:
            print(f"Nenhum resultado para queda_percentual = {queda_percentual}")
            return
        
        capital_curva = self.results[queda_percentual]['capital_curva']
        
        if ax is None:
            fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.plot(capital_curva, linewidth=2, color='#2E86AB', label='Estratégia')
        ax.axhline(y=100, color='#A23B72', linestyle='--', linewidth=1.5, 
                   label='Capital Inicial', alpha=0.7)
        ax.fill_between(range(len(capital_curva)), 100, capital_curva, 
                        alpha=0.2, color='#2E86AB')
        
        ax.set_xlabel('Número do Trade', fontsize=11, fontweight='bold')
        ax.set_ylabel('Capital Acumulado ($)', fontsize=11, fontweight='bold')
        ax.set_title(f'Curva de Capital - Queda {queda_percentual}%', 
                    fontsize=13, fontweight='bold', pad=15)
        ax.grid(True, alpha=0.3)
        ax.legend(loc='best', fontsize=10)
        
        return ax
    
    def plot_multiple_scenarios(self, quedas: List[float]):
        """
        Plota múltiplas curvas de capital
        
        Args:
            quedas (List[float]): Lista de valores de queda percentual
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        axes = axes.flatten()
        
        for idx, queda in enumerate(quedas[:4]):
            if queda in self.results:
                self.plot_equity_curve(queda, ax=axes[idx])
            else:
                axes[idx].text(0.5, 0.5, 'Sem dados', ha='center', va='center')
                axes[idx].set_title(f'Queda {queda}%')
        
        plt.tight_layout()
        return fig
    
    def plot_returns_distribution(self, queda_percentual: float, ax=None):
        """
        Plota distribuição de retornos
        
        Args:
            queda_percentual (float): Valor de queda percentual
            ax: Subplot matplotlib (opcional)
        """
        if queda_percentual not in self.results:
            print(f"Nenhum resultado para queda_percentual = {queda_percentual}")
            return
        
        trades_df = self.results[queda_percentual]['trades_df']
        
        if trades_df is None or len(trades_df) == 0:
            return
        
        if ax is None:
            fig, ax = plt.subplots(figsize=(12, 6))
        
        retornos = trades_df['retorno_percentual'].values
        cores = ['#06A77D' if r > 0 else '#D62828' for r in retornos]
        
        ax.bar(range(len(retornos)), retornos, color=cores, alpha=0.7, edgecolor='black')
        ax.axhline(y=0, color='black', linewidth=1)
        ax.axhline(y=retornos.mean(), color='#F77F00', linestyle='--', 
                  linewidth=2, label=f'Média: {retornos.mean():.2f}%')
        
        ax.set_xlabel('Número do Trade', fontsize=11, fontweight='bold')
        ax.set_ylabel('Retorno (%)', fontsize=11, fontweight='bold')
        ax.set_title(f'Distribuição de Retornos - Queda {queda_percentual}%', 
                    fontsize=13, fontweight='bold', pad=15)
        ax.grid(True, alpha=0.3, axis='y')
        ax.legend(fontsize=10)
        
        return ax
    
    def plot_comparison_buy_hold(self, queda_percentual: float):
        """
        Compara estratégia com buy and hold
        
        Args:
            queda_percentual (float): Valor de queda percentual
        """
        if queda_percentual not in self.results:
            print(f"Nenhum resultado para queda_percentual = {queda_percentual}")
            return
        
        fig, ax = plt.subplots(figsize=(14, 7))
        
        # Estratégia
        capital_estrategia = self.results[queda_percentual]['capital_curva']
        ax.plot(capital_estrategia, linewidth=2.5, color='#2E86AB', 
               label='Estratégia de Queda', marker='o', markersize=3)
        
        # Buy and Hold
        preco_inicial = self.data['Close'].iloc[0]
        precos_normalizados = self.data['Close'].values / preco_inicial * 100
        ax.plot(precos_normalizados, linewidth=2.5, color='#A23B72', 
               label='Buy & Hold', linestyle='--', marker='s', markersize=3)
        
        ax.axhline(y=100, color='gray', linewidth=1, linestyle=':', alpha=0.5)
        ax.fill_between(range(len(capital_estrategia)), 100, capital_estrategia, 
                       alpha=0.1, color='#2E86AB')
        
        ax.set_xlabel('Data (índice)', fontsize=11, fontweight='bold')
        ax.set_ylabel('Capital Acumulado ($)', fontsize=11, fontweight='bold')
        ax.set_title(f'Estratégia vs Buy & Hold - Queda {queda_percentual}%', 
                    fontsize=13, fontweight='bold', pad=15)
        ax.grid(True, alpha=0.3)
        ax.legend(loc='best', fontsize=11, framealpha=0.95)
        
        # Adicionar estatísticas no gráfico
        retorno_estrategia = self.results[queda_percentual]['retorno_acumulado']
        retorno_bh = self.get_buy_hold_benchmark()
        
        textstr = f'Estratégia: {retorno_estrategia:+.2f}%\nBuy & Hold: {retorno_bh:+.2f}%'
        ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=10,
               verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        return fig
    
    def export_trades(self, queda_percentual: float, filename: str = None):
        """
        Exporta trades para Excel
        
        Args:
            queda_percentual (float): Valor de queda percentual
            filename (str): Nome do arquivo (opcional)
        """
        if queda_percentual not in self.results:
            print(f"Nenhum resultado para queda_percentual = {queda_percentual}")
            return
        
        trades_df = self.results[queda_percentual]['trades_df']
        
        if trades_df is None:
            print("Sem trades para exportar")
            return
        
        if filename is None:
            filename = f"trades_queda_{queda_percentual}.xlsx"
        
        # Formatar DataFrame para exportação
        export_df = trades_df.copy()
        export_df['data'] = export_df['data'].dt.strftime('%Y-%m-%d')
        export_df['queda_trigger'] = export_df['queda_trigger'].apply(lambda x: f"{x:.2f}%")
        export_df['entrada_preco'] = export_df['entrada_preco'].apply(lambda x: f"${x:.2f}")
        export_df['saida_preco'] = export_df['saida_preco'].apply(lambda x: f"${x:.2f}")
        export_df['retorno_percentual'] = export_df['retorno_percentual'].apply(lambda x: f"{x:.2f}%")
        
        export_df.to_excel(filename, index=False)
        print(f"✅ Trades exportados para: {filename}")
        
        return export_df


# ============================================================================
# FUNÇÃO PRINCIPAL DE EXECUÇÃO
# ============================================================================

def main():
    """
    Função principal que executa o backtest completo
    """
    
    print("=" * 80)
    print("🚀 SISTEMA DE BACKTEST - ESTRATÉGIA QUANTITATIVA SPY".center(80))
    print("=" * 80 + "\n")
    
    # Inicializar backtester
    backtester = StrategyBacktester(ticker='SPY', days=90)
    
    # Parâmetros a testar
    quedas_testar = [-0.5, -1.0, -1.5, -2.0, -2.5]
    
    # Executar backtest
    df_resultados = backtester.backtest_parametros(quedas_testar)
    
    # Exibir tabela de resultados
    print("📊 TABELA DE RESULTADOS".center(80))
    print("-" * 80)
    print(df_resultados.to_string(index=False))
    print("-" * 80 + "\n")
    
    # Benchmark Buy & Hold
    retorno_bh = backtester.get_buy_hold_benchmark()
    print(f"📈 BENCHMARK BUY & HOLD: {retorno_bh:+.2f}%\n")
    
    # Salvar resultados em Excel
    df_resultados.to_excel('/mnt/user-data/outputs/backtest_resultados.xlsx', index=False)
    print("✅ Resultados salvos em: backtest_resultados.xlsx\n")
    
    # Exportar trades detalhados para o melhor parâmetro
    melhor_queda = quedas_testar[np.argmax([backtester.results[q]['retorno_acumulado'] 
                                            for q in quedas_testar])]
    backtester.export_trades(melhor_queda, '/mnt/user-data/outputs/trades_detalhados.xlsx')
    
    # Gerar gráficos
    print("\n📈 Gerando gráficos...\n")
    
    # Gráfico 1: Múltiplas curvas de capital
    fig1 = backtester.plot_multiple_scenarios(quedas_testar)
    fig1.savefig('/mnt/user-data/outputs/multiplas_curvas_capital.png', dpi=300, bbox_inches='tight')
    print("✅ Gráfico salvo: multiplas_curvas_capital.png")
    
    # Gráfico 2: Comparação com Buy & Hold (melhor parâmetro)
    fig2 = backtester.plot_comparison_buy_hold(melhor_queda)
    fig2.savefig('/mnt/user-data/outputs/estrategia_vs_buyhold.png', dpi=300, bbox_inches='tight')
    print("✅ Gráfico salvo: estrategia_vs_buyhold.png")
    
    # Gráfico 3: Distribuição de retornos
    fig3, ax3 = plt.subplots(figsize=(12, 6))
    backtester.plot_returns_distribution(melhor_queda, ax=ax3)
    fig3.savefig('/mnt/user-data/outputs/distribuicao_retornos.png', dpi=300, bbox_inches='tight')
    print("✅ Gráfico salvo: distribuicao_retornos.png")
    
    plt.close('all')
    
    print("\n" + "=" * 80)
    print("✅ BACKTEST CONCLUÍDO COM SUCESSO!".center(80))
    print("=" * 80)
    print(f"\n📁 Arquivos gerados em: /mnt/user-data/outputs/")
    

if __name__ == "__main__":
    main()
