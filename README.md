# max_identical_sub_strands

## Usage
`python identitical_substring.py`

## Problem Statement 
Please refer to the file [Problem - Longest Strand.md](Problem - Longest Strand.md) for the problem description. 

## Assumptions
> longest strand of bytes that is identical between two or more files

I assumed we need the longest matching (identical/continuous) sub-strand (MIS) and not the standard longest common subsequence (LCS). 
For example - 
Inputs - 'abcde' and 'abce'
	LCS - 'abce'
	MIS - 'abc'

Anyways, I believe my key insight will still hold in the case of LCS as well.  

## Key Insight
