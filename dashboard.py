import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load data
file_path = 'C:/Users/HomePC/Documents/Semester 6 (Bangkit)/Dashboard/all_data.csv'
df = pd.read_csv(file_path)

# Data Cleaning
df['dteday'] = pd.to_datetime(df['dteday'])
df['season'] = df['season'].map({1: 'Semi', 2: 'Panas', 3: 'Gugur', 4: 'Dingin'})
df['yr'] = df['yr'].map({0: '2011', 1: '2012'})

# Helper function for EDA
def plot_time_series(df, x, y, moving_avg_col, trend_col, xlabel, ylabel, title):
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=df[x], y=df[y], label='Rata-Rata per Minggu', color='red')
    sns.lineplot(x=df[x], y=df[moving_avg_col], label='Moving Average (4 Minggu)', linestyle='--', color='cyan')
    sns.lineplot(x=df[x], y=df[trend_col], label='Tren', linestyle=':', color='yellow')

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    st.pyplot()

def plot_stacked_bar_chart(df, x, y, hue, xlabel, ylabel, title):
    plt.figure(figsize=(10, 6))
    sns.barplot(x=x, y=y, hue=hue, data=df, palette='pastel')

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend(title='Tahun')

    plt.tight_layout()
    st.pyplot()

# Dashboard
st.header('Bike Sharing Analysis Dashboard')

# Question 1: How does the bike rental volume change over time?
st.subheader('Bike Rental Volume Over Time')
df_weekly = df.resample('W-Mon', on='dteday').mean()
df_weekly['moving_avg'] = df_weekly['cnt'].rolling(window=4).mean()
x = np.arange(len(df_weekly)).reshape(-1, 1)
y = df_weekly['cnt'].values.reshape(-1, 1)
slope, intercept = np.polyfit(x.flatten(), y.flatten(), 1)
df_weekly['trend'] = intercept + slope * x

plot_time_series(df_weekly, 'dteday', 'cnt', 'moving_avg', 'trend',
                 'Date', 'Bike Rental Count', 'Bike Rental Trends 2011 - 2012')

# Question 2: How does the season affect the bike rental volume?
st.subheader('Bike Rental Volume by Season')
pivot_season_year = df.groupby(['season', 'yr'])['cnt'].sum().reset_index()
plot_stacked_bar_chart(pivot_season_year, 'season', 'cnt', 'yr',
                      'Season', 'Total Bike Rentals (Million)', 'Bike Rental Comparison by Season and Year')
