import sys
from itertools import count
from argparse import ArgumentParser
import numpy as np

# direction constants (bit values, so we can OR them)
HOME, DIAGONAL, HORIZONTAL, VERTICAL = 0, 1, 2, 4


def needleman_wunsch(s, t, score):
    """
    return the optimal GLOBAL alignment between s and t,
    given a scoring function 'score'.
    For two characters a,b, score(a,b) is their score.
    Score(None) < 0 is the gap score.
    """
    m, n = len(s), len(t)
    gapscore = score(None)
    # we need the actual matrix now and a traceback matrix
    S = np.zeros((m+1, n+1), dtype=np.int32)  # scores
    T = np.zeros((m+1, n+1), dtype=np.uint8)  # traceback
    S[0,:] = np.arange(n+1, dtype=S.dtype) * gapscore
    S[:,0] = np.arange(m+1, dtype=S.dtype) * gapscore
    T[0,0] = HOME
    T[0,1:] = HORIZONTAL
    T[1:,0] = VERTICAL
    # Iterate over rows i and characters si in s
    for i, si in zip(count(1), s):
        # iterate over columns j and characters tj in t
        for j, tj in zip(count(1), t):
            d = S[i-1, j-1] + score(si, tj)
            h = S[i, j-1] + gapscore
            v = S[i-1, j] + gapscore
            opt = max(d, h, v)
            S[i,j] = opt
            T[i,j] = (d==opt)*DIAGONAL + (h==opt)*HORIZONTAL + (v==opt)*VERTICAL
    result = S[m,n]
    A = traceback(m, n, T, s, t)
    return result, A


def smith_waterman(s, t, score):
    """
    return the optimal LOCAL alignment between s and t,
    given a scoring function 'score'.
    For two characters a,b, score(a,b) is their score.
    Score(None) < 0 is the gap score.
    """
    m, n = len(s), len(t)
    gapscore = score(None)
    # we need the actual matrix now and a traceback matrix
    S = np.zeros((m+1, n+1), dtype=np.int32)  # scores
    T = np.zeros((m+1, n+1), dtype=np.uint8)  # traceback
    T[0,:] = HOME  # alignments end at border (score 0)
    T[:,0] = HOME  # alignments end at border (score 0)
    best = (-1, -1, -1)  # best (S, i, j)
    # Iterate over rows i and characters si in s
    for i, si in zip(count(1), s):
        # iterate over columns j and characters tj in t
        for j, tj in zip(count(1), t):
            d = S[i-1, j-1] + score(si, tj)
            h = S[i, j-1] + gapscore
            v = S[i-1, j] + gapscore
            opt = max(0, d, h, v)  # note additional 0 here
            S[i,j] = opt
            T[i,j] = (d==opt)*DIAGONAL + (h==opt)*HORIZONTAL + (v==opt)*VERTICAL
            # Note: T[i,j] can be HOME==0 if no other option applies.
            # We need to check whether we found a new maximum at S[i,j]
            if S[i,j] > best[0]:
                best = (S[i,j], i, j)
    result, i, j = best
    A = traceback(i, j, T, s, t)
    return result, A


# python assignment10.py ATAT TATC --score 1:-1:-2 --type overlap
def overlap(s, t, score):
    m, n = len(s), len(t)
    gapscore = score(None)
    # we need the actual matrix now and a traceback matrix
    S = np.zeros((m+1, n+1), dtype=np.int32)  # scores
    T = np.zeros((m+1, n+1), dtype=np.uint8)  # traceback
    #S[0,:] =np.arange(n+1, dtype=S.dtype) * gapscore
    #S[:,0] =np.arange(m+1, dtype=S.dtype) * gapscore
    T[0,0] = HOME
    T[0,1:] = HORIZONTAL
    T[1:,0] = VERTICAL
    # Iterate over rows i and characters si in s
    for i, si in zip(count(1), s):
        # iterate over columns j and characters tj in t
        for j, tj in zip(count(1), t):
            d = S[i-1, j-1] + score(si, tj)
            h = S[i, j-1] + gapscore
            v = S[i-1, j] + gapscore
            opt = max(d, h, v)
            S[i,j] = opt
            T[i,j] = (d==opt)*DIAGONAL + (h==opt)*HORIZONTAL + (v==opt)*VERTICAL
    max_val= -1000
    ind = (0, 0)
    for i, row in enumerate(S):
        for j, col in enumerate(row):
            if i == m or j == n :
                temp =S[i][j]
                if temp > max_val:
                    max_val=temp
                    ind=(i,j)

    A = overlap_traceback(ind[0], ind[1], T, s, t)

    return max_val,A

# python assignment10.py ATAT TATC --score 1:-1:-2 --type patternsearch
def patternsearch(s, t, score):
    m, n = len(s), len(t)
    gapscore = score(None)
    # we need the actual matrix now and a traceback matrix
    S = np.zeros((m + 1, n + 1), dtype=np.int32)  # scores
    T = np.zeros((m + 1, n + 1), dtype=np.uint8)  # traceback
    # S[0,:] =np.arange(n+1, dtype=S.dtype) * gapscore
    S[:,0] =np.arange(m+1, dtype=S.dtype) * gapscore
    T[0, 0] = HOME
    T[0, 1:] = HORIZONTAL
    T[1:, 0] = VERTICAL
    # Iterate over rows i and characters si in s
    for i, si in zip(count(1), s):
        # iterate over columns j and characters tj in t
        for j, tj in zip(count(1), t):
            d = S[i - 1, j - 1] + score(si, tj)
            h = S[i, j - 1] + gapscore
            v = S[i - 1, j] + gapscore
            opt = max(d, h, v)
            S[i, j] = opt
            T[i, j] = (d == opt) * DIAGONAL + (h == opt) * HORIZONTAL + (v == opt) * VERTICAL
    max_val = -1000
    ind = 0
    for i, v in enumerate(S[-1]):
            temp = v
            if temp > max_val:
                max_val = temp
                ind = i

    A = Pattern_traceback(m, ind, T, s, t)

    return max_val, A





def traceback(i, j, T, s, t, *, GAP='-'):
    # We reconstruct the alignment by traceback (T) from i, j
    As, At = [], []  # build rows of alignment in As (for s), At (for t)
    while T[i,j] != HOME:
        trace = T[i,j]
        if (trace & DIAGONAL):
            i -= 1;  As.append(s[i])
            j -= 1;  At.append(t[j])
            continue
        if (trace & HORIZONTAL):
            As.append(GAP)
            j -= 1; At.append(t[j])
            continue
        assert trace & VERTICAL
        i -= 1; As.append(s[i])
        At.append(GAP)
    # create the final alignment (pair of strings)
    return ("".join(As[::-1]), "".join(At[::-1]))



def overlap_traceback(i, j, T, s, t, *, GAP='-'):
    # We reconstruct the alignment by traceback (T) from i, j
    As, At = [], []  # build rows of alignment in As (for s), At (for t)
    while T[i, j] != HOME:
        trace = T[i, j]
        if (trace & DIAGONAL):
            i -= 1;
            As.append(s[i])
            j -= 1;
            At.append(t[j])
            continue
        if (trace & HORIZONTAL):
            As.append(GAP)
            j -= 1;
            At.append(t[j])
            continue
        assert trace & VERTICAL
        i -= 1;
        As.append(s[i])
        At.append(GAP)
    # create the final alignment (pair of strings)
    s1 = "".join(As[::-1])
    s2 = "".join(At[::-1])
    count = 0
    for c in s1:
        if c != "-":
            count += 1
    new_added_part = s[count:]
    new_s = s1 + new_added_part

    for i in range(len(new_s)-len(s2)):
        s2 = s2 + "-"

    return (new_s, s2)



def Pattern_traceback(i, j, T, s, t, *, GAP='-'):
    # We reconstruct the alignment by traceback (T) from i, j
    As, At = [], []  # build rows of alignment in As (for s), At (for t)
    while T[i,j] != HOME:
        if i==0:
            break
        trace = T[i,j]
        if (trace & DIAGONAL):
            i -= 1;  As.append(s[i])
            j -= 1;  At.append(t[j])
            continue
        if (trace & HORIZONTAL):
            As.append(GAP)
            j -= 1; At.append(t[j])
            continue
        assert trace & VERTICAL
        i -= 1; As.append(s[i])
        At.append(GAP)
    # create the final alignment (pair of strings)
    s1 = "".join(As[::-1])
    s2 = "".join(At[::-1])
    return (s1, s2)


def get_scoring_scheme(name, gapcost=None):
    if name == "unit":
        gapscore = -gapcost if gapcost is not None else -1
        def score(a, b=None):
            if a is None:
                assert b is None
                return gapscore
            return 1 if a==b else -1
        return score
    if ':' in name:
        values = list(map(int, name.split(":")))
        if len(values) != 3:
            raise ValueError(f"need match:mismatch:gap scores (3 values); got {name}")
        match, mismatch, gap = values
        gap = -gapcost if gapcost is not None else gap
        if match < 0 or mismatch > 0 or gap > 0:
            raise ValueError(f"need match >= 0 , mismatch <= 0, gap <= 0; got {name}")
        def score(a, b=None):
            if a is None:
                assert b is None
                return gap
            return match if a==b else mismatch
        return score
    # TODO: you can check for other scoring schemes here
    # Always define and return a 'score' function as in the examples above.
    raise ValueError(f"unknown scoring scheme '{name}'")


def get_argument_parser():
    p = ArgumentParser(description="compute optimal alignment score and alignment for two sequences")
    p.add_argument("x", help="first sequence")
    p.add_argument("y", help="second sequence")
    p.add_argument("--type", default='global',
        choices=("global", "local", "overlap", "semiglobal", "patternsearch"),
        help="type of alignment (so far: global, local)")
    p.add_argument("--scores", default='unit',
        help="scoring scheme (so far: 'unit' or match:mismatch:gap)")
    p.add_argument("--gapcost", type=int,
        help="override gap cost (must be >= 0, score is -cost)")
    return p

def main(args):
    score = get_scoring_scheme(args.scores, gapcost=args.gapcost)
    aligner = {
        'global': needleman_wunsch,
        'local': smith_waterman,
        'semiglobal': patternsearch,
        'patternsearch': patternsearch,
        'overlap': overlap,
        }[args.type]
    s, A = aligner(args.x, args.y, score)
    print(*A, sep='\n')  # print alignment
    print(s)  # print score


if __name__ == "__main__":
    p = get_argument_parser()
    args = p.parse_args()
    main(args)
