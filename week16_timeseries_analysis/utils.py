import pandas as pd
from sklearn.metrics import mean_squared_error


def calculate_rmse(df, target_column):
    target_df = df[["Passengers", target_column]].dropna()
    rmse = mean_squared_error(target_df["Passengers"], target_df[target_column], squared=False)
    print(f"{target_column} RMSE: {rmse}")


def load_air_passengers():
    df = pd.read_csv("./data/AirPassengers.csv", index_col="Month", parse_dates=True)
    threshold = pd.Timestamp("1957-12-31")
    train_df = df[:threshold]
    test_df = df[threshold:]
    return train_df, test_df


def load_sunspots():
    df = pd.read_csv("./data/Sunspots.csv", index_col="Date", parse_dates=True)
    threshold = pd.Timestamp("1965-01-01")
    train_df = df[:threshold]
    test_df = df[threshold:]
    return train_df, test_df