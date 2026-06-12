"""
Live 5-second candles, aligned to the time grid.

The bot waits for the current candle to close (the next mark divisible by 5s)
and reads the just-closed candle from the live buffer.

Run:
    python examples/live_candles.py
"""

import time

from pocketoption import PocketOption

ssid = r'''42["auth",{"session":"YOUR_SESSION","isDemo":1,"uid":123,"platform":2}]'''

ASSET = "EURUSD_otc"
PERIOD = 5  # seconds

api = PocketOption(ssid)
print("demo:", api.is_demo(), "| balance:", api.balance())

# Start live aggregation: warms up with history, then updates from ticks.
api.watch(ASSET, [PERIOD])
time.sleep(2)

print(f"\nCollecting {PERIOD}s candles on the time grid. Ctrl+C to stop.\n")

last_time = None
try:
    while True:
        # Wait until the next grid boundary = current candle closes.
        now = time.time()
        next_boundary = (int(now) // PERIOD + 1) * PERIOD
        time.sleep((next_boundary - now) + 0.5)  # small margin for the closing tick

        # Last buffer item is forming; the one before it is the just-closed candle.
        candles = api.candles_live(ASSET, PERIOD, 3)
        if len(candles) < 2:
            continue
        closed = candles[-2]
        if closed["time"] == last_time:
            continue
        last_time = closed["time"]

        hh = time.strftime("%H:%M:%S", time.localtime(closed["time"]))
        print(f"[{hh}] {PERIOD}s closed: "
              f"o={closed['open']:.5f} h={closed['high']:.5f} "
              f"l={closed['low']:.5f} c={closed['close']:.5f} "
              f"(ticks={int(closed['volume'])}) | live={api.last_price(ASSET)}")

        # === your logic here: features on `closed` -> signal -> api.buy/sell ===

except KeyboardInterrupt:
    print("\nstopped.")
