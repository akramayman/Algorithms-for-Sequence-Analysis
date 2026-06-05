# kmerindex.py
from collections import defaultdict, Counter
from argparse import ArgumentParser
import numpy as np
from numba import njit, int32, uint8, uint64


def _fasta_reads_from_filelike(f, COMMENT=b';'[0], HEADER=b'>'[0]):
    """internal function that yields facta records as (header: bytes, seq: bytearray)"""
    strip = bytes.strip
    header = seq = None
    for line in f:
        line = strip(line)
        if len(line) == 0:
            continue
        if line[0] == COMMENT:
            continue
        if line[0] == HEADER:
            if header is not None:
                yield (header, seq)
            header = line[1:]
            seq = bytearray()
            continue
        seq.extend(line)
    if header is not None:
        yield (header, seq)


def make_genome_text(filename, sep=ord("&"), end=ord("$")):
    """
    Create a concatenated text from a genomic FASTA file,
    using the given sequence separator byte (sep) and sentinel byte (end).
    Return a bytearray with the concatenated bytes.
    """
    text = bytearray()
    with open(filename, "rb") as f:
        for (header, seq) in _fasta_reads_from_filelike(f):
            text.extend(seq)
            text.append(sep)  # the separator byte
        text.append(end)  # the end byte (sentinel)
    return bytes(text)


def compute_pos_manber_myers(T):
    """
    using classical Manber-Myers doubling technique.
    OK performance of O(n log n) time -- this implementation may be slower.
    """
    def sort_bucket(t, bucket, result, order=1):
        d = defaultdict(list)
        for i in bucket:
            key = t[i:i+order]
            d[key].append(i)
        for k, v in sorted(d.items()):
            if len(v) > 1:
                result = sort_bucket(t, v, result, order*2)
            else:
                result.append(v[0])
        return result
    result = sort_bucket(T, range(len(T)), [], order=1)  # Python list
    pos = np.array(result, dtype=np.int32)  # convert to numpy array
    return pos


@njit
def compute_lcp(T, pos):
    """
    lcp using Kasai's linear-time algorithm on numpy arrays
    """
    n = len(pos)
    lcp = np.zeros(n+1, dtype=np.int32)
    lcp[0] = lcp[n] = -1  # border sentinels
    # compute rank, the inverse of pos
    rank = np.zeros(n, dtype=np.int32)
    for r in range(n):
        rank[pos[r]] = r

    lp = 0 # current common prefix length
    for p in range(n-1):
        r = rank[p]
        if r == 0:  # pos[r] must be a sentinel, so lcp[r]=0
            lcp[r] = 0
            continue
        pleft = pos[r-1]  # r-1 is now valid
        while T[p+lp] == T[pleft + lp]:
            lp += 1
        lcp[r] = lp
        lp = lp - 1 if lp > 0 else 0  # next suffix: lose first character
    return lcp


def print_arrays(T, pos, lcp):
    for r in range(len(pos)):
        print(f"{pos[r]:2d}  {lcp[r]:2d}  {T[pos[r]:].decode('ASCII')}")


_DNATRANSLATE = np.full(256, 4, dtype=np.uint8)
_DNATRANSLATE[ord('A')] = 0
_DNATRANSLATE[ord('C')] = 1
_DNATRANSLATE[ord('G')] = 2
_DNATRANSLATE[ord('T')] = 3


@njit(locals=dict(code=uint64))
def encode(kmer, translate=_DNATRANSLATE):
    code = 0
    return uint64(-1)


@njit
def compute_kmer_index(T, pos, lcp, k):
    length = 0
    start = np.zeros(length)
    return start


def show_length_histogram(start):
    pass


def get_argument_parser():
    p = ArgumentParser(description="computes a k-mer index of a genomic FASTA file")
    p.add_argument("fasta",
        help="name of FASTA file (genome)")
    p.add_argument("-k", type=int, default=9,
        help="k-mer length (default 9)")
    return p


def main(args):
    print(f"# Reading '{args.fasta}'...")
    T = make_genome_text(args.fasta, sep=ord("&"), end=ord("$"))
    n = len(T)
    print(f"# Genome length: {n}")
    k = args.k
    print(f"# Computing suffix array...")
    pos = compute_pos_manber_myers(T)
    print(f"# Computing lcp array...")
    lcp = compute_lcp(T, pos)
    if n <= 50: print_arrays(T, pos, lcp)  # only actually prints short texts
    # compute q-gram index and show histogram
    print(f"# Computing k-mer index for k={k}")
    start = compute_kmer_index(T, pos, lcp, k)
    show_length_histogram(start)
    print(f"# Done.")


if __name__ == "__main__":
    p = get_argument_parser()
    args = p.parse_args()
    main(args)
