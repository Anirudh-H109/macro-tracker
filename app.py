import streamlit as st
import pandas as pd
from fredapi import Fred
import yfinance as yf
import plotly.express as px

st.title("Macro Event Impact Tracker")
st.write("Tracking how CPI, unemployment and Fed rates affect markets")
st.markdown("""
This app tracks how major US macro events (CPI, unemployment, Fed rate decisions) 
affect financial markets across equities, FX, and rates. 

**How to read this:**
- 📈 CPI rising = inflation increasing
- 📉 Unemployment spike = economic stress  
- 💵 EUR/USD rising = US dollar weakening
- 🔴 Surprise Miss = actual came in below forecast
""")

fred = Fred(api_key=st.secrets["FRED_API_KEY"])

#CPI
cpi = fred.get_series('CPIAUCSL', observation_start='2020-01-01')
fig_cpi = px.line(cpi, title='CPI')
st.plotly_chart(fig_cpi)

#Unemployment Rate
unrate = fred.get_series('UNRATE', observation_start='2020-01-01')
fig_unrate = px.line(unrate, title='Unemployment Rate')
st.plotly_chart(fig_unrate)

# FED Rate
fed_rate=fred.get_series('FEDFUNDS', observation_start='2020-01-01')
fig_fed = px.line(fed_rate, title='FED Rates')
st.plotly_chart(fig_fed)

#NFP (Non Farm Payrolls)
nfp=fred.get_series('PAYEMS', observation_start='2020-01-01')
df_nfp = pd.DataFrame(nfp, columns=['Total_Employed'])

# 3. Calculate the monthly change (This is the magic line!)
df_nfp['Monthly_Change'] = df_nfp['Total_Employed'].diff()

# 4. Plot the monthly change instead of the total number
fig_nfp = px.line(
    df_nfp, 
    y='Monthly_Change', 
    title='Unemployment & Monthly Job Changes (NFP)',
    labels={'Monthly_Change': 'Jobs Added/Lost (in Thousands)', 'index': 'Date'}
)
st.plotly_chart(fig_nfp)

#SPY on CPI Release
spy_cpi_day = yf.download('SPY', start='2026-04-10', end='2026-04-11', interval='5m')
spy_cpi_day = spy_cpi_day['Close']
fig_spy_cpi = px.line(spy_cpi_day, title='SPY on CPI Day (Apr 10 2026)')
st.plotly_chart(fig_spy_cpi)


#Suprise Score
st.subheader("CPI - Surprise Score")

surprise_score={
    'Month' : ['Jan 2026','Feb 2026','March 2026','Apr 2026'],
    'Actual %' : [3.0, 2.8, 2.6, 2.4],
    'Forecast %': [2.9, 2.9, 2.7, 2.6],
    'Surprise' : ['+0.1', '-0.1', '-0.1', '-0.2']
}

df_surprise=pd.DataFrame(surprise_score)
st.dataframe(df_surprise, hide_index=True)

#EUR/USD
eurusd_day=yf.download('EURUSD=X',start='2026-04-10', end='2026-04-11', interval='5m')
eurusd_day.index = eurusd_day.index.tz_convert('America/New_York')
eurusd_day = eurusd_day.between_time('08:00', '16:00')
eurusd_day=eurusd_day['Close']
fig_eurusd=px.line(eurusd_day,title='EUR/USD on CPI Day')
st.plotly_chart(fig_eurusd)


#TLT Bonds
tlt=yf.download('TLT',start='2020-01-01', end='2026-05-25')
eurusd_day.index = eurusd_day.index.tz_convert('America/New_York')
tlt=tlt['Close']
fig_tlt=px.line(tlt,title='TLT Data')
st.plotly_chart(fig_tlt)


