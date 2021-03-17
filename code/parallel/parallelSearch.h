
#ifndef PARALLEL_SEARCH_H
#define PARALLEL_SEARCH_H
#include <vector>
#include <omp.h>
#include "simdSearch.h"


#if isLong
using ll = long long;
#else
using ll = int;
#endif

#ifndef dtype
using dtype = int;
#endif


#ifndef processors
#define processors 8;
#endif


//search for key in btree till the leaves level, while going through each node sequentially
//return the index of the value if found, or -1 otherwise
//B is total number of values in a node
template <typename T>
ll nodeSequentialSearch(std::vector<T> &tree, ll &B, ll &totalNodes, ll &key)
{
    ll k = 0;
    ll res = -1;
    int currentIndex = 0;
    int subIndex = 0;

    //loop to search for key starting from root till leaves level
    while (k < totalNodes)
    {
        subIndex = 0;
        for (; subIndex < B; subIndex++)
        {
            if (key <= tree[k * B + subIndex + 1])
            {
                break;
            }
        }
        //check if the key is located within the first B subtrees
        if (subIndex < B)
            currentIndex = k;
        k = go(k, subIndex, B);
    }
    res = tree[currentIndex * B + subIndex + 1] == key ? currentIndex * B + subIndex + 1 : res;
    return res;
}

//batch search query function
//B is total number of values in a node
template <typename T>
std::vector<ll> batchSearchQueriesSeq(std::vector<T> &tree, ll totalNodes,
                                      std::vector<T> &queries, ll B)
{
    std::vector<ll> results;
    results.reserve(queries.size());

    #pragma omp parallel for num_threads(processors)
    for (ll i = 0; i < queries.size(); i++)
    {
        results[i] = nodeSequentialSearch(tree, B, totalNodes, queries[i]);
    }
    return results;
}

//search for key in btree till the leaves level, while going through each node sequentially
//return the index of the value if found, or -1 otherwise
//B is total number of values in a node
template <typename T>
ll nodeBinarySearch(std::vector<T> &tree, ll &B, ll &totalNodes, ll &key)
{
    ll k = 0;
    ll res = -1;
    int currentIndex = 0;
    int subIndex = 0;
    //check till you reach leaves level using the two indices nodeIndex and currentIndex
    while (k < totalNodes)
    {
        subIndex = 0;
        ll relativeIndex = k * B + 1;

        typename std::vector<T>::iterator startSearch = (tree.begin() + relativeIndex);
        typename std::vector<T>::iterator endSearch = (tree.begin() + relativeIndex + B);
        subIndex = std::lower_bound(startSearch, endSearch, key) - startSearch;
        //check if the key is located within the first B subtrees
        if (subIndex < B)
            currentIndex = k;
        k = go(k, subIndex, B);
    }
    res = tree[currentIndex * B + subIndex + 1] == key ? currentIndex * B + subIndex + 1 : res;
    return res;
}

//batch search query function
//B is total number of values in a node
template <typename T>
std::vector<ll> batchQuerySearchBinary(std::vector<T> &tree, ll totalNodes,
                                       std::vector<T> &queries, ll B)
{
    std::vector<ll> results;
    results.reserve(queries.size());

    #pragma omp parallel for num_threads(processors)
    for (ll i = 0; i < queries.size(); i++)
    {
        results[i] = nodeBinarySearch(tree, B, totalNodes, queries[i]);
    }
    return results;
}

//batch search query function
//B is total number of values in a node
std::vector<ll> batchQuerySearchSIMD(std::vector<dtype> &tree, ll totalNodes,
                                       std::vector<dtype> &queries, ll B)
{
    std::vector<ll> results;
    results.reserve(queries.size());

    int regBlocks = sizeof(tree[0])*B/32;

    #pragma omp parallel for num_threads(processors)
    for (ll i = 0; i < queries.size(); i++)
    {   
        results[i] = searchSimd(queries[i], B, totalNodes, tree, regBlocks);
    }
    return results;
}

#endif