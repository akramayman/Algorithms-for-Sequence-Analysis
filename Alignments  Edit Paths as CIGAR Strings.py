from argparse import ArgumentParser
from collections import deque


def compute_all_cigars(m, n):
    """
    Print one cigar string per line to cigars.txt
    cigar.txt should contain the cigar strings for m=n=5.
    """
    op1, op2 = all_alignments(m, n)#take the list from all_alginment function
    cigar = []
    for ref, read in zip(op1, op2):
        out = []
        for i, j in zip(ref, read):
            if i == " " and j:
                out.append("I")
            elif j == " " and i:
                out.append("D")
            else:
                out.append("M")
        output = "".join(out)
        cigar.append(output)

    with open("cigars.txt", "w") as f:
        for i, s in enumerate(cigar):
            if i == number_of_alignments(len(m), len(n)):
                f.write(s)
            else:
                f.write(s + "\n")


def number_of_alignments(s, t):
    """
    retrun the number of possible cigar strings for two strings with the length of n and m
    """
    n = 0
    Dc = [1] * (s + 1)
    Dp = [1] * (s + 1)
    k = 1
    p = [1] * (s + 1)
    for j in range(t):
        Dp, Dc = Dc, Dp
        for i in range(s):
            Dp[i] = Dp[i - 1] + Dc[i] + Dc[i - 1]
            p[i] = k
    n = Dp[i]
    return n


def all_alignments(x, y):#function that create two list of string have all combination of string (and taking the main idea to find these combination from paper "By John Lekberg")
    def F(x, y):
        if len(x) == 0 and len(y) == 0:
            yield deque()

        scenarios = []
        if len(x) > 0 and len(y) > 0:
            scenarios.append((x[0], x[1:], y[0], y[1:]))
        if len(x) > 0:
            scenarios.append((x[0], x[1:], None, y))
        if len(y) > 0:
            scenarios.append((None, x, y[0], y[1:]))
        for xh, xt, yh, yt in scenarios:
            for alignment in F(xt, yt):
                alignment.appendleft((xh, yh))
                yield alignment

    alignments = F(range(len(x)), range(len(y)))

    op_1 = []
    op_2 = []

    for alignment in map(list, alignments):
        str_1 = "".join(" " if i is None else x[i] for i, _ in alignment)
        str_2 = "".join(" " if j is None else y[j] for _, j in alignment)
        op_1.append(str_1)
        op_2.append(str_2)

    return op_1, op_2


def main(args):
    n = number_of_alignments(args.m, args.n)
    compute_all_cigars(args.m, args.n)


def get_argument_parser():
    p = ArgumentParser(description="Alignments or Edit Paths as Cigar Strings")
    p.add_argument("-n", default=5, type=int,
                   help="length of string one")
    p.add_argument("-m", default=5, type=int,
                   help="length of string two")
    return p


if __name__ == '__main__':
    #main(get_argument_parser().parse_args())
    x="ABABC"
    y="ABAAB"
    print(number_of_alignments(3,2))
    print(number_of_alignments(6,4))
    print(number_of_alignments(3,3))
    print(number_of_alignments(3,9))
    with open("cigars.txt", "rt") as cfile:
        all_cigars = cfile.read().split()
        all_cigars.sort()
        print(all_cigars[-1])
        print(all_cigars[0])
        print(all_cigars[957])
        print(all_cigars[263])
