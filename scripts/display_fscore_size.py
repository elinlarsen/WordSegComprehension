import pandas as pd
import matplotlib.pyplot as plt


PATH_RES = '/Users/gladysbaudet/Desktop/PFE/Results/'
sub = ['/10k/', '/20k/', '/30k/', '/40k/', '/50k/']
# sub = ['/10k/']
df_phoneme = []
df_syllable = []
# ALGOS = ['ag', 'dibs', 'puddle', 'baseline', 'dpseg', 'tp/absoluteforward', 'tp/absolutebackward', 'tp/relativeforward', 'tp/relativebackward']
ALGOS = ['baseline', 'dibs', 'dpseg', 'puddle', 'tp/relativeforward']
SCORE = ["type_fscore", "type_recall", "type_precision", "token_fscore", "token_recall", "token_precision", "boundary_fscore", "boundary_recall", "boundary_precision"]

for i in range(len(sub)):
    df_phoneme.append(pd.DataFrame.from_csv(PATH_RES+sub[i]+'eval_phoneme_csv.txt'))
    df_syllable.append(pd.DataFrame.from_csv(PATH_RES+sub[i]+'eval_syllable_csv.txt'))

df_pho_res = pd.DataFrame(index=ALGOS, columns=sub)
df_syl_res = pd.DataFrame(index=ALGOS, columns=sub)



for a in ALGOS :
    for i in range(len(sub)) :
        df_pho_res.loc[a][sub[i]] = df_phoneme[i].loc[a]["token_fscore"]

print(df_pho_res)

df_pho_res.transpose().plot(title='Algorithms\' mean token F-score depending on the size of the corpus')
plt.show()
