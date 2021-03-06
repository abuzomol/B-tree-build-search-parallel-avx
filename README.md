Requirements:

- INTEL processor that allows AVX2
- C++17
- python3 (matplot, ...NEED LIST OF PACKAGES)
- cmake check verion
- Access to Linux command lscpu

A B-tree is a balanced tree where each node contains B values and B+1 children. 

It generalises the concept of a binary tree and therefore fits more the external memory model where a block of data is read from external memory, 
processed at internal memory, and then written back into the memory.

In modern CPUs, with some simplifications, L3 or L4 can act as an internal memory, while external memory can be the RAM or the main memory.
The size of block is often 64 bytes which is the size of the current cache line.

This code provides some performance measures over different data sizes, different choices for the node size B, the number of processors and different data types. 

The code is general enough to build bottom up and search a tree over any datatype with the exception of AVX2 instructions which require hardcode tweaking.

We offer some plots for the standard C++ datatypes: int, float, long and doubles. Two folders contain the main bulk of the code: code/serial and code/parallel.

To use this code, you can simply run the command: 

```
make run
```

and you will wait for few hours before all the code gets the performance data under data folder in .csv files.

To make pre-designed plots, you can run the command:

```
make plot
```

The code is well-documented, and if a concept is missing, we recommend to read the description at NEED LINK HERE

This is a part of on going project to use B-tree in geometric data structures in general, and point location problem specifically. 

Muzamil Yahia
