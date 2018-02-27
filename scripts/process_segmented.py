from collections import Counter
import sys
import re

# argv 1 : path to file to freq-top
# argv 2 : nb is nb [for divided corpus] else ? FILE HAS TO BE blablax.txt with x a number
way = str(sys.argv[1]).split('/')[:-1]
nb = str(sys.argv[1]).split('.')[-2][-1]
PATH = ""
for s in way :
     PATH+=s+'/'# path to file

if not nb.isdigit():
    nb = ""

words = re.findall(r'\w+', open(str(sys.argv[1])).read().lower())
pre_res = Counter(words)
# pre_res['I']=pre_res['i']
# del pre_res['i']
res = pre_res.most_common(10000)
# print(res)

f = open(PATH+"freq-top"+nb+".txt", 'w')
for double in res :
    f.write(str(double[1])+" "+ str(double[0])+'\n')
