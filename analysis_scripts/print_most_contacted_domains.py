import pandas as pd
import sys

# Load data from CSV
csv_file = sys.argv[1]  # Replace with the path to your CSV file
df = pd.read_csv(csv_file)

df_filtered = df.dropna(subset=['dns_resp_name'])

# Group by "dns_resp_name" and sum the "frame_len"
grouped_df = df_filtered.groupby('dns_resp_name')['frame_len'].sum().reset_index()

# Sort the DataFrame by cumulative frame length in ascending order
sorted_df = grouped_df.sort_values(by='frame_len', ascending=False)

pd.set_option('display.max_rows', None)

# Print the list of dns_resp_name with their associated cumulative frame_len in ascending order
print(sorted_df)
