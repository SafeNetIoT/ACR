import pandas as pd
import sys

csv_path=sys.argv[1]
dev_ip=sys.argv[2]
#dev_ip2=sys.argv[3]

#ADD COLUMN NAMES
columns = ["frame_number","frame_time_epoch","frame_len","frame_protocols","eth_src","eth_dst","ip_src","ip_dst","ip_proto","ip_len","ip_id","tcp_srcport","tcp_dstport","udp_srcport","udp_dstport","tcp_flags","dns_qry_name","dns_resp_name","dns_ips","http_request_method"]
df=pd.read_csv(csv_path, delimiter=",", names = columns, skiprows=[0])

#ADD COLUMN "REMOTE_IP"
df.loc[df["ip_src"]==dev_ip,"remote_ip"] = df.loc[df["ip_src"]==dev_ip,"ip_dst"]
df.loc[df["ip_dst"]==dev_ip,"remote_ip"] = df.loc[df["ip_dst"]==dev_ip,"ip_src"]
#ADD COLUMN "DIRECTION"
df.loc[df["ip_src"]==dev_ip,"direction"] = "Uplink"
df.loc[df["ip_dst"]==dev_ip,"direction"] = "Downlink"

#ADD COLUMN "REMOTE_IP"
#df.loc[df["ip_src"]==dev_ip2,"remote_ip"] = df.loc[df["ip_src"]==dev_ip2,"ip_dst"]
#df.loc[df["ip_dst"]==dev_ip2,"remote_ip"] = df.loc[df["ip_dst"]==dev_ip2,"ip_src"]
#ADD COLUMN "DIRECTION"
#df.loc[df["ip_src"]==dev_ip2,"direction"] = "Uplink"
#df.loc[df["ip_dst"]==dev_ip2,"direction"] = "Downlink"

#CREATE A NEW DF CONTAINING ALL DNS PACKETS AND DROP THEM IN THE MAIN DF
columns_to_drop=["dns_qry_name","dns_resp_name","dns_ips"]
new_df=df[columns_to_drop]
new_df.dropna(subset=['dns_qry_name', 'dns_resp_name'], how='all', inplace=True)
new_df.dropna(subset=['dns_ips'], how='all', inplace=True)
new_df=new_df.drop_duplicates()
df.drop(columns=columns_to_drop, inplace=True)

df=pd.merge(df, new_df, left_on='remote_ip', right_on='dns_ips', how='left')
df.drop(columns='dns_ips', inplace=True)
#df['datetime'] = pd.to_datetime(df['frame_time_epoch'], unit='s')
#df['time'] = df['datetime'].dt.time
#df.drop(columns=['datetime'], inplace=True)
df['datetime']= pd.to_datetime(df['frame_time_epoch'], unit='s') #.astype('datetime64[s]')

#SAVE DFs
df.to_csv(csv_path, index=False)
#new_df.to_csv("dns_df.csv", index=False)
