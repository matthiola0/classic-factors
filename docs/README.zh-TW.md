# classic-factors

> **Languages**: [English](../README.md) · **繁體中文**

我把兩個最經典的股票因子策略 —— 12-1 動量、1-週反轉 —— 用同一條 pipeline 跑過三個市場：美股 S&P 500、台股 0050、流動性 top 25 USDT pairs。真正在意的不是因子在學術 paper 裡有沒有出現，而是扣完各市場真實交易成本後還剩多少。

研究框架：[`qtools`](https://github.com/matthiola0/qtools)。

## Headline 結果

2 因子 × 3 市場、扣完各市場真實成本後的 Net Sharpe：

| | 動量（月頻）| 反轉（週頻）|
|---|---:|---:|
| 美股（S&P 500）| −0.04 | +0.10 |
| 台股（0050）| **+0.68** | −1.60 |
| 加密（top 25）| +0.26 | −0.80 |

6 格中真正可交易（扣成本後）的只有一格 —— **台股動量**。美股大型股動量在 post-2015 已 decay 到雜訊；台股反轉是矩陣中 *毛訊號最強* 的一格，但每筆賣出 0.3% 證交稅 × 週頻再平衡 → 約 35%/年 成本拖累，把它變成 *淨 Sharpe 最差* 的一格。加密反轉在所有 regime 下都負；加密動量 regime-dependent、不是 standalone alpha。

## 研究問題

我真正想搞清楚的是：同一個訊號在不同市場交易，會表現得多不一樣？台股、美股大型股、加密的成本結構差距很大，本來就預期答案會分歧 —— 結果差距比看 gross IC 表會猜的還更大。

## 範圍

| 因子 | 定義 | 再平衡 |
|---|---|---|
| 12-1 動量 | 過去 12 個月報酬扣除最近 1 個月 | 月頻 |
| 1-週反轉 | 過去 1 週報酬取負 | 週頻 |

| 市場 | 股票池 | 期間 | 成本模型 |
|---|---|---|---|
| 美股 | 502 檔當前 S&P 500 成分股 | 2015-01 → 2025-07 | 單邊 5 bps |
| 台股 | 50 檔當前 0050 成分股 | 2015-01 → 2025-07 | 來回 46 bps（單邊 3 bps 手續費 + 5 bps 滑價，賣方加 30 bps 證交稅） |
| 加密 | 成交量 top 25 USDT pairs | 2017-08 → 2025-07 | 單邊 10 bps |

## 限制

- **存活者偏差**：使用當前成分股；下市 / 剔除的標的缺失。
- **僅限價量因子**：因子限於可由 OHLCV 計算者；基本面因子（價值：P/B、P/E）刻意 out-of-scope。
- **簡化成本模型**：固定 bps 單邊，沒有 market-impact 或 per-security 異質性。
- **加密池**：請求 top 30 USDT pairs，但只有 25 檔有回溯到 2017-08 的完整歷史，回測用此 25 檔。

## 結果

### 12-1 動量（[notebook 01](../notebooks/01_momentum.ipynb)）

| 市場 | IC mean | IC IR | LS Sharpe（淨）| 年化報酬 | MDD |
|---|---|---|---|---|---|
| 美股（S&P 500）| −0.002 | −0.01 | −0.04 | −2.5% | −42% |
| **台股（0050）**| **+0.046** | **+0.18** | **+0.68** | **+12.4%** | −38% |
| 加密（top 25）| +0.004 | +0.01 | +0.26 | −2.6% | −87% |

美股大型股的經典動量在 post-2015 已經 decay 到雜訊（IC −0.002、跟亂猜差不多）—— 跟 McLean & Pontiff (2016) 在 factor crowding 文獻裡記錄的一致，沒什麼意外。台股不一樣：IC +0.046、net Sharpe 0.68，2020 COVID 反彈那年最強（+1.96）。我的解讀是散戶比例高 + 機構套利不及美股大型股，機制還沒被套乾。加密動量則 regime-dependent：2021-22 熊市 +1.39 Sharpe（空頭出力）、2023-25 牛市倒轉到 −0.57。沒 regime filter 就不算 standalone alpha。

![12-1 動量跨市場淨累積報酬](../reports/figures/01_momentum_backtest.png)

### 1-週反轉（[notebook 02](../notebooks/02_reversal.ipynb)）

| 市場 | IC mean | Gross Sharpe | Net Sharpe | 年成本拖累 |
|---|---|---|---|---|
| 美股（S&P 500）| +0.014 | +0.56 | +0.10 | ~8% |
| 台股（0050）| +0.027 | +0.17 | **−1.60** | ~35% |
| 加密（top 25）| −0.013 | −0.67 | −0.80 | ~15% |

美股反轉確實有毛 alpha（gross Sharpe +0.56），但成本幾乎全吃光（net +0.10）—— 訊號存在、只是無法落地。台股版更極端：反轉的 gross IC 在整個 6 格矩陣中最強，但 0.3% 證交稅一年複合 ~52 次，產生 ~35%/年 成本拖累，把它變成 −1.60 net Sharpe 的災難 —— *gross 最強的那格、淨值卻最差*。加密在週頻就是個動量市，反轉 IC 在所有 regime 下都負。

![週頻反轉跨市場：毛（虛線）vs 淨（實線）](../reports/figures/02_reversal_gross_vs_net.png)

### 跨因子 × 跨市場（[notebook 99](../notebooks/99_summary.ipynb)）

Net Sharpe 矩陣（2 因子 × 3 市場）：

| | 動量（月頻）| 反轉（週頻）|
|---|---|---|
| 美股 | −0.04 | +0.10 |
| 台股 | **+0.68** | −1.60 |
| 加密 | +0.26 | −0.80 |

![Net Sharpe 矩陣：2 因子 × 3 市場](../reports/figures/99_sharpe_heatmap.png)

在每個市場裡，動量跟反轉接近不相關（|ρ| < 0.1） —— 它們確實捕捉不同 horizon。但這個獨立性沒讓 50/50 組合更好看：當其中一條腿深度負時，平均下去只是把贏家拖下水。6 格裡真正可交易的只有一格：台股動量。

## 結構

```
classic-factors/
├── src/factors/signals.py        # 因子訊號函式
├── scripts/
│   └── download_data.py          # 填充 qtools cache
├── notebooks/
│   ├── 01_momentum.ipynb
│   ├── 02_reversal.ipynb
│   └── 99_summary.ipynb
└── reports/figures/              # notebook 執行時生成
```

## Notebook 導覽

- [`01_momentum.ipynb`](../notebooks/01_momentum.ipynb) — 12-1 動量跑三個市場、IC + 毛/淨 Sharpe + 逐年表現 + 累積淨報酬曲線。台股 Sharpe 0.68 vs 美股 −0.04 的對比就在這。
- [`02_reversal.ipynb`](../notebooks/02_reversal.ipynb) — 1-週反轉跑同三個市場。重點圖是 gross-vs-net Sharpe by market 的對照，台股 35%/年 成本拖累一眼可見。
- [`99_summary.ipynb`](../notebooks/99_summary.ipynb) — 跨因子 × 跨市場 Sharpe heatmap、動量 vs 反轉相關性面板、50/50 組合 sanity check —— *只有台股動量真正可交易* 的結論在這裡收斂。

## 重現

```bash
# clone + 安裝（qtools 透過 pyproject.toml 自動拉）
git clone https://github.com/matthiola0/classic-factors
cd classic-factors
pip install -e .

# 填充價格快取（~60 MB，首次執行 ~45s）
python scripts/download_data.py

# 重新執行 notebooks
jupyter nbconvert --to notebook --execute notebooks/*.ipynb --inplace
```

**本地開發**：若有 [`qtools`](https://github.com/matthiola0/qtools) 本地 clone 想邊改邊用而不 push，安裝後執行 `pip install -e ../qtools` 覆寫 git-installed 版本為 editable 本地版本。

## 參考文獻

研究遵循以下經典公式：

**動量**
- Jegadeesh, N., & Titman, S. (1993). Returns to buying winners and selling losers:
  Implications for stock market efficiency. *Journal of Finance*, 48(1), 65–91.
  [doi:10.1111/j.1540-6261.1993.tb04702.x](https://doi.org/10.1111/j.1540-6261.1993.tb04702.x)
- Asness, C. S., Moskowitz, T. J., & Pedersen, L. H. (2013). Value and momentum
  everywhere. *Journal of Finance*, 68(3), 929–985.
  [doi:10.1111/jofi.12021](https://doi.org/10.1111/jofi.12021)

**短期反轉**
- Jegadeesh, N. (1990). Evidence of predictable behavior of security returns.
  *Journal of Finance*, 45(3), 881–898.
  [doi:10.1111/j.1540-6261.1990.tb05110.x](https://doi.org/10.1111/j.1540-6261.1990.tb05110.x)
- Nagel, S. (2012). Evaporating liquidity. *Review of Financial Studies*, 25(7),
  2005–2039. [doi:10.1093/rfs/hhs066](https://doi.org/10.1093/rfs/hhs066)
  — 把短期反轉利潤詮釋為流動性提供的補償，正好對應 *美股毛訊號被現實成本吃光* 這個結果。

**因子衰減 & 成本調整報酬**
- Novy-Marx, R., & Velikov, M. (2016). A taxonomy of anomalies and their trading
  costs. *Review of Financial Studies*, 29(1), 104–147.
  [doi:10.1093/rfs/hhv063](https://doi.org/10.1093/rfs/hhv063)
- McLean, R. D., & Pontiff, J. (2016). Does academic research destroy stock return
  predictability? *Journal of Finance*, 71(1), 5–32.
  [doi:10.1111/jofi.12365](https://doi.org/10.1111/jofi.12365)
