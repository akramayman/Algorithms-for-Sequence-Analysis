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

# Assignment 01 – Implementation of Naive Pattern Search

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
