# MOEX Trading Signal Bot

Сигнальный торговый бот для Московской биржи на Python с использованием
T-Invest API, SQLite и библиотеки `smartmoneyconcepts`.

Проект предназначен для анализа рынка, формирования торговых сигналов и
управления пользовательским портфелем по стратегии **Dynamic Swing
Momentum**.

> **Важно:** первая версия проекта не выполняет реальные сделки
> автоматически. Она анализирует рынок, портфель и формирует сигналы
> `BUY / ADD / HOLD / REDUCE / SELL`. Исполнение через T-Invest Sandbox
> используется для тестирования алгоритма. Переход к реальной торговле
> рассматривается только после отдельной проверки стратегии.

------------------------------------------------------------------------

## 1. Цель проекта

Создать систему, которая:

1.  получает рыночные данные через T-Invest API;
2.  сохраняет исторические данные в SQLite;
3.  анализирует IMOEX и определяет режим рынка;
4.  определяет относительную силу секторов;
5.  формирует список потенциально сильных акций;
6.  рассчитывает технические показатели;
7.  использует SMC-признаки (`Swing High/Low`, `BOS`, `CHoCH`, `FVG`,
    `Liquidity`, `Order Blocks`) как дополнительные признаки;
8.  ищет два основных сетапа:
    -   Breakout;
    -   Pullback;
9.  анализирует текущий пользовательский портфель;
10. рассчитывает риск и рекомендуемый размер позиции;
11. формирует сигнал:

-   `BUY`;
-   `ADD`;
-   `HOLD`;
-   `REDUCE`;
-   `SELL`;

12. отправляет сигнал пользователю через Telegram;
13. записывает каждый сигнал и результат в БД;
14. позволяет тестировать стратегию на исторических данных и в Sandbox.

------------------------------------------------------------------------

## 2. Основа торговой стратегии

Стратегия из исходного ТЗ использует горизонт преимущественно **3--20
торговых дней**, 5--7 открытых позиций и адаптацию размера позиции к
рыночному режиму. fileciteturn0file0L1-L7

Основная последовательность:

``` text
IMOEX
  ↓
Market Regime
  ↓
Sector Rotation
  ↓
Stock Ranking
  ↓
Breakout / Pullback
  ↓
SMC confirmation
  ↓
Risk Management
  ↓
BUY / ADD / HOLD / REDUCE / SELL
```

Стратегия не должна использовать фиксированный стоп `-7%`, механическое
усреднение убыточной позиции или попытку заранее угадать
сектор-победитель. fileciteturn0file0L205-L217

------------------------------------------------------------------------

# 3. Архитектура

``` text
                    ┌──────────────────────┐
                    │     T-Invest API     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Data Collector    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │       SQLite         │
                    └──────────┬───────────┘
                               │
             ┌─────────────────┼──────────────────┐
             ▼                 ▼                  ▼
      Market Analyzer   Sector Analyzer    Portfolio Manager
             │                 │                  │
             └─────────────────┼──────────────────┘
                               ▼
                    ┌──────────────────────┐
                    │   Technical Engine   │
                    │ EMA / ATR / Momentum │
                    │ Volume / RS / SMC    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Strategy Engine    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     Risk Manager     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Signal Generator   │
                    └──────────┬───────────┘
                               │
                    ┌──────────┴───────────┐
                    ▼                      ▼
             Telegram Bot          Backtest Engine
```

------------------------------------------------------------------------

# 4. Технологический стек

## Основной язык

-   Python 3.11+

## API

-   T-Invest API
-   официальный Python SDK

T-Invest API предоставляет исторические и потоковые рыночные данные, а
также возможность тестировать торговые алгоритмы. Сам механизм проверки
торговой гипотезы на исторических данных клиент реализует
самостоятельно. citeturn0search11turn0search2

## База данных

-   SQLite
-   SQLAlchemy

SQLite используется как основная БД первой версии проекта.

## Анализ данных

-   pandas
-   numpy

## Технический анализ

-   собственные расчёты:
    -   EMA 20/50/200;
    -   ATR;
    -   Momentum;
    -   Relative Strength;
    -   Volume analysis.

## SMC

-   `smartmoneyconcepts`

Библиотека работает с OHLC/OHLCV DataFrame и предоставляет функции для
Swing High/Low, BOS/CHoCH, FVG, Order Blocks, Liquidity, Previous
High/Low и Retracements.

Источник: https://github.com/joshyattridge/smart-money-concepts

## Telegram

-   aiogram

## Тестирование

-   pytest

## Конфигурация

-   `.env`
-   `pydantic-settings`

------------------------------------------------------------------------

# 5. Рыночные данные

Основным источником данных является T-Invest API.

Для проекта нужны:

-   список инструментов;
-   ticker;
-   instrument UID;
-   FIGI при необходимости;
-   OHLCV;
-   последние цены;
-   объём;
-   состояние инструмента;
-   данные портфеля;
-   позиции;
-   операции;
-   данные Sandbox.

Метод `GetCandles` предоставляет исторические свечи и поддерживает
интервалы от секунд/минут до часов, дней, недель и месяцев.
citeturn0search3

------------------------------------------------------------------------

# 6. Таймфреймы

Для первой реализации использовать:

``` text
D1  — основной анализ тренда и структуры
H4  — промежуточная структура
H1  — поиск точки входа
```

Таймфреймы являются архитектурным решением проекта, а не отдельным
правилом исходного файла стратегии.

Общий принцип:

``` text
D1 → направление
H4 → структура
H1 → вход
```

------------------------------------------------------------------------

# 7. Market Regime

IMOEX классифицируется как:

``` text
BULL
NEUTRAL
BEAR
```

Стратегия использует:

-   направление IMOEX;
-   EMA 20;
-   EMA 50;
-   EMA 200;
-   структуру максимумов/минимумов;
-   breadth;
-   объём.

Для Bull предусмотрено 70--100% капитала в акциях, для Neutral ---
40--70%, для Bear --- 0--40%. fileciteturn0file0L13-L26

В коде это должно быть отдельным модулем:

``` text
market_regime.py
```

Пример результата:

``` python
MarketRegime(
    regime="BULL",
    score=0.82,
    exposure_min=0.70,
    exposure_max=1.00
)
```

Точные численные пороги для определения режима должны быть вынесены в
конфигурацию и проверены бэктестом.

------------------------------------------------------------------------

# 8. Sector Analyzer

Раз в неделю система пересчитывает относительную силу секторов.

Базовые группы:

-   нефть и газ;
-   банки;
-   IT;
-   металлургия;
-   золото;
-   потребительский сектор;
-   другие ликвидные группы.

Стратегия предусматривает поиск сильных секторов и работу
преимущественно с сильными бумагами внутри них.
fileciteturn0file0L29-L40

Результат:

``` python
SectorMetric(
    sector="BANKS",
    relative_strength=0.78,
    momentum=0.64,
    volume_score=0.71
)
```

------------------------------------------------------------------------

# 9. Stock Ranking

Из сильных секторов формируется список примерно из 10--15 кандидатов.

Для каждой акции рассчитываются:

-   Relative Strength;
-   Momentum;
-   Volume;
-   ATR;
-   положение относительно EMA 20/50/200;
-   расстояние до сопротивления;
-   корпоративные/фундаментальные катализаторы при наличии данных.

После этого остаётся 5--7 наиболее подходящих кандидатов.
fileciteturn0file0L46-L57

В коде:

``` text
stock_ranker.py
```

------------------------------------------------------------------------

# 10. Technical Engine

Модуль рассчитывает:

``` text
EMA20
EMA50
EMA200
ATR
Momentum
Relative Strength
Volume Ratio
Swing High
Swing Low
```

Дополнительно:

``` text
BOS
CHoCH
FVG
Order Block
Liquidity
Retracement
Previous High/Low
```

SMC-признаки используются как **дополнительные подтверждения**, а не как
самостоятельная торговая стратегия.

------------------------------------------------------------------------

# 11. Интеграция smart-money-concepts

Пример обработки:

``` python
from smartmoneyconcepts import smc

swings = smc.swing_highs_lows(
    ohlc,
    swing_length=50
)

bos_choch = smc.bos_choch(
    ohlc,
    swings,
    close_break=True
)

fvg = smc.fvg(
    ohlc,
    join_consecutive=False
)

order_blocks = smc.ob(
    ohlc,
    swings
)

liquidity = smc.liquidity(
    ohlc,
    swings
)
```

Полученные признаки передаются в `Strategy Engine`.

Важно: параметры `swing_length`, `range_percent` и другие параметры SMC
не должны приниматься как оптимальные заранее. Они являются параметрами
стратегии и должны проверяться на исторических данных.

------------------------------------------------------------------------

# 12. Breakout Setup

Основная логика:

``` text
Цена подходит к важному сопротивлению
        ↓
Происходит пробой
        ↓
Объём увеличивается
        ↓
BOS подтверждает изменение структуры
        ↓
Цена удерживается выше уровня
        ↓
BUY
```

Необходимо отдельно определить в коде:

-   что является сопротивлением;
-   минимальное расстояние до уровня;
-   что считается пробоем;
-   минимальный объём;
-   требуется ли закрытие свечи выше уровня;
-   как используется BOS;
-   допустимый размер свечи;
-   максимальное отклонение от уровня.

Эти параметры должны быть конфигурационными.

------------------------------------------------------------------------

# 13. Pullback Setup

Основная логика:

``` text
Восходящий тренд
      ↓
Коррекция
      ↓
EMA20 / EMA50
или бывшее сопротивление
      ↓
Подтверждение разворота
      ↓
SMC confirmation
      ↓
BUY
```

Стратегия прямо предусматривает вход после подтверждённого разворота, а
не покупку вертикально выросшей бумаги из-за FOMO.
fileciteturn0file0L59-L69

------------------------------------------------------------------------

# 14. SMC как фильтр

Необходимо реализовать отдельный компонент:

``` text
smc_confirmation.py
```

Он не выдаёт BUY напрямую.

Он возвращает признаки:

``` python
SMCConfirmation(
    bullish_structure=True,
    bos=True,
    choch=False,
    fvg_present=True,
    liquidity_sweep=True,
    order_block=True
)
```

Затем Strategy Engine решает, насколько эти признаки подтверждают сетап.

------------------------------------------------------------------------

# 15. Entry Engine

Вход осуществляется частями:

``` text
30–40% → первый подтверждённый сигнал
30%    → подтверждение
остаток → продолжение тренда
```

Добавление разрешено только к прибыльной/подтверждённой позиции.

Убыточную позицию нельзя автоматически усреднять.
fileciteturn0file0L72-L80

Для сигнала необходимо рассчитывать:

``` text
entry_price
stop_price
risk_per_share
allowed_risk
position_size
```

------------------------------------------------------------------------

# 16. Risk Manager

Базовый риск:

``` text
1–1.5% капитала на сделку
```

Для капитала 100 000 ₽:

``` text
1%   = 1 000 ₽
1.5% = 1 500 ₽
```

Размер позиции определяется от расстояния до стопа, а не наоборот.
fileciteturn0file0L83-L104

Формула:

``` text
Risk = |Entry - Stop| × Quantity
```

Количество:

``` text
Quantity = AllowedRisk / |Entry - Stop|
```

При этом количество должно округляться с учётом размера лота.

------------------------------------------------------------------------

# 17. Stop Loss

Стоп определяется:

-   по последнему значимому swing low/high;
-   либо по ATR;
-   с учётом нормальной волатильности.

После открытия позиции стоп нельзя автоматически расширять.
fileciteturn0file0L88-L104

Не использовать универсальное правило:

``` text
Stop = Entry - 7%
```

------------------------------------------------------------------------

# 18. Управление прибылью

Приблизительная логика стратегии:

``` text
+8–12%
   ↓
частичная фиксация
+
перестановка/ужесточение стопа

+15–25%
   ↓
дополнительная фиксация
+
оставшаяся часть сопровождается trailing stop
```

Сильную позицию не нужно полностью закрывать только из-за достижения
фиксированной цели. fileciteturn0file0L107-L116

Все проценты должны быть конфигурационными.

------------------------------------------------------------------------

# 19. Portfolio Manager

Бот должен знать текущее состояние портфеля.

Для каждой позиции:

``` text
ticker
quantity
average_price
current_price
market_value
unrealized_pnl
pnl_percent
entry_date
stop_price
risk
```

Портфель должен оцениваться целиком.

Ограничения стратегии:

``` text
5–7 открытых позиций
20–25% максимум в одной позиции
40–50% максимум в одном секторе
```

Также контролируется общий первоначальный риск.
fileciteturn0file0L147-L168

------------------------------------------------------------------------

# 20. Сигналы

Система должна поддерживать пять основных сигналов:

### BUY

Новая позиция.

### ADD

Добавление к существующей прибыльной позиции после подтверждения.

### HOLD

Позиция сохраняется без изменения.

### REDUCE

Частичное сокращение позиции.

### SELL

Полный выход.

Каждый сигнал должен содержать причину.

Пример:

``` text
SBER

SIGNAL: BUY
SETUP: BREAKOUT

Market regime: BULL
Sector: BANKS
Relative strength: HIGH
Momentum: HIGH
Volume: CONFIRMED
BOS: CONFIRMED

Entry: 345.20
Stop: 332.80

Risk: 1.2%
Position size: 30%

Reason:
Пробой сопротивления подтверждён объёмом и BOS.
```

------------------------------------------------------------------------

# 21. Signal Engine

`Signal Engine` объединяет результаты всех модулей.

Он не должен самостоятельно рассчитывать индикаторы.

Вход:

``` text
MarketRegime
SectorMetrics
StockMetrics
SMCConfirmation
Setup
PortfolioState
RiskState
```

Выход:

``` python
Signal(
    action="BUY",
    ticker="...",
    setup="BREAKOUT",
    confidence=None,
    entry_price=...,
    stop_price=...,
    position_size=...,
    risk_amount=...,
    reason="..."
)
```

Поле `confidence` не следует интерпретировать как вероятность прибыльной
сделки. Если оно будет использоваться, его нужно определить как
технический score и отдельно проверить статистически.

------------------------------------------------------------------------

# 22. Rotation Engine

Раз в неделю:

``` text
Портфель
   ↓
Переоценка каждой позиции
   ↓
Сильнее/слабее рынка?
   ↓
Тренд сохранён?
   ↓
Есть более сильная альтернатива?
```

Если позиция слабее рынка и тренд сломан:

``` text
REDUCE / SELL
```

Если появилась более сильная акция с подтверждённым сетапом:

``` text
освободить капитал
        ↓
новая позиция
```

Капитал не должен быть навсегда привязан к первоначальному списку акций.
fileciteturn0file0L119-L136

------------------------------------------------------------------------

# 23. Cash Management

Базовая доля cash:

``` text
10–20%
```

При ухудшении режима:

``` text
30–50%+
```

При сильном Bear:

``` text
большая часть капитала вне рынка
```

Cash используется для новых подтверждённых возможностей, а не для
усреднения убыточных позиций. fileciteturn0file0L138-L146

------------------------------------------------------------------------

# 24. Макроэкономический фильтр

В перспективе учитывать:

-   ставку ЦБ;
-   инфляцию;
-   курс RUB;
-   Brent/Urals;
-   санкционные события;
-   налоги;
-   корпоративные отчёты;
-   дивиденды.

Макроэкономика является фильтром направления поиска, но не
самостоятельным торговым сигналом.

Новости сами по себе не являются сигналом. Важна реакция цены и объёма.
fileciteturn0file0L119-L136

В первой версии допустимо оставить макро-модуль за пределами MVP и
сначала построить систему на цене, объёме и структуре.

------------------------------------------------------------------------

# 25. SQLite Schema

Минимальная структура БД:

``` text
users
portfolios
positions
instruments
candles
market_regimes
sector_metrics
stock_metrics
smc_metrics
signals
signal_events
orders
risk_parameters
backtest_runs
backtest_trades
alerts
```

### instruments

``` text
id
ticker
figi
instrument_uid
name
sector
currency
lot_size
is_active
```

### candles

``` text
id
instrument_id
timeframe
timestamp
open
high
low
close
volume
```

Уникальный индекс:

``` text
(instrument_id, timeframe, timestamp)
```

### positions

``` text
id
portfolio_id
instrument_id
quantity
average_price
current_price
stop_price
opened_at
updated_at
```

### signals

``` text
id
instrument_id
created_at
action
setup
timeframe
market_regime
sector
entry_price
stop_price
risk_amount
position_size
reason
status
```

### backtest_runs

``` text
id
started_at
finished_at
from_date
to_date
initial_capital
strategy_version
parameters_json
```

------------------------------------------------------------------------

# 26. Конфигурация

Все изменяемые параметры должны находиться в конфигурации.

Пример:

``` yaml
capital: 100000

risk:
  min_percent: 1.0
  max_percent: 1.5

portfolio:
  min_positions: 5
  max_positions: 7
  max_position_percent: 25
  max_sector_percent: 50

market_regime:
  bull_exposure_min: 70
  bull_exposure_max: 100
  neutral_exposure_min: 40
  neutral_exposure_max: 70
  bear_exposure_min: 0
  bear_exposure_max: 40

profit:
  partial_1_min: 8
  partial_1_max: 12
  partial_2_min: 15
  partial_2_max: 25

smc:
  swing_length: 50
  close_break: true
```

Не зашивать эти значения непосредственно в бизнес-логику.

------------------------------------------------------------------------

# 27. Структура проекта

``` text
moex-trading-bot/
│
├── app/
│   ├── main.py
│   │
│   ├── config/
│   │   ├── settings.py
│   │   └── strategy.yaml
│   │
│   ├── api/
│   │   ├── tinkoff_client.py
│   │   ├── market_data.py
│   │   ├── portfolio.py
│   │   └── sandbox.py
│   │
│   ├── database/
│   │   ├── models.py
│   │   ├── database.py
│   │   └── repositories/
│   │
│   ├── market/
│   │   ├── regime.py
│   │   ├── sectors.py
│   │   └── universe.py
│   │
│   ├── indicators/
│   │   ├── trend.py
│   │   ├── momentum.py
│   │   ├── volatility.py
│   │   ├── volume.py
│   │   └── relative_strength.py
│   │
│   ├── smc/
│   │   ├── analyzer.py
│   │   └── confirmation.py
│   │
│   ├── strategy/
│   │   ├── breakout.py
│   │   ├── pullback.py
│   │   ├── ranking.py
│   │   └── engine.py
│   │
│   ├── portfolio/
│   │   ├── manager.py
│   │   ├── rotation.py
│   │   └── exposure.py
│   │
│   ├── risk/
│   │   ├── manager.py
│   │   ├── position_size.py
│   │   └── stops.py
│   │
│   ├── signals/
│   │   ├── models.py
│   │   └── generator.py
│   │
│   ├── backtest/
│   │   ├── engine.py
│   │   ├── broker.py
│   │   └── metrics.py
│   │
│   └── telegram/
│       ├── bot.py
│       ├── handlers.py
│       └── keyboards.py
│
├── tests/
├── scripts/
├── data/
├── logs/
├── .env.example
├── requirements.txt
├── README.md
└── pyproject.toml
```

------------------------------------------------------------------------

# 28. Этапы разработки

## Этап 1 --- каркас проекта

Создать:

``` text
app/
tests/
scripts/
data/
logs/
```

Настроить:

-   Python;
-   virtual environment;
-   `pyproject.toml`;
-   logging;
-   `.env`;
-   конфигурацию;
-   pytest.

**Результат:** приложение запускается.

------------------------------------------------------------------------

## Этап 2 --- SQLite

Реализовать:

-   подключение;
-   SQLAlchemy models;
-   создание таблиц;
-   repositories;
-   миграционную стратегию.

Сначала:

``` text
instruments
candles
portfolios
positions
signals
```

**Результат:** данные сохраняются и читаются из SQLite.

------------------------------------------------------------------------

## Этап 3 --- T-Invest API

Реализовать клиент:

``` text
TinkoffClient
```

Методы:

``` text
get_instruments()
get_candles()
get_last_prices()
get_portfolio()
get_positions()
```

Отдельно:

``` text
SandboxClient
```

для Sandbox-счёта и заявок.

T-Invest API имеет отдельный sandbox-контур и предоставляет там работу
со счетами, портфелем, позициями и торговыми поручениями.
citeturn0search0turn0search1

**Результат:** бот получает реальные рыночные данные через API и может
работать с тестовым счётом.

------------------------------------------------------------------------

# 29. Этап 4 --- Historical Data Loader

Создать:

``` text
scripts/load_history.py
```

Функции:

``` text
загрузка списка инструментов
        ↓
загрузка исторических свечей
        ↓
нормализация
        ↓
SQLite
```

Для каждого инструмента загружать необходимые таймфреймы:

``` text
D1
H4
H1
```

Исторические свечи получать через `GetCandles`. citeturn0search3

**Результат:** локальная БД содержит исторические данные для анализа и
бэктеста.

------------------------------------------------------------------------

# 30. Этап 5 --- Technical Engine

Реализовать и протестировать:

``` text
EMA20
EMA50
EMA200
ATR
Momentum
Volume Ratio
Relative Strength
Swing High/Low
```

Каждый индикатор должен иметь отдельные unit-тесты.

**Результат:** для каждой свечи можно получить набор технических
признаков.

------------------------------------------------------------------------

# 31. Этап 6 --- SMC Engine

Подключить:

``` text
smartmoneyconcepts
```

Реализовать адаптер:

``` text
SMCAnalyzer
```

Он должен преобразовывать результат сторонней библиотеки в собственную
модель проекта.

Например:

``` python
SMCResult(
    swing_high=...,
    swing_low=...,
    bos=...,
    choch=...,
    fvg=...,
    liquidity=...,
    order_block=...
)
```

Не использовать напрямую DataFrame сторонней библиотеки во всех
остальных модулях.

**Результат:** замена версии SMC-библиотеки не ломает Strategy Engine.

------------------------------------------------------------------------

# 32. Этап 7 --- Market Regime

Реализовать:

``` text
MarketRegimeAnalyzer
```

Вход:

``` text
IMOEX D1
```

Выход:

``` text
BULL / NEUTRAL / BEAR
```

Добавить unit-тесты на искусственных наборах данных.

------------------------------------------------------------------------

# 33. Этап 8 --- Sector Rotation

Реализовать:

``` text
SectorAnalyzer
```

Функции:

``` text
calculate_sector_strength()
rank_sectors()
get_top_sectors()
```

Период пересчёта:

``` text
1 раз в неделю
```

------------------------------------------------------------------------

# 34. Этап 9 --- Stock Ranking

Реализовать:

``` text
StockRanker
```

Pipeline:

``` text
ликвидные акции
       ↓
сильные сектора
       ↓
Relative Strength
       ↓
Momentum
       ↓
Volume
       ↓
ATR
       ↓
EMA structure
       ↓
5–7 кандидатов
```

------------------------------------------------------------------------

# 35. Этап 10 --- Breakout

Создать:

``` text
BreakoutStrategy
```

Необходимо формализовать:

``` text
Resistance
Breakout
Volume confirmation
BOS
Retest
Entry
```

Каждое правило должно быть бинарным и программно проверяемым.

Не использовать фразы вида:

``` text
"пробой выглядит сильным"
"объём достаточно большой"
"тренд явно хороший"
```

Вместо этого должны быть формулы и пороги.

------------------------------------------------------------------------

# 36. Этап 11 --- Pullback

Создать:

``` text
PullbackStrategy
```

Проверять:

``` text
Uptrend
+
Pullback
+
EMA20/EMA50/support
+
reversal
+
SMC confirmation
+
volume
```

------------------------------------------------------------------------

# 37. Этап 12 --- Strategy Engine

Объединить:

``` text
Market Regime
+
Sector
+
Stock Ranking
+
Breakout/Pullback
+
SMC
+
Risk
```

Strategy Engine должен выдавать:

``` text
NO_SIGNAL
BUY
ADD
HOLD
REDUCE
SELL
```

------------------------------------------------------------------------

# 38. Этап 13 --- Risk Manager

Реализовать:

``` text
calculate_stop()
calculate_risk()
calculate_position_size()
calculate_portfolio_exposure()
validate_trade()
```

Перед каждым BUY/ADD:

``` text
Strategy Signal
       ↓
Risk Manager
       ↓
Trade allowed?
       ↓
YES → Signal
NO  → NO_SIGNAL
```

------------------------------------------------------------------------

# 39. Этап 14 --- Portfolio Manager

Получать данные портфеля из API.

Для каждой позиции определять:

``` text
trend status
profit/loss
stop status
relative strength
sector strength
setup status
```

Результат:

``` text
HOLD
REDUCE
SELL
ADD
```

------------------------------------------------------------------------

# 40. Этап 15 --- Signal Journal

Каждый сигнал сохранять в SQLite.

Обязательно записывать:

``` text
timestamp
ticker
action
setup
market_regime
sector
technical metrics
SMC metrics
entry
stop
risk
position size
reason
strategy version
```

Это необходимо для последующего анализа:

``` text
сигнал → сделка → результат
```

------------------------------------------------------------------------

# 41. Этап 16 --- Backtest Engine

Это обязательный этап до реального использования.

Важно разделять два понятия:

### Historical Backtest

Исторические свечи загружаются через API и воспроизводятся локальным
движком.

``` text
Historical Data
      ↓
Backtest Engine
      ↓
Strategy Engine
      ↓
Virtual Broker
      ↓
Trades
      ↓
Metrics
```

T-Invest API предоставляет исторические данные, а разработчик
самостоятельно реализует механизм проверки торговой гипотезы.
citeturn0search11

### Sandbox

Sandbox используется как дополнительный контур тестирования
взаимодействия с торговой инфраструктурой и исполнения заявок.

По документации T-Invest, Sandbox является тестовым контуром, не
влияющим на реальные данные, и поддерживает тестовые счета, позиции и
торговые поручения. citeturn0search0

При этом Sandbox имеет отличия от реального исполнения: например,
рыночные заявки исполняются по последней сделке, комиссии моделируются
отдельно, а налоги и дивиденды не начисляются. citeturn0search0

Поэтому **Sandbox нельзя считать заменой полноценному историческому
backtest**.

------------------------------------------------------------------------

# 42. Backtest Metrics

Минимальный набор:

``` text
Total Return
CAGR
Max Drawdown
Win Rate
Profit Factor
Average Win
Average Loss
Expectancy
Number of Trades
Average Holding Period
Largest Win
Largest Loss
```

Дополнительно:

``` text
Return by sector
Return by setup
Return by market regime
Return by timeframe
Performance of SMC filters
```

Особенно важно сравнить:

``` text
Strategy
Strategy + SMC
```

чтобы проверить, действительно ли SMC улучшает систему.

------------------------------------------------------------------------

# 43. Walk-Forward Testing

Не оптимизировать параметры на всей истории одновременно.

Использовать:

``` text
Train period
      ↓
Optimization
      ↓
Validation period
      ↓
Next period
      ↓
Repeat
```

Цель --- проверить устойчивость стратегии к изменению рынка.

------------------------------------------------------------------------

# 44. Этап 17 --- Telegram Bot

Основной интерфейс пользователя.

Команды:

``` text
/start
/portfolio
/signals
/market
/sectors
/stocks
/risk
/history
/backtest
/settings
```

Пример:

``` text
📊 Рынок

IMOEX: BULL

Экспозиция: 80%

Сильные сектора:
1. BANKS
2. OIL_GAS
3. IT
```

------------------------------------------------------------------------

# 45. Пользовательский портфель

Сценарий:

``` text
/start
   ↓
Создание профиля
   ↓
Подключение T-Invest
   ↓
Получение портфеля
   ↓
Анализ
```

В перспективе можно поддержать:

``` text
Sandbox portfolio
Real portfolio
Manual portfolio
```

Но в первой версии достаточно Sandbox + ручного тестового портфеля.

------------------------------------------------------------------------

# 46. Уведомления

Уведомлять пользователя только при значимых изменениях:

``` text
BUY
ADD
REDUCE
SELL
STOP HIT
REGIME CHANGE
STRONG SECTOR CHANGE
```

Не отправлять сообщение на каждую новую свечу, если торговый сигнал не
изменился.

------------------------------------------------------------------------

# 47. Логирование

Использовать стандартный Python logging.

Уровни:

``` text
DEBUG
INFO
WARNING
ERROR
```

Логировать:

-   API ошибки;
-   отсутствие данных;
-   ошибки расчётов;
-   сигналы;
-   изменение режима;
-   ошибки Telegram;
-   backtest;
-   Sandbox operations.

Не записывать API-токен в лог.

------------------------------------------------------------------------

# 48. Безопасность

Токены:

``` text
.env
```

Никогда:

``` text
не хранить токен в Git
не записывать токен в SQLite
не отправлять токен в Telegram
не помещать токен в README
```

Добавить:

``` text
.env
*.db
logs/
__pycache__/
```

в `.gitignore`.

------------------------------------------------------------------------

# 49. Тестирование

Минимальная структура:

``` text
tests/
├── test_indicators.py
├── test_market_regime.py
├── test_sector.py
├── test_smc.py
├── test_breakout.py
├── test_pullback.py
├── test_risk.py
├── test_portfolio.py
├── test_signals.py
└── test_backtest.py
```

Каждый новый модуль сначала покрывается unit-тестами.

------------------------------------------------------------------------

# 50. Definition of Done для MVP

MVP считается готовым, когда система может:

``` text
1. Подключиться к T-Invest API
2. Получить список акций
3. Получить исторические свечи
4. Сохранить свечи в SQLite
5. Рассчитать EMA/ATR/Momentum/Volume/RS
6. Определить Market Regime
7. Рассчитать Sector Strength
8. Сформировать Stock Ranking
9. Рассчитать SMC
10. Найти Breakout
11. Найти Pullback
12. Рассчитать Stop
13. Рассчитать Risk
14. Рассчитать Position Size
15. Получить Sandbox Portfolio
16. Сформировать BUY/ADD/HOLD/REDUCE/SELL
17. Сохранить сигнал в SQLite
18. Запустить исторический backtest
19. Получить статистику
20. Отправить сигнал в Telegram
```

------------------------------------------------------------------------

# 51. Порядок разработки

Не писать весь проект одновременно.

Рекомендуемый порядок:

``` text
01. Project skeleton
        ↓
02. Configuration
        ↓
03. SQLite
        ↓
04. T-Invest client
        ↓
05. Historical data loader
        ↓
06. Indicators
        ↓
07. Market Regime
        ↓
08. Sector Analyzer
        ↓
09. Stock Ranking
        ↓
10. SMC adapter
        ↓
11. Breakout
        ↓
12. Pullback
        ↓
13. Strategy Engine
        ↓
14. Risk Manager
        ↓
15. Portfolio Manager
        ↓
16. Signal Journal
        ↓
17. Backtest Engine
        ↓
18. Walk-forward tests
        ↓
19. Sandbox
        ↓
20. Telegram
        ↓
21. Monitoring
```

------------------------------------------------------------------------

# 52. Первый рабочий спринт

Начинать следует не с Telegram.

### Шаг 1

Создать репозиторий:

``` text
moex-trading-bot
```

### Шаг 2

Создать виртуальное окружение.

### Шаг 3

Установить зависимости:

``` text
tinkoff-investments
pandas
numpy
sqlalchemy
aiogram
smartmoneyconcepts
pydantic-settings
pytest
pyyaml
```

Версии пакетов зафиксировать после проверки совместимости.

### Шаг 4

Создать:

``` text
.env.example
strategy.yaml
pyproject.toml
```

### Шаг 5

Реализовать SQLite.

### Шаг 6

Реализовать `TinkoffClient`.

### Шаг 7

Проверить получение:

``` text
список инструментов
исторические свечи
последние цены
```

### Шаг 8

Загрузить небольшой исторический набор.

### Шаг 9

Проверить расчёт:

``` text
EMA20
EMA50
EMA200
ATR
Volume
Momentum
```

### Шаг 10

Подключить `smartmoneyconcepts`.

На этом этапе уже должна появиться первая полностью работающая
вертикаль:

``` text
T-Invest API
    ↓
Historical candles
    ↓
SQLite
    ↓
Indicators
    ↓
SMC
    ↓
Console output
```

Только после её успешного завершения переходить к Strategy Engine.

------------------------------------------------------------------------

# 53. Принцип разработки стратегии

Главное правило проекта:

> Сначала формализовать правило, затем писать код.

Нельзя реализовывать:

``` text
"сильный тренд"
"хороший объём"
"сильная акция"
"важный уровень"
```

без математического определения.

Каждое правило должно выглядеть примерно так:

``` python
if (
    close > resistance
    and volume_ratio >= MIN_VOLUME_RATIO
    and bos == 1
    and close > ema20
):
    breakout = True
```

После этого правило тестируется на истории.

------------------------------------------------------------------------

# 54. Версионирование стратегии

Каждый backtest должен сохранять:

``` text
strategy_version
config_version
smc_parameters
risk_parameters
date_range
```

Например:

``` text
strategy_v0.1
strategy_v0.2
strategy_v0.3
```

Нельзя сравнивать результаты двух backtest без сохранения использованных
параметров.

------------------------------------------------------------------------

# 55. Основной принцип проекта

Стратегия должна реализовываться как последовательность:

``` text
Макро-фильтр
      ↓
IMOEX
      ↓
Market Regime
      ↓
Sector Rotation
      ↓
Relative Strength
      ↓
Stock Ranking
      ↓
Breakout / Pullback
      ↓
SMC Confirmation
      ↓
Risk Management
      ↓
Position Size
      ↓
Signal
      ↓
Portfolio Management
      ↓
Backtest / Sandbox
```

Именно эта последовательность должна стать основной архитектурой
проекта.

Ключевой принцип исходной стратегии:

> **Макро задаёт направление поиска, сектор показывает где искать, цена
> даёт конкретный сигнал, риск-менеджмент определяет размер ставки.**
> fileciteturn0file0L205-L217

------------------------------------------------------------------------

# 56. Что не делать в первой версии

Не добавлять сразу:

``` text
Deep Learning
нейросети
генеративный ИИ
автоматическое управление реальным счётом
десятки индикаторов
сложный frontend
микросервисную архитектуру
Redis
Kafka
Docker Swarm/Kubernetes
```

Первая версия должна быть:

``` text
Python
+
SQLite
+
T-Invest API
+
pandas/numpy
+
smartmoneyconcepts
+
Strategy Engine
+
Backtest
+
Telegram
```

Цель MVP --- получить **воспроизводимую и тестируемую торговую логику**,
а не максимально сложную инфраструктуру.

------------------------------------------------------------------------

## Источники

-   T-Invest API: https://developer.tbank.ru/invest/intro/intro
-   T-Invest API Sandbox:
    https://developer.tbank.ru/invest/intro/developer/sandbox
-   Исторические свечи:
    https://developer.tbank.ru/invest/api/market-data-service-get-candles
-   Smart Money Concepts:
    https://github.com/joshyattridge/smart-money-concepts

## Статус

``` text
Architecture:     READY
Database:         SQLite
Broker API:       T-Invest API
Testing:          Historical Backtest + Sandbox
SMC:              Integrated as confirmation layer
Trading mode:     Signals first
Auto execution:   Not in MVP
```
