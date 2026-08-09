import os
import pandas as pd
from datetime import datetime

# Download the current leaderboard as a CSV (this requires the kaggle library)
os.system("kaggle competitions leaderboard playground-series-s6e8 --show-time -v > current_lb.csv")

# Read the downloaded CSV
df = pd.read_csv("current_lb.csv")

# Add a column for exactly when we scraped this data
df['Scrape_Time_UTC'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

# Check if we already have a history file
if os.path.exists("lb_history.csv"):
    history_df = pd.read_csv("lb_history.csv")
    # Append the new data to the history
    combined_df = pd.concat([history_df, df], ignore_index=True)
else:
    combined_df = df

# Save it back to the history file
combined_df.to_csv("lb_history.csv", index=False)
print("Successfully updated Leaderboard history!")
