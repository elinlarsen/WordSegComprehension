import os

PATH = '/Users/gladysbaudet/Desktop/PFE/'

read_list = []
for i in range(10):
    read_list.append(open(PATH+"Brent/sub"+str(i)+"/ortholines.txt", 'r').readlines())



for i in range (10): # for each size / then 10
    # create folder newpath = r'C:\Program Files\arbitrary'
    newpath = PATH+'sub_corpus/'+str((i+1)*10)+'k/'
    print(newpath)
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    for j in range(10): # for each new file
        # create file
        new_file = open(newpath+"ortholines"+str(j)+".txt", 'w')
        for k in range(i+1):
            # concat sub_j, ..., sub_(j+i)
            new_file.writelines(read_list[(j+k)%10])
