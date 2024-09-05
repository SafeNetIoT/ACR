from numpy.typing import ArrayLike
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
from typing import List

def lineplot(x: ArrayLike, ys: List[ArrayLike], title: str, x_label: str, y_label: str) -> (plt.Figure, plt.Axes):
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
    fig, ax = plt.subplots(1, figsize=(30, 4))

    # add the data to the plot
    colors=['lightblue','lightcoral', 'lightblue','lightcoral']
    i=0
    for y in ys:
        ax.plot(x, y, color=colors[i], alpha=0.3)
        ax.fill_between(x, y, color=colors[i], alpha=0.3)
        i=i+1

    # remove whitespace before and after
    ax.margins(x=0)

    # format the axes
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
#    ax.set_xticks(x[::20], x[::20], rotation=60)
    return fig, ax

csv_file1=sys.argv[1]
csv_file2=sys.argv[2]

# Dataframe containing the entire traffic
df=pd.read_csv(csv_file1) # Training
#df2=pd.read_csv(csv_file2) # Post-Opt-Out-Training
df2=df
# For choosing the time window in which aggregating packets
interval = '1s' #1min
df['time_seconds'] = (df['frame_time_epoch'] - df['frame_time_epoch'].min())
df2['time_seconds'] = (df2['frame_time_epoch'] - df2['frame_time_epoch'].min())

#df = df[df['time_seconds'] <= 28800]
#df2 = df2[df2['time_seconds'] <= 28800]

#df['frame_time_epoch'] = pd.to_datetime(df['frame_time_epoch'], unit='s') # Training
#df2['frame_time_epoch'] = pd.to_datetime(df2['frame_time_epoch'], unit='s') # Post-Opt-Out-Training

# If want to filter out packets of a certain time window (like excluding beginning or end of capture)
#filter_condition = (df['time_seconds'] > 0) & (df['time_seconds'] <= 240)
#filter_condition2 = (df2['time_seconds'] > 0) & (df2['time_seconds'] <= 240)
    #filter_condition = (df['frame_time_epoch'].dt.hour == 10) & (df['frame_time_epoch'].dt.minute > 0) & (df['frame_time_epoch'].dt.minute <= 4)
    #filter_condition2 = (df2['frame_time_epoch'].dt.hour == 10) & (df2['frame_time_epoch'].dt.minute > 0) & (df2['frame_time_epoch'].dt.minute <= 4)
#df.loc[filter_condition, 'frame_len'] = 0
#df2.loc[filter_condition2, 'frame_len'] = 0

# If want to filter out packets towards a certain destination (for example transmission towards content provider)
filter_condition = df['dns_resp_name'].str.contains('fashiontv-fashiontv-5-gb.lg.wurl.tv', na=False) | df['dns_resp_name'].isna()
df.loc[filter_condition, 'frame_len'] = 0
#emt.live.ll.ww.aiv-cdn.net
filter_condition2 = df2['dns_resp_name'].str.contains('fashiontv-fashiontv-5-gb.lg.wurl.tv', na=False) | df2['dns_resp_name'].isna()
df2.loc[filter_condition2, 'frame_len'] = 0

reference_date = pd.to_datetime('2024-01-01')
df['frame_time_epoch'] = reference_date + pd.to_timedelta(df['time_seconds'], unit='s')
df2['frame_time_epoch'] = reference_date + pd.to_timedelta(df2['time_seconds'], unit='s')
# Aggregate packets based on time window (sum values of bytes)
agg_df = df.groupby(pd.Grouper(key='frame_time_epoch', freq=interval))['frame_len'].sum().reset_index()
agg_df2 = df2.groupby(pd.Grouper(key='frame_time_epoch', freq=interval))['frame_len'].sum().reset_index()
agg_df2['frame_len'] = -agg_df2['frame_len']
# Normalize bytes (min-max)
#agg_df['frame_len_normalized'] = (agg_df['frame_len'] - agg_df['frame_len'].min()) / (agg_df['frame_len'].max() - agg_df['frame_len'].min())
#agg_df2['frame_len_normalized'] = -(agg_df2['frame_len'] - agg_df2['frame_len'].min()) / (agg_df2['frame_len'].max() - agg_df2['frame_len'].min())

# Dataframe containing only the 'acr' traffic
acr_df = df[['frame_time_epoch', 'dns_resp_name', 'frame_len']]
filter_condition = ~acr_df['dns_resp_name'].str.contains('acr', na=False) | acr_df['dns_resp_name'].isna()
acr_df.loc[filter_condition, 'frame_len'] = 0
acr_df2 = df2[['frame_time_epoch', 'dns_resp_name', 'frame_len']]
filter_condition2 = ~acr_df2['dns_resp_name'].str.contains('acr', na=False) | acr_df2['dns_resp_name'].isna()
acr_df2.loc[filter_condition2, 'frame_len'] = 0

# Aggregate packets with same time window as before
agg_acr_df = acr_df.groupby(pd.Grouper(key='frame_time_epoch', freq=interval))['frame_len'].sum().reset_index()
agg_acr_df2 = acr_df2.groupby(pd.Grouper(key='frame_time_epoch', freq=interval))['frame_len'].sum().reset_index()
agg_acr_df2['frame_len'] = -agg_acr_df2['frame_len']
# Normalize packets
#agg_acr_df['frame_len_normalized'] = (agg_acr_df['frame_len'] - agg_df['frame_len'].min()) / (agg_df['frame_len'].max() - agg_df['frame_len'].min())
#agg_acr_df2['frame_len_normalized'] = -(agg_acr_df2['frame_len'] - agg_df2['frame_len'].min()) / (agg_df2['frame_len'].max() - agg_df2['frame_len'].min())


#print(acr_df)
#x = df['frame_time_epoch']
#y1 = df['frame_len']
#y2 = acr_df['frame_len']
x = agg_df['frame_time_epoch']
y1 = agg_df['frame_len']
y2 = agg_acr_df['frame_len']
#y3 = agg_df2['frame_len']
#y4 = agg_acr_df2['frame_len']
#y = agg_df['frame_len_normalized']
#ys=[y1, y2, y3, y4]

ys=[y1,y2]
fig, ax = lineplot(x, ys, "Test", "Time", "Bytes")

#plt.figure()
#plt.plot(df.groupby(by='datetime')['frame_len'].sum().index,df.groupby(by='datetime')['frame_len'].sum())

#plt.xticks(rotation=40)
plt.savefig(csv_file1+'.pdf') #, dpi=300, bbox_inches='tight')
plt.show()
