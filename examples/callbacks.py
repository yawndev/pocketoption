"""
Event-driven usage: react to ticks and candle closes via callbacks.

Run:
    python examples/callbacks.py
"""

import time

from pocketoption import PocketOption

ssid = r'''42["auth",{"session":"YOUR_SESSION","isDemo":1,"uid":123,"platform":2}]'''

ASSET = "EURUSD_otc"

api = PocketOption(ssid)
api.watch(ASSET, [5])   # live 5s candles + tick subscription

# Called when each 5s candle closes (already closed, ready to use).
def on_candle(c):
    print("closed 5s:", c["time"], "close=", c["close"])

# Called on every tick.
_count = {"n": 0}
def on_tick(t):
    _count["n"] += 1
    if _count["n"] % 100 == 0:
        print("tick", _count["n"], t["price"])

api.on_candle(ASSET, 5, on_candle)
api.on_tick(on_tick)

print("listening for 60s... (Ctrl+C to stop)")
try:
    time.sleep(60)
except KeyboardInterrupt:
    pass
print("done.")
