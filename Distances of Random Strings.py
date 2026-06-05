import matplotlib.pyplot as plt
import numpy as np
from random import choice
from random import sample
from itertools import count

import numpy

def Randome_sequence_length ():
    bases=["A","G","C","T"]
    length = 100
    sequence = ""
    for i in range(length):
        base = choice(bases)
        sequence += base
    return sequence

def Paris_of_randome():
    string1=[]
    string2=[]
    pairs_range=1000
    for i in range(pairs_range):
        seq1 = Randome_sequence_length()
        seq2 = Randome_sequence_length()
        string1.append(seq1)
        string2.append(seq2)
    return string1,string2


def Hamming_distance(string1,string2):
    hammingD=[]
    if len(string1) != len(string2):
        raise ValueError('strings have unequal lengths')

    for s1, s2 in zip(string1, string2):
        t = 0
        for x, y in zip(s1, s2):
            t += int(x != y)
        hammingD.append(t)
    return hammingD

def edit_distance(s, t):
    m, n = len(s), len(t)
    # Column 0
    Dc = list(range(m + 1))
    Dp = [0] * (m + 1)
    for j, tj in zip(count(1), t):
        Dp, Dc = Dc, Dp
        Dc[0] = j
        for i, si in zip(count(1), s):
            Dc[i] = min(Dp[i - 1] + (si != tj),
                    Dp[i] + 1,
                    Dc[i - 1] + 1)
    return Dc[m]

if __name__ == '__main__':

    bases=["A","G","C","T"]
    lists,s=Paris_of_randome()
    hamming=Hamming_distance(lists,s)
    editdistance=[]
    for s1,s2 in zip(lists,s):
        editdistance.append(edit_distance(s1,s2))


n, bins, patches = plt.hist(x=hamming,  color='red',
                            alpha=0.7, rwidth=0.5,label="Hamming")
n, bins, patches = plt.hist(x=editdistance,  color='blue',
                            alpha=0.7, rwidth=0.5,label="Edit")
plt.grid(axis='y', alpha=0.75)
plt.xlabel('Distance')
plt.ylabel('Total Number of Pairs')
plt.title('Distances Histogram')
plt.text(23, 45, r'$\mu=15, b=3$')
plt.legend()
plt.show()





