import pandas as pd
import sys, os
import argparse

def display_all(c):
    df = pd.read_csv(c)
    df.transpose().boxplot()
    plt.show()




if __name__=='__main__' :
    parser = argparse.ArgumentParser(description='Displays whatever you want to display, but only whiskers for 10ksub correlation at one age per algorithm for now')
    parser.add_argument('-csv', '--csv_file', help='CSV file containing features to plot')
    args=parser.parse_args()
    display_all(args.csv_file)
