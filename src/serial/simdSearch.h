#ifndef SIMD_SEARCH_H
#define SIMD_SEARCH_H

#include <immintrin.h>
#include <vector>
#include "mathHeader.h"

using reg = __m256;   //register 256 bit for float
using regi = __m256i; //register 256 bit for int
using regd = __m256d; //register 256 bit for double

//vector less than or equal comparison between x_vec and 256 bits of *y_ptr
int cmp(regi x_vec, int *y_ptr)
{
    //load 256 bit from y_ptr
    regi y_vec = _mm256_lddqu_si256((regi *)y_ptr);

    // cout << "y_vec: " ;
    // for(int i = 0; i < 4; i++)
    // {
    //     cout  << (unsigned int) y_vec[i]  << " " << (unsigned int) (y_vec[i] >> 32)  << " " ;
    // }
    // cout << "x_vec:" ;
    // for(int i = 0; i < 4; i++)
    // {
    //     cout << (unsigned int) x_vec[i]  << " " << (unsigned int) (x_vec[i] >> 32)  << " ";
    // }

    //avx2 instruction for comparison
    regi mask = _mm256_cmpgt_epi32(x_vec, y_vec);
    // bin(_mm256_movemask_epi8(mask));
    //avx2 instruction for creating mask from the most significant bit of each 8-bit element in a
    return _mm256_movemask_epi8(mask);
}

//search for key in btree till the leaves the level
//return the index of the value if found, or -1 otherwise
int searchSimd(int x, int B, int totalNodes, std::vector<int> &btree, int regBlocks)
{
    int k = 0;
    int res = -1;
    //avx instruction to make 4 copies of keys
    regi x_vec = _mm256_set1_epi32(x);

    int currentIndex = 0;
    int subIndex = 0;

    //loop to search for key starting from root till leaves level
    while (k < totalNodes)
    {
        int mask[regBlocks];
        //store the avx comparison for each 256 bit of the btree node in mask
        for (int i = 0; i < regBlocks; ++i)
        {
            mask[i] = ~cmp(x_vec, &btree[k * B + 1 + i * 8]);
        }

        // cout << endl;
        // bin(mask[1]);
        // bin(mask[0]);
        // cout <<endl;
        subIndex = 0;

        // find first non-zero byte in mask[1..blocks]
        for (int i = 0; i < regBlocks; ++i)
        {
            subIndex = (__builtin_ffs(mask[i]) >> 2);
            if (subIndex != 0)
            {
                subIndex += i * 8;
                break;
            }

            if (mask[i] & 1 == 1)
            {
                subIndex += i * 8;
                break;
            }
            if (i == regBlocks - 1)
                subIndex = B;
        }
        //check if the key is located within the first B subtrees
        if (subIndex < B)
            currentIndex = k;
        k = go(k, subIndex, B);
    }
    res = btree[currentIndex * B + subIndex + 1] == x ? currentIndex * B + subIndex + 1 : res;
    return res;
}


//vector less than or equal comparison between x_vec and 256 bits of *y_ptr
int cmp(reg x_vec, float *y_ptr)
{
    //avx load 256 instruction
    reg y_vec = _mm256_loadu_ps(y_ptr); //load 256-bits (composed of 8 packed single-precision (32-bit) floating-point elements) from memory into dst
    //avx2 instruction for comparison
    regi mask = _mm256_cmpgt_epi32(_mm256_castps_si256(x_vec), _mm256_castps_si256(y_vec));
    //avx2 instruction for creating mask from the most significant bit of each 8-bit element in a
    return _mm256_movemask_epi8(mask);
}
//search for key in btree till the leaves level, while going through each node in a avx manner.
//return the index of the value if found, or -1 otherwise
int searchSimd(float x, int B, int totalNodes, std::vector<float> &btree, int regBlocks)
{
    int k = 0;
    int res = -1;
    //avx instruction to make 4 copies of keys
    reg x_vec = _mm256_set1_ps(x);

    int currentIndex = 0;
    int subIndex = 0;

    //loop to search for key starting from root till leaves level
    while (k < totalNodes)
    {
        int mask[regBlocks];
        //store the avx comparison for each 256 bit of the btree node in mask
        for (int i = 0; i < regBlocks; ++i)
        {
            mask[i] = ~cmp(x_vec, &btree[k * B + 1 + i * 8]);
        }

        //find first non-zero 2bytes in mask[1..blocks]
        subIndex = 0;
        for (int i = 0; i < regBlocks; ++i)
        {
            subIndex = (__builtin_ffs(mask[i]) >> 2);
            if (subIndex != 0)
            {
                subIndex += i * 8;
                break;
            }

            if (mask[i] & 1 == 1)
            {
                subIndex += i * 8;
                break;
            }
            if (i == regBlocks - 1)
                subIndex = B;
        }
        //check if the key is located within the first B subtrees
        if (subIndex < B)
            currentIndex = k; 
        k = go(k, subIndex, B);
    }
    res = btree[currentIndex * B + subIndex + 1] == x ? currentIndex * B + subIndex + 1 : res;
    return res;
}

//vector less than or equal comparison between x_vec and 256 bits of *y_ptr
int cmp(regi x_vec, int64_t *y_ptr)
{
    //avx load 256 instruction
    regi y_vec = _mm256_lddqu_si256((regi *)y_ptr);
    //avx2 instruction for comparison
    regi mask = _mm256_cmpgt_epi64(x_vec, y_vec);
    //avx2 instruction for creating mask from the most significant bit of each 8-bit element in a
    return _mm256_movemask_epi8(mask); 
}
//search for key in btree till the leaves the level
//return the index of the value if found, or -1 otherwise
int searchSimd(int64_t key, int B, int totalNodes, std::vector<int64_t> &btree, int regBlocks)
{
    int k = 0;
    int res = -1;
    //avx instruction to make 4 copies of key
    regi x_vec = _mm256_set1_epi64x(key);

    int currentIndex = 0;
    int subIndex = 0;

    //loop to search for key starting from root till leaves level
    while (k < totalNodes)
    {
        int mask[regBlocks];
        //store the avx comparison for each 256 bit of the btree node in mask
        for (int i = 0; i < regBlocks; ++i)
        {
            mask[i] = ~cmp(x_vec, &btree[k * B + 1 + i * 4]);
        }

        //find first non-zero 2bytes in mask[1..blocks]
        subIndex = 0;
        for (int i = 0; i < regBlocks; ++i)
        {
            subIndex = (__builtin_ffs(mask[i]) >> 3);
            if (subIndex != 0)
            {
                subIndex += i * 4;
                break;
            }

            if (mask[i] & 1 == 1)
            {
                subIndex += i * 4;
                break;
            }
            if (i == regBlocks - 1)
                subIndex = B;
        }
        //check if the key is located within the first B subtrees
        if (subIndex < B)
            currentIndex = k;
        k = go(k, subIndex, B); // go to next node
    }
    //if key is found in the leaf return index, otherwise return -1
    res = btree[currentIndex * B + subIndex + 1] == key ? currentIndex * B + subIndex + 1 : res;
    return res;
}

//vector less than or equal comparison between x_vec and 256 bits of *y_ptr
int cmp(regd x_vec, double *y_ptr)
{
    //avx load 256 instruction
    regd y_vec = _mm256_loadu_pd(y_ptr);
    //avx2 instruction for comparison
    regi mask = _mm256_cmpgt_epi64(_mm256_castpd_si256(x_vec), _mm256_castpd_si256(y_vec));
    //avx2 instruction for creating mask from the most significant bit of each 8-bit element in a
    return _mm256_movemask_epi8(mask);
}
//search for key in btree till the leaves the level
//return the index of the value if found, or -1 otherwise
int searchSimd(double key, int B, int totalNodes, std::vector<double> &btree, int regBlocks)
{
    int k = 0;
    int res = -1;
    //avx instruction to make 4 copies of key
    regd x_vec = _mm256_set1_pd(key);

    int currentIndex = 0;
    int subIndex = 0;

    //loop to search for key starting from root till leaves level.
    while (k < totalNodes)
    {
        int mask[regBlocks];
        //store the avx comparison for each 256 bit of the btree node in mask
        for (int i = 0; i < regBlocks; ++i)
        {
            mask[i] = ~cmp(x_vec, &btree[k * B + 1 + i * 4]);
        }

        //find first non-zero 2bytes in mask[1..blocks]
        subIndex = 0;
        for (int i = 0; i < regBlocks; ++i)
        {
            subIndex = (__builtin_ffs(mask[i]) >> 3);
            if (subIndex != 0)
            {
                subIndex += i * 4;
                break;
            }

            if (mask[i] & 1 == 1)
            {
                subIndex += i * 4;
                break;
            }
            if (i == regBlocks - 1)
                subIndex = B;
        }
        //check if the key is located within the first B subtrees
        if (subIndex < B)
            currentIndex = k;
        k = go(k, subIndex, B); // go to next node
    }
    //if key is found in the leaf return index, otherwise return -1
    res = btree[currentIndex * B + subIndex + 1] == key ? currentIndex * B + subIndex + 1 : res;
    return res;
}

#endif