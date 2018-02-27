import sys
import pandas as pd
import matplotlib.pyplot as plt

sub = ['/10k/', '/20k/', '/30k/', '/40k/', '/50k/']

# path/sub[i]/algos[j]/eval0.txt
# ALGOS = ['ag', 'dibs', 'puddle', 'baseline', 'dpseg', 'tp/absoluteforward', 'tp/absolutebackward', 'tp/relativeforward', 'tp/relativebackward']
ALGOS = ['baseline/', 'dibs/', 'dpseg/', 'puddle/', 'tp/relativeforward/']
unit = ['syllable/', 'phoneme/']
# p = sys.argv[1]
p = '/Users/gladysbaudet/Desktop/PFE/Results/'
PATH = [[pd.DataFrame.from_csv(p+sub[j]+ALGOS[i]+unit[0]+'/summary_csv.txt') for i in range(len(ALGOS))] for j in range(len(sub))]


def read_eval(f, summary, df, i):

    for line in f :
        line = line[:-1]
        key, val = line.split('\t')
        summary[key] += float(val)
        df.loc[key][i] = float(val)

df = pd.DataFrame(index=sub, columns=ALGOS)


print(len(PATH[0]))
for i in range(len(PATH)) :
    for j in range(len(ALGOS)):
        df.loc[sub[i]][ALGOS[j]]=PATH[i][j].loc['token_recall']['0']

print(df)
df.plot()
plt.show()
