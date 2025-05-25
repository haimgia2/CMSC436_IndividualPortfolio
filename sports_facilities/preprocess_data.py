import pandas as pd
import os

def preprocess_data(folder):
    df = pd.read_csv(os.path.join(folder, 'athletic-facilities-1.csv'))

    return df


if __name__ == "__main__":
    df = preprocess_data()