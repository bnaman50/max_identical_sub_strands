# max_identical_sub_strands

## Requirements
Python 3

## Usage
`python identitical_substring.py`

## Problem Statement 
Please refer to the file [Problem_Longest_Strand.md](Problem_Longest_Strand.md) for the problem description. 

## Assumptions
> longest strand of bytes that is identical between two or more files

I assumed we need the longest matching (identical/continuous) sub-strand (MIS) and not the standard longest common subsequence (LCS). 
<br />
For example - 
<br />
&emsp;&emsp;&emsp; Inputs - 'abcde' and 'abce' <br />
&emsp;&emsp;&emsp; LCS - 'abce' <br />
&emsp;&emsp;&emsp;	MIS - 'abc' <br />

Anyways, I believe my key insight will still hold in the case of LCS as well.  

## Key Insight
At a crude level, you would have to find MIS for all the combinations of file ranging from 2 to n (where n is the number of input files). Particularly, you would have to check for 
<br />
```
nC2 + nC3 + ... + nCn
```
combinations. 
<br />
But this is going to be very time-intensive. My key insight is that **I don't need to look for anything more than `nC2` combinations since `MIS(S1, S2, ..., Si) <= MIS(S1, S2)`** (where `Si`'s are various strings and `i` is greater than 2.)

## Results 
```
The length of maximum strand is 27648. It occurs in following sets of files

Set: 1/1
Its files and corresponding offsets are as follows:
File name: sample.2, Offset: 3072
File name: sample.3, Offset: 17408
```
It is possible that there are two sets of file with different maximum identical sub strands. I print all such sets seperately. 
<br />
<br />
Note: Here offset means the index from where the identical part starts (not the one before it). Look at the follwoing picture for refeence since I am using the same function. 
![note_pic](https://user-images.githubusercontent.com/5251592/115482552-97842e80-a214-11eb-9ed8-4b5e374bc7e8.png)

In the above picture, offset is 0 for the first input and 4 for the second input.

## Future
On further thinking, I realized that you can make it even faster but I am gonna leave it for future. The idea is that I am going redundant work while calculating `MIS(S1, S3)` once I have computed `MIS(S1, S2)` and `MIS(S2, S3)`. 
```
MIS(S1, S3) = (left-side) + MIS(MIS(S1, S2), MIS(S2, S3))
```
<br />
I believe this will be faster on avergae since you are now computing `MIS` on much smaller strings/files. 
