import os
import sys
import pandas as pd
from datetime import datetime
import zipfile

comp_name = "playground-series-s6e8"
zip_path = f"{comp_name}.zip"
csv_name = f"{comp_name}-publicleaderboard.csv"

print("Downloading leaderboard from Kaggle...")
os.system(f"kaggle competitions leaderboard {comp_name} -d")

# SAFETY CHECK: Did the file actually download?
if not os.path.exists(zip_path):
    print(f"ERROR: {zip_path} failed to download.")
    print("Check your Kaggle API credentials and make sure you accepted the competition rules!")
    sys.exit(1)

print("Extracting and reading data...")
with zipfile.ZipFile(zip_path, 'r') as z:
    with z.open(csv_name) as f:
        df = pd.read_csv(f)

df['Scrape_Time_UTC'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

if os.path.exists("lb_history.csv"):
    history_df = pd.read_csv("lb_history.csv")
    combined_df = pd.concat([history_df, df], ignore_index=True)
else:
    combined_df = df

combined_df.to_csv("lb_history.csv", index=False)
print("Successfully downloaded and updated Leaderboard history!")
