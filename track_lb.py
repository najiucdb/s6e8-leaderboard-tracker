import os
import pandas as pd
from datetime import datetime
import zipfile

# 1. Download the leaderboard as a zip file using the -d (download) flag
comp_name = "playground-series-s6e8"
os.system(f"kaggle competitions leaderboard {comp_name} -d")

# 2. Read the downloaded zip file
zip_path = f"{comp_name}.zip"

# Kaggle automatically names the CSV inside the zip like this:
csv_name = f"{comp_name}-publicleaderboard.csv"

# Open the zip and read the CSV
with zipfile.ZipFile(zip_path, 'r') as z:
    with z.open(csv_name) as f:
        df = pd.read_csv(f)

# 3. Add a column for exactly when we scraped this data
df['Scrape_Time_UTC'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

# 4. Check if we already have a history file
if os.path.exists("lb_history.csv"):
    history_df = pd.read_csv("lb_history.csv")
    # Append the new data to the history
    combined_df = pd.concat([history_df, df], ignore_index=True)
else:
    combined_df = df

# 5. Save it back to the history file
combined_df.to_csv("lb_history.csv", index=False)
print("Successfully downloaded and updated Leaderboard history!")
