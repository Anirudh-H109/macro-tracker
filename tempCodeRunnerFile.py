from fredapi import Fred
import pandas as pd

# Paste your API key here
fred = Fred(api_key='9b5c94f27bd2df3a124d83d12a00347e')

# Pull CPI data (last 3 years)
cpi = fred.get_series('CPIAUCSL', observation_start='2022-01-01')

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

import matplotlib.pyplot as plt
fig , (ax1,ax2,ax3) = plt.subplots(3,1, figsize=(12,8))

ax1.plot(df_cpi['CPI'])
ax1.set_title("CPI Graph")


ax2.plot(df_unrate['Unemployment Rate'])
ax2.set_title("Unemployement rate Graph")


ax3.plot(df_fedrate['Fed Rates'])
ax3.set_title("Fed Rate Graph")

plt.tight_layout()
plt.show()
