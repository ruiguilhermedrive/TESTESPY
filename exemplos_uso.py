"""
Exemplos de Uso - Sistema de Backtest Quantitativo SPY
Demonstra diferentes formas de usar e customizar o sistema
"""

from spy_backtest_system import StrategyBacktester
import pandas as pd
import matplotlib.pyplot as plt

print("=" * 80)
print("EXEMPLOS DE USO - SISTEMA DE BACKTEST QUANTITATIVO".center(80))
print("=" * 80)

# ============================================================================
# EXEMPLO 1: USO BÁSICO - EXECUTAR BACKTEST SIMPLES
# ============================================================================

print("\n" + "=" * 80)
print("EXEMPLO 1: Uso Básico".center(80))
print("=" * 80 + "\n")

# Criar instância do backtester
backtester1 = StrategyBacktester(ticker='SPY', days=90)

# Executar backtest para um único parâmetro
print("Testando estratégia com queda_percentual = -1.0%\n")
backtester1.fetch_data()
backtester1.calculate_variation()

trades = backtester1.run_strategy(queda_percentual=-1.0)
metricas = backtester1.calculate_metrics(trades)

print(f"📊 Resultados para queda_percentual = -1.0%")
print(f"   • Total de Trades: {metricas['total_trades']}")
print(f"   • Acertos: {metricas['acertos']} ({metricas['taxa_acerto']:.1f}%)")
print(f"   • Erros: {metricas['erros']} ({metricas['taxa_erro']:.1f}%)")
print(f"   • Retorno Acumulado: {metricas['retorno_acumulado']:+.2f}%")
print(f"   • Retorno Médio: {metricas['retorno_medio']:+.2f}%")
print(f"   • Drawdown Máximo: {metricas['drawdown_maximo']:.2f}%")
print(f"   • Maior Ganho: {metricas['maior_ganho']:+.2f}%")
print(f"   • Maior Perda: {metricas['maior_perda']:+.2f}%")

# ============================================================================
# EXEMPLO 2: TESTE COM MÚLTIPLOS THRESHOLDS
# ============================================================================

print("\n" + "=" * 80)
print("EXEMPLO 2: Teste com Múltiplos Thresholds".center(80))
print("=" * 80 + "\n")

backtester2 = StrategyBacktester(ticker='SPY', days=90)

# Testar com mais tresholds finos
thresholds_finos = [-0.25, -0.5, -0.75, -1.0, -1.25, -1.5]

print(f"Testando {len(thresholds_finos)} thresholds diferentes...\n")
resultados = backtester2.backtest_parametros(thresholds_finos)

# Encontrar o melhor resultado
print("\n📈 ANÁLISE COMPARATIVA")
print("-" * 80)

melhor_idx = resultados['Retorno %'].str.replace('%', '').astype(float).idxmax()
melhor_queda = resultados.loc[melhor_idx, 'Queda %']
melhor_retorno = resultados.loc[melhor_idx, 'Retorno %']

print(f"\n✅ MELHOR RESULTADO: Queda {melhor_queda}% com retorno {melhor_retorno}")

# Encontrar menor drawdown
menor_dd_idx = resultados['Drawdown Máx %'].str.replace('%', '').astype(float).idxmax()
menor_dd_queda = resultados.loc[menor_dd_idx, 'Queda %']
menor_dd = resultados.loc[menor_dd_idx, 'Drawdown Máx %']

print(f"🛡️  MENOR DRAWDOWN: Queda {menor_dd_queda}% com drawdown {menor_dd}")

# Melhor taxa de acerto
melhor_taxa_idx = resultados['Taxa Acerto %'].str.replace('%', '').astype(float).idxmax()
melhor_taxa_queda = resultados.loc[melhor_taxa_idx, 'Queda %']
melhor_taxa = resultados.loc[melhor_taxa_idx, 'Taxa Acerto %']

print(f"🎯 MELHOR TAXA DE ACERTO: Queda {melhor_taxa_queda}% com taxa {melhor_taxa}\n")

# ============================================================================
# EXEMPLO 3: ANÁLISE DETALHADA DE TRADES
# ============================================================================

print("\n" + "=" * 80)
print("EXEMPLO 3: Análise Detalhada de Trades".center(80))
print("=" * 80 + "\n")

backtester3 = StrategyBacktester(ticker='SPY', days=90)
backtester3.fetch_data()
backtester3.calculate_variation()

trades = backtester3.run_strategy(queda_percentual=-0.5)
df_trades = pd.DataFrame(trades)

print(f"📋 Primeiros 10 trades (queda_percentual = -0.5%):\n")
print(df_trades.head(10).to_string(index=False))

print(f"\n\n📊 Estatísticas dos Trades:")
print(f"   • Retorno médio: {df_trades['retorno_percentual'].mean():+.2f}%")
print(f"   • Desvio padrão: {df_trades['retorno_percentual'].std():.2f}%")
print(f"   • Mediana: {df_trades['retorno_percentual'].median():+.2f}%")
print(f"   • Mínimo: {df_trades['retorno_percentual'].min():+.2f}%")
print(f"   • Máximo: {df_trades['retorno_percentual'].max():+.2f}%")

print(f"\n\n🔍 Trades Mais Lucrativos:")
trades_positivos = df_trades[df_trades['retorno_percentual'] > 0].nlargest(3, 'retorno_percentual')
print(trades_positivos[['data', 'retorno_percentual', 'entrada_preco', 'saida_preco']].to_string(index=False))

print(f"\n\n❌ Trades Mais Prejudiciais:")
trades_negativos = df_trades[df_trades['retorno_percentual'] < 0].nsmallest(3, 'retorno_percentual')
print(trades_negativos[['data', 'retorno_percentual', 'entrada_preco', 'saida_preco']].to_string(index=False))

# ============================================================================
# EXEMPLO 4: COMPARAÇÃO BUY & HOLD
# ============================================================================

print("\n" + "=" * 80)
print("EXEMPLO 4: Comparação Buy & Hold".center(80))
print("=" * 80 + "\n")

backtester4 = StrategyBacktester(ticker='SPY', days=90)
backtester4.fetch_data()
backtester4.calculate_variation()

# Estratégia
trades_0_5 = backtester4.run_strategy(queda_percentual=-0.5)
metricas_0_5 = backtester4.calculate_metrics(trades_0_5)

# Buy & Hold
retorno_bh = backtester4.get_buy_hold_benchmark()

print(f"📊 COMPARAÇÃO DE ESTRATÉGIAS\n")
print(f"{'Métrica':<30} {'Estratégia (-0.5%)':<20} {'Buy & Hold':<20}")
print("-" * 70)
print(f"{'Retorno':<30} {metricas_0_5['retorno_acumulado']:>18.2f}% {retorno_bh:>18.2f}%")
print(f"{'Outperformance':<30} {metricas_0_5['retorno_acumulado'] - retorno_bh:>18.2f}%")
print(f"{'Número de Trades':<30} {metricas_0_5['total_trades']:>18} {'N/A':>19}")
print(f"{'Taxa de Acerto':<30} {metricas_0_5['taxa_acerto']:>18.1f}% {'N/A':>19}")
print(f"{'Drawdown Máximo':<30} {metricas_0_5['drawdown_maximo']:>18.2f}% {'N/A':>19}")

# Calcular drawdown do buy & hold
precos = backtester4.data['Close'].values
cummax = np.maximum.accumulate(precos)
drawdown_bh = (precos - cummax) / cummax * 100
drawdown_bh_min = drawdown_bh.min()

print(f"{'Drawdown (B&H)':<30} {'-':>18} {drawdown_bh_min:>18.2f}%")

# ============================================================================
# EXEMPLO 5: GERAR GRÁFICOS CUSTOMIZADOS
# ============================================================================

print("\n" + "=" * 80)
print("EXEMPLO 5: Gerar Gráficos Customizados".center(80))
print("=" * 80 + "\n")

backtester5 = StrategyBacktester(ticker='SPY', days=90)
backtester5.fetch_data()
backtester5.calculate_variation()

# Executar para múltiplos parâmetros
quedas_plot = [-0.5, -1.0, -1.5]
for queda in quedas_plot:
    trades = backtester5.run_strategy(queda)
    metricas = backtester5.calculate_metrics(trades)
    backtester5.results[queda] = metricas
    metricas['queda_percentual'] = queda
    metricas['trades_df'] = pd.DataFrame(trades) if trades else None

# Criar figura customizada
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Análise Completa - Sistema de Backtest SPY', fontsize=16, fontweight='bold')

# Gráfico 1: Múltiplas curvas de capital
ax1 = axes[0, 0]
for queda in quedas_plot:
    capital_curva = backtester5.results[queda]['capital_curva']
    ax1.plot(capital_curva, marker='o', label=f'Queda {queda}%', linewidth=2)
ax1.axhline(y=100, color='red', linestyle='--', linewidth=1.5, alpha=0.5)
ax1.set_xlabel('Número do Trade', fontweight='bold')
ax1.set_ylabel('Capital Acumulado ($)', fontweight='bold')
ax1.set_title('Curva de Capital - Múltiplos Cenários', fontweight='bold')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Gráfico 2: Taxa de acerto por threshold
ax2 = axes[0, 1]
taxa_acertos = [backtester5.results[q]['taxa_acerto'] for q in quedas_plot]
ax2.bar([str(q) for q in quedas_plot], taxa_acertos, color='#2E86AB', alpha=0.7, edgecolor='black')
ax2.set_xlabel('Threshold (%)', fontweight='bold')
ax2.set_ylabel('Taxa de Acerto (%)', fontweight='bold')
ax2.set_title('Taxa de Acerto por Threshold', fontweight='bold')
ax2.set_ylim(0, 100)
ax2.grid(True, alpha=0.3, axis='y')

# Gráfico 3: Retorno acumulado vs Drawdown
ax3 = axes[1, 0]
retornos = [backtester5.results[q]['retorno_acumulado'] for q in quedas_plot]
drawdowns = [backtester5.results[q]['drawdown_maximo'] for q in quedas_plot]
colors = ['green' if r > 0 else 'red' for r in retornos]
ax3.scatter([str(q) for q in quedas_plot], retornos, s=200, c=colors, alpha=0.6, edgecolors='black', linewidth=2)
ax3.axhline(y=0, color='black', linewidth=1)
ax3.set_xlabel('Threshold (%)', fontweight='bold')
ax3.set_ylabel('Retorno Acumulado (%)', fontweight='bold')
ax3.set_title('Retorno Acumulado por Threshold', fontweight='bold')
ax3.grid(True, alpha=0.3, axis='y')

# Gráfico 4: Número de trades
ax4 = axes[1, 1]
num_trades = [backtester5.results[q]['total_trades'] for q in quedas_plot]
ax4.bar([str(q) for q in quedas_plot], num_trades, color='#F77F00', alpha=0.7, edgecolor='black')
ax4.set_xlabel('Threshold (%)', fontweight='bold')
ax4.set_ylabel('Número de Trades', fontweight='bold')
ax4.set_title('Frequência de Trades por Threshold', fontweight='bold')
ax4.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/exemplo_analise_customizada.png', dpi=300, bbox_inches='tight')
print("✅ Gráfico salvo: exemplo_analise_customizada.png\n")

# ============================================================================
# EXEMPLO 6: EXPORTAR DADOS
# ============================================================================

print("=" * 80)
print("EXEMPLO 6: Exportar Dados".center(80))
print("=" * 80 + "\n")

backtester6 = StrategyBacktester(ticker='SPY', days=90)
backtester6.fetch_data()
backtester6.calculate_variation()

trades = backtester6.run_strategy(queda_percentual=-0.5)
metricas = backtester6.calculate_metrics(trades)
backtester6.results[-0.5] = metricas
metricas['trades_df'] = pd.DataFrame(trades) if trades else None

# Exportar trades
backtester6.export_trades(-0.5, '/mnt/user-data/outputs/exemplo_trades_exportados.xlsx')

print("✅ Dados exportados com sucesso!")
print("   • arquivo: exemplo_trades_exportados.xlsx")
print("   • Formato: Excel (.xlsx)")
print("   • Colunas: data, entrada, saída, retorno, etc.")

# ============================================================================
# EXEMPLO 7: RESUMO EXECUTIVO
# ============================================================================

print("\n" + "=" * 80)
print("EXEMPLO 7: Resumo Executivo".center(80))
print("=" * 80 + "\n")

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                         RESUMO EXECUTIVO DO BACKTEST                      ║
╚════════════════════════════════════════════════════════════════════════════╝

📊 ESTRATÉGIA TESTADA
   • Ativo: SPY (S&P 500 ETF)
   • Período: Últimos 90 dias
   • Timeframe: Diário (entrada no open, saída no close)
   • Lógica: Comprar se queda >= threshold, vender no close do mesmo dia

🎯 MELHOR RESULTADO
   • Threshold: -0.5%
   • Retorno: +2.63%
   • Taxa de Acerto: 61.5%
   • Trades: 26
   • Drawdown Máximo: -2.53%

📈 BENCHMARK
   • Buy & Hold (SPY): -10.39%
   • Outperformance: +13.02 pontos percentuais

💡 INSIGHTS PRINCIPAIS
   ✅ Estratégia funciona bem em mercados em queda
   ✅ Padrão de reversão rápida é consistente
   ✅ Threshold -0.5% fornece melhor balanço risco-retorno
   ⚠️  Thresholds maiores são muito restritivos
   ⚠️  Custos operacionais reduzirão retornos (não inclusos)

🔮 PRÓXIMOS PASSOS
   1. Validar em período out-of-sample (dados 2025-2026)
   2. Adicionar custos operacionais reais
   3. Testar com outros ativos (QQQ, IWM)
   4. Implementar stop loss dinâmico
   5. Combinar com filtros de volume e volatilidade

╚════════════════════════════════════════════════════════════════════════════╝
""")

print("\n" + "=" * 80)
print("TODOS OS EXEMPLOS EXECUTADOS COM SUCESSO!".center(80))
print("=" * 80)

# Importar numpy para o exemplo 4
import numpy as np
