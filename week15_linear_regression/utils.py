import pandas as pd
from sklearn.model_selection import train_test_split


def load_house_dataset():
    df = pd.read_csv("./data/house.csv")
    X = df.drop(["price"], axis=1)
    y = df["price"]
    return train_test_split(X, y, train_size=0.8, random_state=1234) 


def load_diamonds_dataset():
    df = pd.read_csv("./data/diamonds.csv")
    X = df.drop(["price"], axis=1)
    y = df["price"]
    return train_test_split(X, y, train_size=0.8, random_state=1234) 
