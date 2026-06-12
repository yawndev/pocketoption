"""
Quick start: connect, read candles, place a trade.

Run:
    python examples/quickstart.py
"""

from pocketoption import PocketOption

# Paste your SSID as a RAW TRIPLE-QUOTED string (it contains double quotes).
ssid = r'''42["auth",{"session":"YOUR_SESSION","isDemo":1,"uid":123,"platform":2}]'''

api = PocketOption(ssid)
print("demo:", api.is_demo(), "| balance:", api.balance())

ASSET = "EURUSD_otc"
print("payout:", api.payout(ASSET), "| open:", api.is_open(ASSET))

# Historical candles (ready for pandas / ML)
candles = api.get_candles(ASSET, 60, 50)
print("got", len(candles), "candles, last close:", candles[-1]["close"])

# Open a trade and wait for the outcome
result = api.trade(ASSET, "call", 1.0, 60)   # 1.0 USD, 60s expiry
print("outcome:", result["outcome"], "| profit:", result["profit"])
