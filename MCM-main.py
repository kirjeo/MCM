import pandas as pd
import numpy as np
import seaborn as sns
import predictr
import matplotlib.pyplot as plt
from textblob import Word
import scipy.stats as s


def remove_words(in_list, bad_list):
    out_list = []
    for line in in_list:
        words = ' '.join([word for word in line.split() if not any([phrase in word for phrase in bad_list]) ])
        out_list.append(words)
    return out_list


def readingInFiles(file):
    with open(file) as f:
        lines = f.readlines()
        out_lines = remove_words(lines, ['\n'])
        res = [eval(i) for i in out_lines]
    return res


def main():
    std = readingInFiles('std.txt')
    mean = readingInFiles('mean.txt')
    hardplayers = readingInFiles('hardplayer.txt')
    """"
    df = pd.read_excel('Data_for_John3.xlsx')
    for i in range(len(df.index)):
        print(df.loc[i].iat[1])
    """
    plt.scatter(std, hardplayers)
    plt.xlabel('STD')
    plt.ylabel('Hard Players')
    plt.show()


if __name__ == '__main__':
    main()
