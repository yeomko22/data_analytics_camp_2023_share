import pandas as pd
from sklearn.metrics import mean_squared_error
from matplotlib import pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller, kpss


def plot_acf_pacf(df, target_column):
    target_series = df[target_column].dropna()
    fig = plt.figure(figsize=(10, 3))
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)
    plot_acf(df[target_column].dropna(), ax=ax1);
    plot_pacf(df[target_column].dropna(), ax=ax2);
    

def stationary_test(df, target_column):
    target_series = df[target_column].dropna()
    adf_result = adfuller(target_series)
    adf_p_value = adf_result[1]
    kpss_result = kpss(target_series)
    kpss_p_value = kpss_result[1]
    print(f"{target_column} ADF p-value: {round(adf_p_value, 4)} stationary: {adf_p_value < 0.05}")
    print(f"{target_column} KPSS p-value: {round(kpss_p_value, 4)} stationary: {kpss_p_value > 0.05}")


def calculate_rmse(df, label_column, target_column):
    target_df = df[[label_column, target_column]].dropna()
    rmse = mean_squared_error(target_df[label_column], target_df[target_column], squared=False)
    print(f"{target_column} RMSE: {rmse}")


def load_air_passengers():
    df = pd.read_csv("./data/AirPassengers.csv", index_col="Month", parse_dates=True)
    df.index.freq = "MS"
    threshold = pd.Timestamp("1957-12-31")
    train_df = df[:threshold]
    test_df = df[threshold:]
    return train_df, test_df


def load_sunspots():
    df = pd.read_csv("./data/Sunspots.csv", index_col="Date", parse_dates=True)
    df.index.freq = "M"
    threshold = pd.Timestamp("1965-01-01")
    train_df = df[:threshold]
    test_df = df[threshold:]
    return train_df, test_df


def load_restaurant():
    df = pd.read_csv("./data/restaurant.csv", index_col="date", parse_dates=True)
    df.index.freq = "D"
    threshold = pd.Timestamp("2016-11-30")
    train_df = df[:threshold]
    test_df = df[threshold:]
    return train_df, test_df


def load_tsla_stock():
    df = pd.read_csv("./data/TSLA.csv", index_col="Date", parse_dates=True)
    threshold = pd.Timestamp("2022-12-31")
    train_df = df[:threshold]
    test_df = df[threshold:]
    return train_df, test_df


def load_delhi_climate():
    df = pd.read_csv("./data/DelhiClimate.csv", index_col="date", parse_dates=True)
    threshold = pd.Timestamp("2016-01-01")
    train_df = df[:threshold]
    test_df = df[threshold:]
    return train_df, test_df
