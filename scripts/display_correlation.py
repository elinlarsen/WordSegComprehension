import pandas as pd
import matplotlib.pyplot as plt


PATH_RES = '/Users/gladysbaudet/Desktop/PFE/Results/'
sub = ['/10k/', '/20k/', '/30k/', '/40k/', '/50k/']
# sub = ['/10k/']
# df_phoneme = []
df_syllable = []
# ALGOS = ['ag', 'dibs', 'puddle', 'baseline', 'dpseg', 'tp/absoluteforward', 'tp/absolutebackward', 'tp/relativeforward', 'tp/relativebackward']
ALGOS = ['gold', 'baseline', 'dibs', 'dpseg', 'puddle', 'tp/relativeforward']
SCORE = ["type_fscore", "type_recall", "type_precision", "token_fscore", "token_recall", "token_precision", "boundary_fscore", "boundary_recall", "boundary_precision"]

for i in range(len(sub)):
    # df_phoneme.append(pd.DataFrame.from_csv(PATH_RES+sub[i]+'correlationR2_phoneme.txt'))
    df_syllable.append(pd.DataFrame.from_csv(PATH_RES+sub[i]+'correlationR2_syllable.txt'))

# df_pho_res = pd.DataFrame(index=ALGOS, columns=sub)
df_syl_res = pd.DataFrame(index=ALGOS, columns=sub)

for a in ALGOS :
    for i in range(len(sub)) :
        # df_pho_res.loc[a][sub[i]] = df_phoneme[i].loc[a]["token_fscore"]
        df_syl_res.loc[a][sub[i]] = df_syllable[i].loc[a]["mean"]

# print(df_syl_res)

df_tp_rf = pd.DataFrame(index=sub, columns=[i for i in range(10)], dtype=float)
df_gold = pd.DataFrame(index=sub, columns=[i for i in range(10)], dtype=float)
for j in range(len(sub)) :
    for i in range(10):
        df_tp_rf.loc[sub[j]][i] = float(df_syllable[j].loc['tp/relativeforward'][i])
        df_gold.loc[sub[j]][i] = float(df_syllable[j].loc['gold'][i])
# print(df_tp_rf)
# pd.to_numeric(df_tp_rf.loc[1])
# print('df.dtypes: \n{0}'.format(df_tp_rf.dtypes))
# df_pho_res.transpose().plot(title='Algorithms\' mean token F-score depending on the size of the corpus')
df_syl_res.transpose().plot()
# df_gold.transpose().boxplot()
# df_tp_rf.transpose().boxplot()
# df_tp_rf.plot(title="Evolution of correlation between CDI and TP relative forward results, depending on corpus size")
plt.show()
