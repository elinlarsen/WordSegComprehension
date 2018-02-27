import pandas as pd

fil = open("test.txt",'r').readlines()
for f in fil :
    f = f[:-1]
    a, b = f.split('\t')
    print(a, b)

d = {'a':0, 'b':1, 'c':2}
df = pd.DataFrame(list(d.items()))
print(df)
