# 🚀 Guia de Execução - Plataforma Interativa de Backtest

## 📋 Sumário

1. [Instalação de Dependências](#instalação)
2. [Como Executar](#execução)
3. [Navegação na Interface](#navegação)
4. [Explicação das Funcionalidades](#funcionalidades)
5. [Troubleshooting](#troubleshooting)

---

## 📦 Instalação

### Requisitos do Sistema
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação de Dependências

Execute o comando abaixo para instalar todas as dependências necessárias:

```bash
pip install streamlit plotly pandas numpy yfinance --break-system-packages
```

Ou, se preferir instalar de um arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

**Arquivo requirements.txt:**
```
streamlit==1.28.0
plotly==5.17.0
pandas==2.0.0
numpy==1.24.0
yfinance==0.2.32
matplotlib==3.7.0
```

---

## 🎬 Execução

### Opção 1: Execução Local (Recomendado)

#### Windows:
```bash
cd caminho/para/projeto
streamlit run app_backtest.py
```

#### macOS/Linux:
```bash
cd caminho/para/projeto
streamlit run app_backtest.py
```

A plataforma abrirá em seu navegador padrão em `http://localhost:8501`

### Opção 2: Especificar Porta

Se a porta 8501 já estiver em uso, especifique uma porta diferente:

```bash
streamlit run app_backtest.py --server.port 8502
```

### Opção 3: Modo de Desenvolvimento (sem cache)

Para desativar o cache durante desenvolvimento:

```bash
streamlit run app_backtest.py --logger.level=debug
```

---

## 🧭 Navegação na Interface

### Layout Principal

```
┌────────────────────────────────────────────────────────────────┐
│  🚀 Plataforma Interativa de Backtest                          │
│  Estratégia Quantitativa - SPY (S&P 500 ETF)                  │
└────────────────────────────────────────────────────────────────┘

┌─────────────────────┬──────────────────────────────────────────┐
│                     │                                          │
│  ⚙️ SIDEBAR        │        📊 AREA PRINCIPAL                │
│                     │                                          │
│  Configurações:     │  • Resumo Executivo                    │
│  • Ativo (SPY...)   │  • Tabela de Resultados                │
│  • Período (dias)   │  • Gráficos Interativos                │
│  • Parâmetros       │  • Análise Detalhada                   │
│  • Ações            │  • Insights & Recomendações            │
│                     │                                          │
└─────────────────────┴──────────────────────────────────────────┘
```

### Fluxo de Uso Básico

1. **Configure a Barra Lateral**
   - Selecione o ativo (SPY, QQQ, IWM, DIA)
   - Escolha o período em dias
   - Selecione o modo de teste (Rápido ou Customizado)

2. **Escolha os Parâmetros**
   - **Teste Rápido:** Selecione um preset pré-configurado
   - **Teste Customizado:** Insira manualmente cada threshold

3. **Execute o Backtest**
   - Clique no botão "▶️ Executar Backtest"
   - Aguarde o processamento

4. **Analise os Resultados**
   - Veja o resumo executivo
   - Explore os gráficos interativos
   - Analise os trades detalhados

---

## 🎯 Explicação das Funcionalidades

### Seção 1: Configurações (Sidebar)

#### 📈 Ativo
- **SPY:** S&P 500 ETF (recomendado para começar)
- **QQQ:** Nasdaq-100 (mais volátil)
- **IWM:** Russell 2000 (small caps)
- **DIA:** Dow Jones 30 (blue chips)

#### 📅 Período
- Quantidade de dias históricos para análise
- Range: 30 a 365 dias
- Padrão: 90 dias (3 meses)

#### 🔧 Modo de Teste

**Teste Rápido (Presets):**
- Conservador (-1.0%)
- Moderado (-0.5%)
- Agressivo (-0.25%)
- Muito Agressivo (-0.1%)
- Personalizado

**Teste Customizado:**
- Defina número de thresholds
- Configure cada threshold manualmente
- Permite máxima flexibilidade

#### 🎬 Ações
- Botão "▶️ Executar Backtest" (verde/primário)
- Inicia o processamento do backtest
- Exibe spinner durante execução

---

### Seção 2: Resumo Executivo

Exibe 4 métricas-chave no topo da página:

| Métrica | Significado |
|---------|------------|
| 📈 Buy & Hold | Retorno passivo do ativo no período |
| 🏆 Melhor Retorno | Melhor resultado entre todos os thresholds |
| 📋 Total de Trades | Quantidade total de operações |
| 🎯 Taxa de Acerto Média | Média da taxa de acerto entre os tresholds |

---

### Seção 3: Tabela de Resultados

Exibe uma tabela completa com:

| Coluna | Descrição |
|--------|-----------|
| Queda % | Threshold testado |
| Nº Trades | Total de operações |
| Acertos/Erros | Quantidade de ganhos e perdas |
| Taxa Acerto % | Percentual de trades positivos |
| Seq. Acertos | Maior sequência de vitórias |
| Retorno % | Retorno total acumulado |
| Drawdown Máx % | Maior queda no capital |
| Maior Ganho % | Trade mais lucrativo |
| Maior Perda % | Trade mais prejudicial |

---

### Seção 4: Análise Gráfica (5 Abas)

#### 📈 Aba 1: Curva de Capital
- **Gráfico:** Evolução do capital acumulado
- **Interação:** 
  - Hover para ver valores precisos
  - Zoom com click + drag
  - Duplo click para reset
- **Estatísticas:** Métricas principais abaixo do gráfico

#### 📊 Aba 2: Comparação
- **Gráfico:** Estratégia vs Buy & Hold
- **Cores:**
  - Azul: Estratégia
  - Rosa: Buy & Hold (linha tracejada)
- **Análise:** Comparação resumida ao final

#### 📉 Aba 3: Distribuição
- **Gráfico:** Histograma de retornos
- **Cores:**
  - Verde: Trades positivos
  - Vermelho: Trades negativos
- **Análise:** Linha de média incluída

#### 🎯 Aba 4: Métricas
- **Gráficos:** 4 subplots comparando:
  1. Taxa de Acerto vs Threshold
  2. Retorno Acumulado vs Threshold
  3. Número de Trades vs Threshold
  4. Drawdown Máximo vs Threshold

#### 💰 Aba 5: Detalhes dos Trades
- **Tabela:** Listagem completa de cada trade
- **Colunas:**
  - Data da operação
  - Queda que acionou o sinal
  - Preço de entrada (abertura)
  - Preço de saída (fechamento)
  - Retorno percentual
- **Download:** Botão para exportar como CSV

---

### Seção 5: Insights e Recomendações

Duas colunas com análises automáticas:

**🏆 Melhor Performance**
- Threshold com maior retorno
- Valor do retorno
- Taxa de acerto associada
- Outperformance vs benchmark

**🛡️ Menor Risco**
- Threshold com menor drawdown
- Valor do drawdown
- Número de trades
- Taxa de acerto

**📌 Recomendações Dinâmicas**
- Verifica se supera benchmark
- Avalia qualidade da taxa de acerto
- Analisa nível de risco (drawdown)

---

## 🔧 Exemplos de Uso

### Exemplo 1: Teste Rápido - Preset Moderado

1. **Sidebar:**
   - Ativo: SPY
   - Período: 90 dias
   - Modo: Teste Rápido
   - Preset: Moderado (-0.5%)

2. **Executar:** Clique em "▶️ Executar Backtest"

3. **Análise:** Veja os resultados no painel principal

**Tempo de execução:** ~5-10 segundos

---

### Exemplo 2: Teste Customizado - Múltiplos Thresholds

1. **Sidebar:**
   - Ativo: QQQ
   - Período: 120 dias
   - Modo: Teste Customizado
   - Número de thresholds: 7
   - Valores: -0.1%, -0.3%, -0.5%, -0.75%, -1.0%, -1.5%, -2.0%

2. **Executar:** Clique em "▶️ Executar Backtest"

3. **Análise:**
   - Compare a Aba 4 (Métricas) para ver o trade-off entre risco e retorno
   - Aba 2 (Comparação) mostra cada estratégia vs B&H

**Tempo de execução:** ~15-20 segundos

---

### Exemplo 3: Análise Detalhada de um Threshold Específico

1. Execute um backtest com múltiplos thresholds

2. **Curva de Capital (Aba 1):**
   - Selecione um threshold
   - Observe a evolução do capital
   - Veja estatísticas detalhadas

3. **Distribuição (Aba 3):**
   - Analise padrão de ganhos/perdas
   - Veja média, mediana, desvio padrão

4. **Detalhes (Aba 5):**
   - Liste todos os trades
   - Identifique os maiores ganhos e perdas
   - Exporte em CSV para análise adicional

---

## 🐛 Troubleshooting

### Problema 1: "ModuleNotFoundError: No module named 'streamlit'"

**Solução:**
```bash
pip install streamlit --break-system-packages
```

### Problema 2: Porta 8501 já em uso

**Solução:**
```bash
streamlit run app_backtest.py --server.port 8502
```

Ou encontre o processo usando a porta:
```bash
# Windows
netstat -ano | findstr :8501

# macOS/Linux
lsof -i :8501
```

### Problema 3: Dados não carregam (Yahoo Finance indisponível)

**Comportamento esperado:**
O sistema automaticamente usa dados simulados realistas
- Permite testar a funcionalidade mesmo sem internet
- Dados simulados têm propriedades estatísticas realistas
- Padrões identificados são válidos para análise

### Problema 4: Gráficos não aparecem

**Soluções:**
1. Limpe o cache:
   ```bash
   streamlit cache clear
   ```

2. Atualize a página no navegador (F5)

3. Use um navegador diferente

### Problema 5: Execução muito lenta

**Otimizações:**
- Use período menor (ex: 30 dias em vez de 365)
- Use menos thresholds para testar
- Feche outras aplicações

---

## 📱 Acesso Remoto

Se quiser acessar de outro computador:

### Opção 1: Exposed Server (desenvolvimento local)

```bash
streamlit run app_backtest.py \
  --server.headless true \
  --server.address 0.0.0.0
```

Acesse de outro computador em: `http://seu_ip:8501`

### Opção 2: Streamlit Cloud (produção)

1. Faça push do código para um repositório GitHub
2. Vá para https://streamlit.io/cloud
3. Conecte seu repositório
4. Seu app será servido em uma URL pública

---

## 💾 Salvando Resultados

### Exportar Trades

1. Vá para a Aba 5 (Detalhes dos Trades)
2. Selecione o threshold desejado
3. Clique em "📥 Baixar como CSV"
4. O arquivo será salvo em seu Downloads

### Capturar Gráficos

1. Clique no ícone de câmera (canto superior direito de cada gráfico)
2. O gráfico será salvo como PNG

---

## 🎓 Dicas Úteis

### Performance Melhor
- Comece com período pequeno (30 dias) para teste rápido
- Use "Teste Rápido" com presets para comparação rápida
- Use "Teste Customizado" apenas para fine-tuning

### Análise Melhor
- Compare Aba 2 e Aba 4 para decisão rápida
- Use Aba 5 para verificar trades individuais suspeitos
- Combine insights de múltiplas abas

### Validação
- Sempre compare com Buy & Hold
- Verifique se taxa de acerto > 55% (preferível > 60%)
- Analise drawdown máximo (preferível < 5%)

---

## 📞 Suporte

Para problemas ou sugestões:

1. **Logs Detalhados:**
   ```bash
   streamlit run app_backtest.py --logger.level=debug
   ```

2. **Documentação Streamlit:**
   https://docs.streamlit.io

3. **Comunidade:**
   https://discuss.streamlit.io

---

## 🔄 Atualizar Dependências

```bash
pip install --upgrade streamlit plotly pandas numpy yfinance
```

---

## ✅ Checklist de Setup Inicial

- [ ] Python 3.8+ instalado
- [ ] pip funcionando
- [ ] Dependências instaladas
- [ ] app_backtest.py no diretório correto
- [ ] Streamlit executando sem erros
- [ ] Browser abrindo em http://localhost:8501
- [ ] Sidebar visível e responsiva
- [ ] Botão "Executar Backtest" funcionando

Pronto para começar! 🚀

---

**Versão:** 1.0  
**Data:** Abril 2026  
**Autor:** Sistema de Backtest Quantitativo
