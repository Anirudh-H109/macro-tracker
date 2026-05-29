import streamlit as st
import pandas as pd
from fredapi import Fred
import yfinance as yf
import plotly.express as px
import requests
import datetime



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

#CPI Dropdown option
release_dates = {
    'May 2025': '2025-05-14',
    'June 2025': '2025-06-13',
    'July 2025': '2025-07-11',
    'Aug 2025': '2025-08-13',
    'Sep 2025': '2025-09-11',
    'Oct 2025': '2025-10-10',
    'Jan 2026': '2026-01-13',
    'Feb 2026': '2026-02-13',
    'March 2026': '2026-03-12',
    'Apr 2026': '2026-04-10',
    'May 2026': '2026-05-13'
}

st.subheader("Choose the CPI release date to see Market reaction on that day")
selected_month = st.selectbox("Choose a Date: ", list(release_dates.keys()), index=9)

chosen_date_str = release_dates[selected_month]
chosen_date = datetime.datetime.strptime(chosen_date_str, "%Y-%m-%d")

today = datetime.datetime.now()
days_ago = (today - chosen_date).days

# If else to check if intraday data is available
if days_ago <= 60:
    start_date = chosen_date.strftime("%Y-%m-%d")
    end_date = (chosen_date + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    chart_interval = '5m'
    is_intraday = True
else:
    start_date = (chosen_date - datetime.timedelta(days=10)).strftime("%Y-%m-%d")
    end_date = (chosen_date + datetime.timedelta(days=10)).strftime("%Y-%m-%d")
    chart_interval = '1d'
    is_intraday = False


# SPY on CPI Release
spy_cpi_day = yf.download('SPY', start=start_date, end=end_date, interval=chart_interval)
if not spy_cpi_day.empty:
    spy_close = spy_cpi_day['Close']
    
    title_text = f"⚡ SPY 5-Min Flash Volatility ({selected_month})" if is_intraday else f"📈 SPY 20-Day Macro Trend ({selected_month})"
    
    fig_spy_cpi = px.line(spy_close, title=title_text, labels={'Value': 'Stock Price', 'index': 'Timeline'}, markers=not is_intraday)
    
    fig_spy_cpi.update_layout(hovermode="x unified", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_spy_cpi)
else:
    st.warning(f"No SPY daily data found for {start_date}. The market might have been closed (weekend/holiday).")


# EUR/USD
eurusd_day = yf.download('EURUSD=X', start=start_date, end=end_date, interval=chart_interval)

if not eurusd_day.empty:
    if is_intraday:
        # Timezone fixes are safely isolated inside intraday only!
        if eurusd_day.index.tz is None:
            eurusd_day.index = eurusd_day.index.tz_localize('UTC')
        eurusd_day.index = eurusd_day.index.tz_convert('America/New_York')
        eurusd_day = eurusd_day.between_time('08:00', '16:00')
        
        eurusd_close = eurusd_day['Close']
        title_text = f'EUR/USD Intraday data on {chosen_date} from 8:00 to 16:00'
        # Fixed 'lables' typo here
        fig_eurusd = px.line(eurusd_close, title=title_text, labels={'Value': 'Price', 'index': 'Time'}, markers=False)
    else:
        eurusd_close = eurusd_day['Close']
        title_text = f'EUR/USD 20 day graph with {chosen_date} being the central date'
        # Fixed 'lables' typo here
        fig_eurusd = px.line(eurusd_close, title=title_text, labels={'Value': 'Price', 'index': 'Time'}, markers=True)

    fig_eurusd.update_layout(hovermode="x unified", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_eurusd)
else:
    st.warning(f"No EUR/USD data found for {start_date}.")

# Surprise Score
st.subheader("CPI - Surprise Score")

surprise_score={
    'Month' : ['May 2025','June 2025','July 2025','Aug 2025','Sep 2025','Oct 2025','Jan 2026','Feb 2026','March 2026','Apr 2026','May 2026'],
    'Actual %' : [0.2,0.1,0.3,0.2,0.4,0.3,0.3,0.2,0.3,0.9,0.6],
    'Forecast %': [0.3,0.2,0.3,0.2,0.3,0.4,0.3,0.3,0.3,1.0,0.6],
    'Surprise' : [-0.1,-0.1,0.0,0.0,0.1,-0.1,0.0,-0.1,0.0,-0.1,0.0]
}

df_surprise=pd.DataFrame(surprise_score)
st.dataframe(df_surprise, hide_index=True)

fig_surprise = px.bar(df_surprise, x='Month', y='Surprise', title='Surprise score for last 12 months',color='Surprise',
                      color_continuous_scale=['red', 'grey', 'green'],
                      color_continuous_midpoint=0)
st.plotly_chart(fig_surprise)


#TLT Bonds
tlt=yf.download('TLT',start='2020-01-01', end='2026-05-25')
eurusd_day.index = eurusd_day.index.tz_convert('America/New_York')
tlt=tlt['Close']
fig_tlt=px.line(tlt,title='TLT Data')
st.plotly_chart(fig_tlt)


