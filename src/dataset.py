# winner_prediction_v2.py

import pandas as pd

# Load the updated dataset
df = pd.read_csv("data_csv/Eliteserien_Dataset.csv")

# Quick preview
print(df.head())

# Show columns to confirm
print("\nColumns in dataset:", df.columns.tolist())
