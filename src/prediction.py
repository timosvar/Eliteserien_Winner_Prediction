import pandas as pd

# ==============================
# Load Main Dataset
# ==============================
df = pd.read_csv(r"Eliteserien_Winner_Prediction/data_csv/Eliteserien_Dataset.csv")

# ==============================
# Load Historical Champions
# ==============================
champions_df = pd.read_csv(r"Eliteserien_Winner_Prediction/data_csv/Last_Champions.csv")

# Count championships for each team
champion_counts = champions_df["Team"].value_counts().to_dict()

# Add Champion Bonus column
df["Champion_Bonus"] = df["Team"].map(lambda x: champion_counts.get(x, 0))

# Convert Team Budget from "10.3M" to numeric
df["Team Budget"] = (
    df["Team Budget"]
    .str.replace('M', '', regex=False)   # remove M
    .astype(float) * 1_000_000            # convert to full number
)

# Normalize Budget (0–1 scale)
df["Budget_Normalized"] = (
    (df["Team Budget"] - df["Team Budget"].min()) /
    (df["Team Budget"].max() - df["Team Budget"].min())
)

# ==============================
# Define Weights
# (You can tweak these later)
# ==============================
weights = {
    "points": 4,
    "gd": 1.5,
    "home_attack": 0.3,
    "home_defense": -0.2,
    "away_attack": 0.3,
    "away_defense": -0.2,
    "wins": 1.5,
    "draws": 0.5,
    "red_cards": -0.7,
    "penalties_attempted": 0.1,
    "budget": 2,
    "champion_bonus": 1
}

# ==============================
# Calculate Prediction Score
# ==============================
df["GD"] = df["GF"] - df["GA"]  # Just in case GD not in CSV

df["Prediction_Score"] = (
    df["Points"] * weights["points"] +
    df["GD"] * weights["gd"] +
    df["Home GF"] * weights["home_attack"] +
    df["Home GA"] * weights["home_defense"] +
    df["Away GF"] * weights["away_attack"] +
    df["Away GA"] * weights["away_defense"] +
    df["Wins"] * weights["wins"] +
    df["Draws"] * weights["draws"] +
    df["Red Cards"] * weights["red_cards"] +
    df["Penalty Kicks"] * weights["penalties_attempted"] +
    df["Budget_Normalized"] * weights["budget"] +
    df["Champion_Bonus"] * weights["champion_bonus"]
)

# ==============================
# Sort Predictions
# ==============================
df_sorted = df.sort_values(by="Prediction_Score", ascending=False)

# ==============================
# Display Predicted Table
# ==============================
df_sorted["Prediction_Score"] = df_sorted["Prediction_Score"].round(2)
print("Predicted Table with Budget & Historical Bonus:")
print(df_sorted[["Team", "Prediction_Score"]].to_string(index=False))

# Predicted Winner
winner = df_sorted.iloc[0]["Team"]
print(f"\nPredicted Winner: {winner}")

