import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

cases = ["US-LG", "UK-LG", "US-Samsung", "UK-Samsung"]

for case in cases:

    # Define scenarios and activities
    scenarios = ['LIn-OIn', 'LIn-OOut', 'LOut-OIn', 'LOut-OOut']
    activities = ['Idle', 'Linear', 'FAST', 'OTT', 'HDMI', 'ScreenCast']
    activity_labels = ['Idle', 'Linear', 'FAST', 'OTT', 'HDMI', 'Screen Cast']
    colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown']  # Different colors for each activity

    # Set up the plot with 4 subplots in a row
    fig, axs = plt.subplots(1, 4, figsize=(15, 4), sharey=True)
    fig.subplots_adjust(top=0.95)  # Adjust top to leave space for a common legend

    # Column names based on the order in which they are saved by tshark
    column_names = [
        'frame_number', 'frame_time_epoch', 'frame_len', 'frame_protocols',
        'eth_src', 'eth_dst', 'ip_src', 'ip_dst', 'ip_proto', 'ip_len', 'ip_id',
        'tcp_srcport', 'tcp_dstport', 'udp_srcport', 'udp_dstport', 'tcp_flags',
        'dns_qry_name', 'dns_resp_name', 'dns_a', 'http_request_method'
    ]

    # Iterate through each scenario and corresponding subplot
    for i, scenario in enumerate(scenarios):
        ax = axs[i]
        for j, activity in enumerate(activities):
            # Path to the directory for the current scenario and activity
            folder_path = f'csvs/{case}/{scenario}/{activity}'
            print(folder_path)
            
            # Search for the CSV file in the folder
            csv_file = None
            if not os.path.exists(folder_path):
                continue
            for file in os.listdir(folder_path):
                if file.endswith('.csv'):
                    csv_file = os.path.join(folder_path, file)
                    break
            
            # If no CSV file found, continue to the next activity
            if not csv_file:
                continue

            # Load the CSV file into a DataFrame without headers and assign column names
            df = pd.read_csv(csv_file, delimiter=',', header=None, names=column_names, low_memory=False, on_bad_lines='warn')

            # ACR traffic identification logic
            acr_df = df[['frame_time_epoch', 'dns_resp_name', 'frame_len']].copy()
            acr_df['dns_resp_name'] = acr_df['dns_resp_name'].str.lower()
            filter_condition = ~acr_df['dns_resp_name'].str.contains('acr', na=False) | acr_df['dns_resp_name'].isna()
            acr_df.loc[filter_condition, 'frame_len'] = 0
            
            # Sort by time to accumulate bytes over time
            acr_df = acr_df.sort_values(by='frame_time_epoch')

            # Convert epoch time to minutes, relative to the first timestamp
            acr_df['time_in_minutes'] = (acr_df['frame_time_epoch'] - acr_df['frame_time_epoch'].min()) / 60

            # Compute cumulative sum of bytes over time
            acr_df['cumulative_bytes'] = acr_df['frame_len'].cumsum()

            # Normalize to get the CDF (percentage of total traffic)
            total_bytes = acr_df['frame_len'].sum()
            acr_df['cdf'] = acr_df['cumulative_bytes'] / total_bytes
            acr_df['cdf_percentage'] = (acr_df['cumulative_bytes'] / total_bytes) * 100

            # Plot the CDF with time in minutes on the x-axis and cumulative percentage on the y-axis
            ax.plot(acr_df['time_in_minutes'], acr_df['cdf_percentage'], label=activity_labels[j], color=colors[j])


        # Set subplot titles and labels
        # ax.set_title(scenario)
        ax.set_xlabel('Time (Minutes)')
        # Add subplot title inside the plot at the top left corner
        ax.text(0.05, 0.95, scenario, transform=ax.transAxes, fontsize=12, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.7))
        if i == 0:
            ax.set_ylabel('Cumulative Percentage of Bytes Transferred')

        # Set the x-axis limits and ticks
        ax.set_xlim(0, max(acr_df['time_in_minutes'].max(), 60))  # Adjust the upper limit if necessary
        ax.set_xticks(np.arange(0, max(acr_df['time_in_minutes'].max(), 60), step=10))

    # Add a common legend at the top, centered and in a single row
    # fig.legend(activity_labels, loc='right')
    # fig.legend(activity_labels, loc='upper center', bbox_to_anchor=(0.5, 2.05), ncol=6)
    axs[3].legend(loc='center', bbox_to_anchor=(0.5, 0.5))

    # Apply tight layout to ensure everything fits without extra space
    plt.tight_layout()

    # Save the plot to a file or show it
    plt.savefig(f'./output/{case}_cdf_bytes_over_time.png', bbox_inches='tight')
    # plt.show()
