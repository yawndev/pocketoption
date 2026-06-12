# API Reference

Version: **0.6.0**

All methods are synchronous (they block until done). The Rust core runs ticks,
candle aggregation and reconnection in the background.

## Connection

### `PocketOption(ssid: str)`
Connects and authenticates synchronously. Demo vs real is detected from the SSID.

> Paste the SSID as a **raw triple-quoted string**: `ssid = r'''42["auth",{...}]'''`.
> Plain `"..."` breaks on the inner double quotes.

`pocketoption.__version__` → module version string.

## Account & status

| Method | Returns | Description |
|--------|---------|-------------|
| `is_demo()` | `bool` | True for a demo account |
| `balance()` | `float` | Latest balance |
| `server_time()` | `int` | Server time (unix seconds), 0 if unknown |
| `payout(asset)` | `float \| None` | Broker payout % for the asset |
| `payout_corrected(asset, bias=8.0, cap=92.0)` | `float \| None` | `min(payout + bias, cap)` |
| `is_open(asset)` | `bool \| None` | Whether the asset is open for trading |
| `last_price(asset)` | `float \| None` | Last tick price |

## Candles — history

### `get_candles(asset: str, period: int, count: int) -> list[dict]`
One-shot history. `period` is the candle length in seconds (1, 5, 10, 15, 30, 60, …).
Each candle: `{"time", "open", "high", "low", "close", "volume"}`, oldest first.

## Candles — live buffer (any timeframe)

### `watch(asset: str, periods: list[int]) -> None`
Starts live aggregation for the given periods (seconds). Warms up with history,
then keeps candles updated from the tick stream.

### `candles_live(asset: str, period: int, count: int = 200) -> list[dict]`
Returns the last `count` candles from the live buffer — **instant, no network**.
The **last** candle is the currently forming one; drop it with `[:-1]` for closed bars.

## Trading

| Method | Returns | Description |
|--------|---------|-------------|
| `buy(asset, amount, expiry)` | `dict` | Open a CALL (`{"id","asset","amount","open_price"}`) |
| `sell(asset, amount, expiry)` | `dict` | Open a PUT |
| `open(asset, action, amount, expiry)` | `dict` | Direction by `action`: `"call"`/`"put"` |
| `check_result(deal_id, wait_secs=120)` | `dict` | Wait for outcome (`{"id","asset","outcome","profit"}`) |
| `trade(asset, action, amount, expiry)` | `dict` | Open + wait for outcome (shortcut) |

`amount` is in dollars (float), `expiry` in seconds. `outcome` is `"win" / "loss" / "draw"`.

## Ticks & events

| Method | Description |
|--------|-------------|
| `subscribe(asset)` | Subscribe to the asset's tick stream |
| `recv_tick(timeout_secs=10)` | Next tick `{"asset","time","price"}` or `None` |
| `on_tick(callback)` | Call `callback(tick_dict)` on every tick (background) |
| `on_candle(asset, period, callback)` | Call `callback(candle_dict)` when a candle closes |

## Low-level

### `raw_send(frame: str) -> None`
Send a raw Socket.IO frame (escape hatch for rare events).

## Behavior

- **Auto-reconnect:** disconnects are handled transparently; the object stays usable
  and re-subscribes automatically.
- **Errors:** invalid SSID, rejected orders and timeouts raise `RuntimeError`.
- **Demo vs real:** check `is_demo()` before going live — real trades use real funds.
