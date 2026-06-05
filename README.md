# Algorithms-for-Sequence-Analysis

<p align="left">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
</p>

This repository contains implementations and assignments for the course “Algorithms for Sequence Analysis” at Saarland University (M.Sc. Bioinformatics / Computer Science).

The course covers fundamental and advanced algorithms used in sequence analysis, with applications in bioinformatics such as pattern matching, sequence alignment, indexing structures, genome analysis, and motif discovery.

## 📚 Course Topics

- Exact pattern matching algorithms (naïve, automata-based, bit-parallel methods)
- Full-text index structures (suffix trees, suffix arrays)
- Succinct data structures (FM-index) and backward search
- Approximate pattern matching and read mapping
- Pairwise sequence alignment (global/local alignment, optimizations)
- Score matrices and evolutionary models
- Alignment statistics
- Multiple sequence alignment techniques
- Alignment-free methods (k-mers, hashing, min-hashing, LSH)
- Genome assembly basics
- Motif search and discovery

## 🎯 Purpose

The goal of this repository is to:

- Implement classical and modern sequence analysis algorithms
- Understand their computational complexity and applications
- Apply them to bioinformatics problems

# Algorithm 01 – Implementation of Naive Pattern Search

## 📌 Overview

This assignment implements the **Naive Pattern Search algorithm**, which is the simplest method for finding occurrences of a pattern within a text. The algorithm checks every possible alignment of the pattern in the text and compares characters one by one.

---

## 🧠 Algorithm: Naive Pattern Search

### 💡 Idea
The naive approach slides the pattern over the text one position at a time and checks for a match at each position.

For each shift:
- Compare the pattern with the current substring of the text
- If all characters match → report occurrence
- Otherwise → shift by one position

---
# Algorithm 02 – Implementation of Shift-And Algorithm

## 📌 Overview

This assignment focuses on implementing the **Shift-And (Bitap) algorithm**, an efficient exact pattern matching technique based on bitwise operations. It is particularly effective for searching patterns in texts over small alphabets and demonstrates how bit-parallelism can significantly speed up string matching.

---

## 🧠 Idea

The Shift-And algorithm represents the state of pattern matching using **bitmasks**, where each bit corresponds to a position in the pattern.

- Each character in the pattern is encoded into a bitmask.
- As the text is processed character by character, a bit-vector is updated using bitwise shifts and AND operations.
- A match is detected when a specific bit (corresponding to the end of the pattern) becomes set.

The key idea is to simulate a finite automaton using **bit-level parallelism**, allowing multiple comparisons to be performed simultaneously using fast CPU operations.

---

# Algorithm 03 – Suffix Trees from Suffix Arrays 

## 📌 Overview

This task focuses on constructing a suffix tree from a suffix array and LCP array and exporting the resulting tree in DOT format for visualization using Graphviz.

---

## 🧠 Idea

The suffix tree is reconstructed indirectly using:
- The **suffix array**, which provides lexicographic ordering of suffixes
- The **LCP array**, which provides the longest common prefix between consecutive suffixes

By tracking changes in LCP values, the structure of the suffix tree can be derived without explicitly building it from scratch.

---
# Algorithm 04 – Maximal Unique Matches

## 📌 Overview

This task focuses on identifying maximal unique matches (MUMs) between two bacterial genomes using suffix arrays and LCP arrays constructed from a concatenated genome sequence.

---

## 🧠 Idea

The two genomes are concatenated into a single string, and a suffix array and LCP array are built over it.

MUMs are then extracted as substrings that:
- Appear exactly once in each genome
- Are maximal, meaning they cannot be extended without losing uniqueness

This allows efficient comparison of genomic similarity based on shared unique substrings.

---

# Algorithm 5 – Alignments / Edit Paths as CIGAR Strings

## 📌 Overview

This assignment focuses on enumerating all possible alignments between two strings and representing them as **edit paths**, also known as **CIGAR strings**.

Additionally, it analyzes the number of possible alignments for two strings of length 5.

---

## 🧠 Idea

An alignment between two strings can be represented as a sequence of edit operations:

- **M** → match or mismatch (align one character from each string)
- **I** → insertion (gap in the second string)
- **D** → deletion (gap in the first string)

Each alignment corresponds to a path from `(0,0)` to `(m,n)` in a grid:
- Right move → I
- Down move → D
- Diagonal move → M

All valid paths represent all possible alignments between the two strings.

For strings of length `m = n = 5`, the number of possible alignments corresponds to all monotonic paths in a 2D grid using these three move types.

---

## 📌 CIGAR Representation

A **CIGAR string** encodes an alignment as a sequence of operations:

- `M` → match/mismatch (diagonal step)
- `I` → insertion (horizontal step)
- `D` → deletion (vertical step)

### Examples (length = 5):
- `MMMMM`
- `IIIIIDDDDD`

Each valid combination of these operations corresponds to a unique edit path.

---

# Algorithm 6 – Distances of Random Strings

## 📌 Overview

This assignment investigates the relationship between **Hamming distance** and **edit distance** by experimentally analyzing random DNA sequences.

The goal is to generate random string pairs, compute both distance measures, and visualize their distributions.

---

## 🧠 Idea

The experiment is based on statistical comparison of two string distance metrics:

### 🔹 Hamming Distance
Measures the number of positions where two strings of equal length differ.

- Only defined for strings of the same length
- Captures simple positional mismatches

### 🔹 Edit Distance (Levenshtein Distance)
Measures the minimum number of operations (insertions, deletions, substitutions) required to transform one string into another.

- More general than Hamming distance
- Accounts for shifts and gaps in alignment

---

