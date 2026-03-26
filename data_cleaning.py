import pandas as pd

def read_and_preview_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        print(df.head())
    except Exception as e:
        print(f"Error reading the file: {e}")

# file path
file_path = "data.csv"

# function call
read_and_preview_csv(file_path)