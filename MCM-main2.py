import pandas as pd
import numpy as np
import weibull
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
    al = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    std = readingInFiles('std.txt')
    mean = readingInFiles('mean.txt')
    premean = readingInFiles('predictedWordMean.txt')
    hardplayers = readingInFiles('hardplayer.txt')
    dataframe1 = pd.read_excel('Problem_C_Data_Wordle.xlsx')
    words = []
    new_word = list(dataframe1["Unnamed: 3"])
    for i in range(1, len(dataframe1.index)):
        word = []
        for x in dataframe1.loc[i].iat[3]:
            word.append([x, mean[i-1]])
        for x in word:
            words.append(x)
    words.sort()
    letterMean = []
    for letter in al:
        meanOfLetter = []
        for i in range(len(words)):
            if letter == words[i][0]:
                meanOfLetter.append(words[i][1])
        if len(meanOfLetter) != 0:
            letterMean.append(sum(meanOfLetter)/len(meanOfLetter))


    new_word_means = []
    for i in range(1, len(new_word)):
        new_word_mean = []
        aword = [x for x in new_word[i]]
        for letter in aword:
            new_word_mean.append(letterMean[ord(letter)-97])
        new_word_means.append(sum(new_word_mean)/len(new_word_mean))

    y = np.array(std)
    x = np.array(premean)
    a, b = np.polyfit(x, y, 1)
    #print(a)
    #print(b)
    r = np.corrcoef(x, y)
    print(r)
    plt.scatter(premean, std)
    plt.plot(x, a * x + b)
    plt.xlabel('STD')
    plt.ylabel('premean')
    plt.show()


if __name__ == '__main__':
    main()