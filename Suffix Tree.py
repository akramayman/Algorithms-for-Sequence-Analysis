from collections import defaultdict, Counter, namedtuple
from argparse import ArgumentParser
from anytree import Node, RenderTree
from anytree.exporter import DotExporter

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
    return sort_bucket(T, range(len(T)), [], order=1)


def compute_lcp(T, pos):
    """
    lcp using Kasai's linear-time algorithm on numpy arrays
    """
    n = len(pos)
    lcp = [0] * (n+1)
    rank = [0] * (n+1)
    lcp[0] = lcp[n] = -1  # border sentinels
    # compute rank, the inverse of pos (w/o sentinel -1)
    for r in range(n):
        rank[pos[r]] = r

    lp = 0 # current common prefix length
    for p in range(n-1):
        r = rank[p]
        if r == 0:  # pos[r] must be a sentinel, so lcp[r]=0
            lcp[r] = 0
            continue
        pleft = pos[r - 1]  # r-1 is now valid
        while T[p + lp] == T[pleft + lp]:
            lp += 1
        lcp[r] = lp
        lp = lp - 1 if lp > 0 else 0  # next suffix: lose first character
    return lcp


def build_suffixtree_from_array(pos, lcp,T):
    length=max(pos)
    root=Node("root")
    index=0
    innerlevel=0
    while (index<length):
        value=lcp[index]
        if value==-1 and index==0:
            Child=Node("$",parent=root,P=pos[index],Text=T[pos[index]])
            innerlevel += 1
            index+=1
        elif value==0:
            position=pos[index]
            if position==length-1:
                label=T[position]
            else:
                label=T[position:length]
                innerlevel+=1
            globals()["child"+label]=Node(label,parent=root,i_=innerlevel,Text=label)
            globals()["child$" + label]=Node("$",parent=globals()["child"+label],P=pos[index],Text="$")
            if lcp[index+1]==0:
                index+=1
                continue
            else:
                for inner in range (index+1,len(lcp)-1):
                    inner_value=lcp[inner]
                    inner_pos=pos[inner]
                    inner_label=T[inner_value+inner_pos:length+1]
                    globals()["child"+label + inner_label] = Node(inner_label, parent=globals()["child" + label],P=pos[inner],Text=inner_label)
                    if lcp[inner+1]==0:
                        break
                index=inner+1
    return root


# def suffixtree_to_dot(root, T, *, label="suffixtree"):
#     # root: the tree (repesented by its root)
#     # T: the text (annotate edges by substrings of T)
#     # label: for the header line `digraph suffixtree { ... }`
#     # Return a multiline string that can be printed to stdout.
#     contents = []
#     # TODO: convert suffix tree to DOT notation
#     #for i in DotExporter(root,graph=label,nodeattrfunc=lambda node: "shape=box"):
#     # contents.append(root)
#         # print(i)
#
#     # Each line of the DOT file should be a string in contents
#     lines = [f"digraph {label}" + "{"] + contents + ["}"]
#     return "\n".join(lines)



def main(args):
    T = args.text
    # check length and sentinel
    if len(T) > 99:
        raise ValueError(f"only texts of length <= 99 are supported")
    C = Counter(T)
    if C[T[-1]] > 1:
        raise ValueError(f"sentinel {T[-1]} is not unique in text {T}")
    if T[-1] != sorted(C.keys())[0]:
        raise ValueError(f"sentinel {T[-1]} is not smallest in text {T}")
    # compute suffix array and lcp array
    pos = compute_pos_manber_myers(T)
    lcp = compute_lcp(T, pos)
    # build the suffix tree (S is the root node); then get DOT string
    S = build_suffixtree_from_array(pos, lcp,T)

    print(RenderTree(S))
    #dot = suffixtree_to_dot(S, T)
    #print(dot)  # to stdout


def get_argument_parser():
    p = ArgumentParser(description="Suffix Tree Drawing Tool")
    p.add_argument("text",
        help="text (with sentinel, must be unique and smallest character)")
    return p



if __name__ == "__main__":
    main(get_argument_parser().parse_args())
