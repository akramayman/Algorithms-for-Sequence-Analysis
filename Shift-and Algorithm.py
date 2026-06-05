import argparse  # for command line interface

def build_nfa_and(P):
    masks = dict()
    accept_state = 0
    bit=1
    for c in P:
        if c not in masks:masks[c]=0
        masks[c]=masks[c] | bit
        bit=bit*2
    accept_state=bit//2

    return masks, accept_state


def build_nfa_or(P):
    masks = dict()
    accept_state = 0
    bit = 1
    for c in P:
        if c not in masks:masks[c]=0
        masks[c]=masks[c]& bit
        bit=bit*2
    accept_state = bit//2

    return masks, accept_state


def shift_and(masks, accept, text, N):
    k=0
    results = []
    D = 0
    for i, c in enumerate(text):
        D = ((D << 1) | 1) & masks[c]
        if (D & accept) != 0:
            results.append(i)
            k += 1
    return k,results


def shift_or(mask, accept, text, N):
    k = 0
    results = []
    D = 0
    for i, c in enumerate(text):
        D = ((D << 1) | 1) & mask[c]
        if (D & accept) != 0:
            results.append(i)
            k+=1
    return k, results


def get_text(args):
    if args.text is not None:
        return args.text
    with open(args.textfile, "r") as ftext:
        text = ftext.read()
    return text


def get_patterns(args):
    if args.pattern is not None:
        return [args.pattern]  # list with single item
    with open(args.patternfile, "r") as fpat:
        Ps = [pattern.strip() for pattern in fpat.readlines()]
    return Ps


def main(args):
    alg = args.algorithm
    T = get_text(args)  # bytes object
    Ps = get_patterns(args)  # list of bytes objects
    build_nfa = build_nfa_and if alg == "and" else build_nfa_or
    find_matches = shift_and if alg == "and" else shift_or
    NRESULTS = args.maxresults
    for P in Ps:  # iterate over patterns
        if len(P) == 0: continue  # skip empty patterns
        nfa = build_nfa(P)
        nresults, results = find_matches(*nfa, T, NRESULTS)
        if nresults > NRESULTS:
            print("! Too many results, showing first {NRESULTS}")
            nresults = NRESULTS
        print(*list(results[:nresults]), sep="\n")


def get_argument_parser():
    p = argparse.ArgumentParser(description="DNA Motif Searcher")
    pat = p.add_mutually_exclusive_group(required=True)
    pat.add_argument("-P", "--pattern",
        help="immediate pattern to be matched")
    pat.add_argument("-p", "--patternfile",
        help="name of file containing patterns (one per line)")
    txt = p.add_mutually_exclusive_group(required=True)
    txt.add_argument("-T", "--text",
        help="immerdiate text to be searched")
    txt.add_argument("-t", "--textfile",
        help="name of file containing text (will be read in one piece)")
    p.add_argument("-a", "--algorithm", metavar="ALGORITHM",
        default="and", choices=("and", "or"),
        help="algorithm to use ('and' (default), 'or')")
    p.add_argument("--maxresults", "-R", type=int, default=10_000,
        help="maximum number of results to show (10_000)")
    return p


if __name__ == "__main__":
    main(get_argument_parser().parse_args())
