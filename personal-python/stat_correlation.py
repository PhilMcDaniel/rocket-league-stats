import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt

#read csv source file
all_player_stats = pd.read_csv("d:/Git/MNCS/rocket-league-stats/personal-python/s5_data.csv", sep=',')
#change data type to numeric so correlation works
all_player_stats['Game Win %'] = all_player_stats['player game win %'].str.replace('%','').astype(float)

Premier_player_stats = all_player_stats[all_player_stats['league_name'] == 'Premier']
Challenger_player_stats = all_player_stats[all_player_stats['league_name'] == 'Challenger']
RisingStar_player_stats = all_player_stats[all_player_stats['league_name'] == 'RisingStar']

all_players_corrMatrix = all_player_stats.corr()
Premier_corrMatrix = Premier_player_stats.corr()
Challenger_corrMatrix = Challenger_player_stats.corr()
RisingStar_corrMatrix = RisingStar_player_stats.corr()

#print(Premier_corrMatrix)
print(all_players_corrMatrix,Premier_corrMatrix,Challenger_corrMatrix,RisingStar_corrMatrix)

# sn.heatmap(all_players_corrMatrix, annot=True)
# plt.show()
# sn.heatmap(MNCS_corrMatrix, annot=True)
# plt.show()
# sn.heatmap(CLMN_corrMatrix, annot=True)
# plt.show()
# sn.heatmap(MNRS_corrMatrix, annot=True)
# plt.show()