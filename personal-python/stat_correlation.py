import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt

#read csv source file
all_player_stats = pd.read_csv("MNCS/MNCS_S3_PlayerRatingData.csv", sep=',')
#change data type to numeric so correlation works
all_player_stats['Game Win %'] = all_player_stats['Game Win %'].str.replace('%','').astype(float)

MNCS_player_stats = all_player_stats[all_player_stats['League'] == 'mncs']
CLMN1_player_stats = all_player_stats[all_player_stats['League'] == 'clmn 1']
CLMN2_player_stats = all_player_stats[all_player_stats['League'] == 'clmn 2']

all_players_corrMatrix = all_player_stats.corr()
MNCS_corrMatrix = MNCS_player_stats.corr()
CLMN1_corrMatrix = CLMN1_player_stats.corr()
CLMN2_corrMatrix = CLMN2_player_stats.corr()

print(all_players_corrMatrix,MNCS_corrMatrix,CLMN1_corrMatrix,CLMN2_corrMatrix)

sn.heatmap(all_players_corrMatrix, annot=True)
plt.show()
sn.heatmap(MNCS_corrMatrix, annot=True)
plt.show()
sn.heatmap(CLMN1_corrMatrix, annot=True)
plt.show()
sn.heatmap(CLMN2_corrMatrix, annot=True)
plt.show()