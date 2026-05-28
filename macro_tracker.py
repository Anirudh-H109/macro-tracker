from fredapi import Fred
import pandas as pd

# Paste your API key here
fred = Fred(api_key='9b5c94f27bd2df3a124d83d12a00347e')

# Pull CPI data (last 3 years)
cpi = fred.get_series('CPIAUCSL', observation_start='2020-01-01')

# Turn it into a table
df_cpi = pd.DataFrame(cpi, columns=['CPI'])
df_cpi.index.name = 'Date'

#Pull Unemployment data
unrate = fred.get_series('UNRATE', observation_start='2020-01-01')

df_unrate=pd.DataFrame(unrate,columns=['Unemployment Rate'])
df_unrate.index.name = 'Date'

#Pull Fed rates Data
fed_rate=fred.get_series('FEDFUNDS', observation_start='2020-01-01')

df_fedrate=pd.DataFrame(fed_rate, columns=['Fed Rates'])
df_fedrate.index.name='Date'

# Print it
print(df_cpi.tail(12))  # last 12 months
print(df_unrate.tail(12))
print(df_fedrate.tail(12))

import yfinance as yf

spy = yf.download('SPY', start='2020-01-01', interval='1d')
print(spy.tail(5))

spy_cpi_day = yf.download('SPY', start='2026-04-10', end='2026-04-11', interval='5m')
print(spy_cpi_day)

eurusd_day=yf.download('EURUSD=X',start='2026-04-10', end='2026-04-11', interval='5m')
eurusd_day.index = eurusd_day.index.tz_convert('America/New_York')
print(eurusd_day)



import matplotlib.pyplot as plt

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 16))

ax1.plot(df_cpi['CPI'])
ax1.set_title("CPI")
ax1.set_ylabel("Index")


# ax2.plot(df_unrate['Unemployment Rate'])
# ax2.set_title("Unemployment Rate")
# ax2.set_ylabel("%")


# ax3.plot(df_fedrate['Fed Rates'])
# ax3.set_title("Fed Funds Rate")
# ax3.set_ylabel("%")

ax2.plot(eurusd_day.index,eurusd_day['Close'])
ax2.set_title("EUR/USD on Apr 10 2026")
ax2.set_ylabel("Price")
ax2.set_xlabel("Time")
ax2.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%H:%M'))

ax3.plot(spy_cpi_day.index, spy_cpi_day['Close'])
ax3.set_title("SPY on CPI Day (Apr 10 2026)")
ax3.set_ylabel("Price")
ax3.set_xlabel("Time")
ax3.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%H:%M'))
ax3.axvline(x=pd.Timestamp('2026-04-10 09:30:00', tz='America/New_York'), 
            color='red', linestyle='--', label='Market Open')
ax3.legend()

plt.tight_layout()
plt.show()