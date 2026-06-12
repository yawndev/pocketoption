# pocketoption

[![Platforms](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-blue)]()
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)]()
[![Made with Rust](https://img.shields.io/badge/core-Rust-orange)]()

A fast, native **PocketOption** client for Python — built on a Rust core.
Stream live prices, build candles for **any timeframe (including seconds)**, place
trades, and react to events with low latency.

> Unofficial library. Not affiliated with or endorsed by PocketOption.

---

## Features

- ⚡ **Native Rust core** — minimal latency, all parsing/aggregation off the GIL.
- 🕒 **Live candles on every timeframe**, including 1s/5s/10s/15s/30s — built locally
  from a single tick stream, read from memory instantly.
- 📈 Historical candles (OHLC), payouts, asset open/closed status.
- 💵 Trading: `buy` / `sell` / `open`, with outcome resolution.
- 🔔 Event-driven callbacks: `on_tick`, `on_candle`.
- 🔌 Auto-reconnect with automatic re-subscription.
- 🪟🐧🍎 Prebuilt wheels for Windows, Linux (manylinux x86_64) and macOS.

---

## Install

Download the wheel for your OS from the [**Releases**](../../releases) page, then:

```bash
pip install pocketoption-0.6.0-*.whl
```

Pick the right file:

| OS | Wheel |
|----|-------|
| Windows (x64)       | `...-win_amd64.whl` |
| Linux (x86_64)      | `...-manylinux_..._x86_64.whl` |
| macOS (Intel)       | `...-macosx_..._x86_64.whl` |
| macOS (Apple Silicon) | `...-macosx_..._arm64.whl` |

No Rust required — the wheel is a self-contained compiled binary. Python 3.8+.

---

## Quick start

```python
from pocketoption import PocketOption

# IMPORTANT: paste the SSID as a RAW TRIPLE-QUOTED string (it contains double quotes).
ssid = r'''42["auth",{"session":"...","isDemo":1,"uid":123,"platform":2}]'''

api = PocketOption(ssid)              # connects synchronously
print("demo:", api.is_demo(), "balance:", api.balance())

# Historical candles -> ready for pandas / ML
candles = api.get_candles("EURUSD_otc", 60, 100)

# Place a trade and wait for the result
res = api.trade("EURUSD_otc", "call", 1.0, 60)
print(res["outcome"], res["profit"])   # 'win' 0.92
```

## Live candles (any timeframe, including seconds)

Subscribe once, read fresh candles from memory — no per-call network requests.

```python
import time

api.watch("EURUSD_otc", [5, 15, 30])   # aggregate these timeframes live
time.sleep(2)

c5 = api.candles_live("EURUSD_otc", 5, 200)
closed = c5[:-1]                        # last item is the still-forming candle
```

## Event-driven (callbacks)

```python
# fires when each 5s candle closes (already closed, ready to use)
api.watch("EURUSD_otc", [5])
api.on_candle("EURUSD_otc", 5, lambda c: print("closed 5s:", c))

# fires on every tick
api.on_tick(lambda t: ...)
```

---

## Docs & examples

- Full API reference: [`API.md`](API.md)
- Runnable examples: [`examples/`](examples/)

---

## Notes

- **SSID is a credential** (your session). Keep it private, never commit it.
- Trading involves financial risk. This library is provided as-is, without warranty;
  you are responsible for how you use it.
