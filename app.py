import pandas as pd
import json

# MATCH RESULTS
df = pd.read_json("t20_wc_match_results.json")
data_results = pd.DataFrame(df.loc[0,'matchSummary'])
data_results.rename({'scorecard': 'match_id'}, axis = 1, inplace = True)
data_results.to_csv("Match_results.csv",index=False)

# BATTING SUMMARY
df2 = pd.read_json("t20_wc_batting_summary.json")
summary = []
for i in range(len(df2)):
    item = df2.loc[i,'battingSummary']
    summary.extend(item)

data_batting_summary  = pd.DataFrame(summary)
data_batting_summary['out/not_out'] = data_batting_summary['dismissal'].apply(lambda x: "out" if len(x) > 0 else "not_out")
data_batting_summary.drop(columns=['dismissal'],inplace=True)

match_ids_dict = {}

for index, row in data_results.iterrows():
    key1 = row['team1'] + ' Vs ' + row['team2']
    key2 = row['team2'] + ' Vs ' + row['team1']
    match_ids_dict[key1] = row['match_id']
    match_ids_dict[key2] = row['match_id']

data_batting_summary['match_id'] = data_batting_summary['match'].map(match_ids_dict)

data_batting_summary['batsmanName'] = data_batting_summary['batsmanName'].apply(lambda x: x.replace('â€', ''))
data_batting_summary['batsmanName'] = data_batting_summary['batsmanName'].apply(lambda x: x.replace('\xa0', ''))
data_batting_summary.to_csv("Batting_Summary.csv")

# Bowling summary
with open('t20_wc_bowling_summary.json') as f:
    data = json.load(f)
    all_records = []
    for rec in data:
        all_records.extend(rec['bowlingSummary'])
df_bowling = pd.DataFrame(all_records)
print(df_bowling.shape)
print(df_bowling.head())

df_bowling['match_id'] = df_bowling['match'].map(match_ids_dict)
print(df_bowling.head())

df_bowling.to_csv('bowling_summary.csv', index = False)

# Player information
with open('t20_wc_player_info.json') as f:
    data = json.load(f)
df_players = pd.DataFrame(data)

print(df_players.shape)
print(df_players.head(10))

df_players['name'] = df_players['name'].apply(lambda x: x.replace('â€', ''))
df_players['name'] = df_players['name'].apply(lambda x: x.replace('†', ''))
df_players['name'] = df_players['name'].apply(lambda x: x.replace('\xa0', ''))
df_players.head(10)

print(df_players[df_players['team'] == 'India'])

df_players.to_csv('players_no_images.csv', index = False)
