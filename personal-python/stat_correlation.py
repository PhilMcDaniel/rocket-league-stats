import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt

#read csv source file
all_player_stats = pd.read_csv("d:/Git/MNCS/rocket-league-stats/personal-python/s4_coeffs.csv", sep=',')
#change data type to numeric so correlation works
all_player_stats['Game Win %'] = all_player_stats['player game win %'].str.replace('%','').astype(float)

MNCS_player_stats = all_player_stats[all_player_stats['league_name'] == 'mncs']
CLMN_player_stats = all_player_stats[all_player_stats['league_name'] == 'clmn']
MNRS_player_stats = all_player_stats[all_player_stats['league_name'] == 'mnrs']

all_players_corrMatrix = all_player_stats.corr()
MNCS_corrMatrix = MNCS_player_stats.corr()
CLMN_corrMatrix = CLMN_player_stats.corr()
MNRS_corrMatrix = MNRS_player_stats.corr()

print(MNRS_corrMatrix)
#print(all_players_corrMatrix,MNCS_corrMatrix,CLMN_corrMatrix,MNRS_corrMatrix)

# sn.heatmap(all_players_corrMatrix, annot=True)
# plt.show()
# sn.heatmap(MNCS_corrMatrix, annot=True)
# plt.show()
# sn.heatmap(CLMN_corrMatrix, annot=True)
# plt.show()
# sn.heatmap(MNRS_corrMatrix, annot=True)
# plt.show()