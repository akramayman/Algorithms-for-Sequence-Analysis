import argparse

import numpy as np

def naive_pattern_matching(P, T):
    fs=len(T)
    fr=len(P)
    n = 0
    positions = []
    comps = 0
    for i in range(fs - fr + 1):
        for j in range(fr):
            comps+=1
            if T[i + j] != P[j]:
                break
            if (j == (fr - 1)):
                #print("Pattern found at index ", i)
                n += 1
                positions.append(i)

    found=bool(n!=0)

    return found, n, positions, comps

def get_text(args):
    text = ""
    if args.text is not None:
        return args.text
    with open(args.textfile, "r") as ftext:
        text = "".join(ftext.read().split())
    return text


def get_patterns(args):

    Ps = []
    if args.pattern is not None:
        return [args.pattern]  # list with single item
    with open(args.patternfile, "r") as fpat:
        Ps = [pattern.strip() for pattern in fpat.readlines()]

    return Ps


def main(args):
    T = get_text(args)
    Ps = get_patterns(args)

    for P in Ps:  # iterate over patterns
        if len(P) == 0: continue  # skip empty patterns
        print(f"> {P}")
        found, n , positions, comps = naive_pattern_matching(P, T)
        print(f"Pattern {P}:\n Found: {found}\n Occurred: {n} times \n Positions: {positions}\n Comparisons: {comps}")


def get_argument_parser():
    p = argparse.ArgumentParser(description="DNA naive pattern matching")
    pat = p.add_mutually_exclusive_group(required=True)
    pat.add_argument("-P", "--pattern",
        help="immediate pattern to be matched")
    pat.add_argument("-p", "--patternfile",
        help="name of file containing patterns (one per line)")
    txt = p.add_mutually_exclusive_group(required=True)
    txt.add_argument("-T", "--text",
        help="immerdiate text to be searched")
    txt.add_argument("-t", "--textfile",
        help="name of file containing text")
    return p


if __name__ == "__main__":
    main(get_argument_parser().parse_args())
    #main(get_argument_parser().parse_args(["-T","TTACGTATTTTTCGAGTACGTT","-P","TTTT"]))
