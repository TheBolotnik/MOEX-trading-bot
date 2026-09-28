# MOEX Trading Signal Bot

Сигнальный торговый бот для Московской биржи: данные через **T-Invest API**,
хранение в **SQLite**, анализ по стратегии **Dynamic Swing Momentum**,
доставка сигналов в **Telegram**.

> **MVP:** только сигналы `BUY / ADD / HOLD / REDUCE / SELL`.  
> Автоисполнение реальных сделок **не входит** в первую версию.  
> Sandbox — для проверки инфраструктуры заявок, не замена historical backtest.

Полное техническое задание: [`docs/specification.md`](docs/specification.md).

## Стек

| Слой | Технологии |
| --- | --- |
| Язык | Python 3.11+ |
| Брокер | T-Invest API (`tinkoff-investments`) |
| БД | SQLite + SQLAlchemy |
| Конфиг | `.env`, pydantic-settings, `strategy.yaml` |
| UI | Telegram (aiogram) |
| Тесты | pytest |

## Структура

```text
app/
  main.py                 # точка входа
  config/                 # settings + strategy.yaml
  api/                    # T-Invest client (заглушки)
  database/               # SQLAlchemy models / session
  market/                 # regime, sectors, universe
  indicators/             # EMA/ATR/Momentum/Volume/RS
  smc/                    # SMC confirmation adapter
  strategy/               # breakout, pullback, ranking, engine
  portfolio/              # manager, rotation, exposure
  risk/                   # size, stops
  signals/                # signal models / generator
  backtest/               # engine, metrics
  telegram/               # bot, handlers
tests/
scripts/
data/
logs/
```

## Быстрый старт

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# заполните TINKOFF_TOKEN и TELEGRAM_BOT_TOKEN при необходимости

python -m app.main
pytest
```

## Конфигурация

- `.env` — секреты и пути (см. `.env.example`)
- `app/config/strategy.yaml` — пороги риска, режима рынка, SMC и т.д.
- `app/config/settings.py` — загрузка через pydantic-settings

## Статус каркаса

Сейчас репозиторий содержит **только скелет**: пакеты, конфиг, точки входа и
smoke-тесты импортов. Торговая логика, индикаторы, бэктест и реальные вызовы
брокера **намеренно не реализованы** — следующий этап: SQLite + T-Invest client.

## Режим работы

- **Signals first** — анализ и рекомендации
- **Auto execution** — не в MVP
