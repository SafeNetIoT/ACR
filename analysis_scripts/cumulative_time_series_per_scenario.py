from numpy.typing import ArrayLike
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
from typing import List
from datetime import datetime
import matplotlib.dates as mdates

def lineplot(x: ArrayLike, yss: List[List[ArrayLike]], titles: List[str], x_label: str, y_label: str, number: int) -> (plt.Figure, plt.Axes):
    """
    Creates a line plot for the given data, title and labels.

    Args:
        x (ArrayLike): value of the data on the x-axis
        y (ArrayLike): value of the data on the y-axis
        title (str): title of the plot
        x_label (str): x-axis label
        y_label (str): y-axis label
    Returns:
        (plt.Figure, plt.Axes): matplotlib figure and axes objects
    """
    # create the figure
    fig, axs = plt.subplots(number, figsize=(15, 30))

    # add the data to the plot
    colors=['blue','blue', 'blue','blue']
    labels=['Entire Traffic','ACR Traffic']
    j=0
    for ys in yss:
        i=0
        for y in ys:
            print(titles[j])
            print(labels[i])
            #print(y)
            axs[j].plot(x, y, color=colors[i], label=labels[i], alpha=0.7)
#            axs[j].fill_between(x, y, color=colors[i], alpha=0.7)
            axs[j].set_ylim(0, 8000)
            axs[j].xaxis.set_major_formatter(mdates.DateFormatter('%M'))
#            axs[j].set_xticks(rotation=60) #range(11),range(11))
            i=i+1

    # remove whitespace before and after
        axs[j].margins(x=0)

    # format the axes
        axs[j].set_title(titles[j], fontsize=30)
        axs[j].set_xlabel(x_label, fontsize=24)
        axs[j].set_ylabel(y_label, fontsize=24)
        axs[j].tick_params(axis='x', labelsize=24, pad=10)
        axs[j].tick_params(axis='y', labelsize=24)
        j=j+1
#    ax.set_xticks(x[::20], x[::20], rotation=60)
    return fig, axs

csv_number=sys.argv[1]
csvs=[]
agg_dfs=[]
count=0
for i in range(2,int(csv_number)+2):
    csvs.append(sys.argv[i])
    count=i
    print(count)
print(count)
output_file=sys.argv[count+1]
agg_acr_dfs=[]

#i=0
for csv in csvs:
    df = pd.DataFrame()
    df = pd.read_csv(csv)
    interval = '1ms' #1min
    # Create new column with the time in seconds
    df['time_seconds'] = (df['frame_time_epoch'] - df['frame_time_epoch'].min())
    # If want to filter out packets towards a certain destination (for example transmission towards content provider)
    #filter_condition = df['dns_resp_name'].str.contains('fashiontv-fashiontv-5-gb.lg.wurl.tv', na=False) | df['dns_resp_name'].isna()
    #df.loc[filter_condition, 'frame_len'] = 0
    # Convert everything to the same date
    reference_date = pd.to_datetime('2024-01-01 23:40:00')
    min_datetime_object=datetime(2024, 1, 1, 23, 40)
    max_datetime_object = datetime(2024, 1, 2, 0, 40)
    df['frame_time_epoch'] = reference_date + pd.to_timedelta(df['time_seconds'], unit='s') + pd.to_timedelta(df['time_seconds'], unit='ms')
    # Filter out rows exceeding 1h time window
    df = df[df['time_seconds'] <= 3600]
    #df = df[(df['time_seconds'] >= 1200) & (df['time_seconds'] <= 1800)]
    agg_df = pd.DataFrame()
    agg_df = df.groupby(pd.Grouper(key='frame_time_epoch', freq=interval))['frame_len'].sum().reset_index()
    # Sometimes happens that there are no packets transmitted in the chosen time interval, therefore in order to have the same dimension we add the missing rows
    agg_df.set_index('frame_time_epoch', inplace=True)
    min_datetime_object=datetime(2024, 1, 2, 0, 00)
    max_datetime_object=datetime(2024, 1, 2, 0, 10)
#    if i==2:
#        min_datetime_object=datetime(2024, 1, 2, 0, 10)
#        max_datetime_object=datetime(2024, 1, 2, 0, 20)
    #full_index = pd.date_range(start=agg_df.index.min(), end=max_datetime_object, freq='ms') # S
    full_index = pd.date_range(start=min_datetime_object, end=max_datetime_object, freq='ms') # S
    agg_df = agg_df.reindex(full_index)
    agg_df['frame_len'].fillna(0, inplace=True)
    agg_dfs.append(agg_df)

    acr_df = pd.DataFrame()
    acr_df = df[['frame_time_epoch', 'dns_resp_name', 'frame_len']]
    filter_condition = ~acr_df['dns_resp_name'].str.contains('acr', na=False) | acr_df['dns_resp_name'].isna()
    acr_df.loc[filter_condition, 'frame_len'] = 0
    agg_acr_df = pd.DataFrame()
    agg_acr_df = acr_df.groupby(pd.Grouper(key='frame_time_epoch', freq=interval))['frame_len'].sum().reset_index()
    agg_acr_df.set_index('frame_time_epoch', inplace=True)
    full_index = pd.date_range(start=min_datetime_object, end=max_datetime_object, freq='ms')
    agg_acr_df = agg_acr_df.reindex(full_index)
    agg_acr_df['frame_len'].fillna(0, inplace=True)
    agg_acr_dfs.append(agg_acr_df)
#    i=i+1

#x=agg_dfs[0].index
yss=[]
i=0
for agg_df in agg_dfs:
    x=agg_df.index #['frame_time_epoch']
    #y1=agg_df['frame_len']
    y2=agg_acr_dfs[i]['frame_len']
    print(i)
    print(y2)
    yss.append([y2]) # y1,y2
    i=i+1
titles=["Idle", "Antenna", "FAST", "OTT", "HDMI", "Screen Cast"]
#titles=["Antenna - HDMI", "Idle - FAST - OTT - Screen Casting"]
#titles=["Antenna - FAST - HDMI", "Idle - OTT - Screen Casting"]
fig, axs = lineplot(x, yss, titles, "Time (Minutes)", "Total Traffic (Bytes)", len(yss))
plt.tight_layout()
#plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.savefig(output_file) #, dpi=300, bbox_inches='tight')
