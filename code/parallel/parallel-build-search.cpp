#include <algorithm>
#include <chrono>
#include <iostream>
#include <random>
#include <string>
#include <vector>
#include <immintrin.h>
#include <omp.h>
#include "parallelHorizontalBuild.h"
#include "parallelVerticalBuild.h"
#include "parallelSearch.h"
#include "simdSearch.h"

//#pragma GCC optimize("O3")
#pragma GCC target("avx2")

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

class RandomNumberBetween
{
public:
  RandomNumberBetween(int low, int high)
      : random_engine_{std::random_device{}()}, distribution_{low, high} {}
  int operator()() { return distribution_(random_engine_); }

private:
  std::mt19937 random_engine_;
  std::uniform_int_distribution<int> distribution_;
};

int main(int argc, char **argv)
{
  //***********************************************************
  //check file inputs
  if (argc < 2 || argc > 3)
  {
    std::cout << "Error: Incorrect  number of arguments!" << std::endl;
    std::cout << "Usage: " << argv[0]
              << " <number of items> <number of values in a node>";
    return -1;
  }
  //***********************************************************
  //construct items sequentially 0 -- itemsSize
  auto itemsSize = std::stol(argv[1]);
  auto VAL_SIZE = std::stol(argv[2]);
  auto CHILD_SIZE = VAL_SIZE + 1;
  std::vector<dtype> items;
  items.reserve(itemsSize);
  for (ll i = 0; i < itemsSize; i++)
  {
    items.emplace_back(i);
  }
  //***********************************************************
  //Build tree horizontally
  std::vector<dtype> tree;
  std::vector<dtype> tree2;
  std::vector<dtype> tree3;
  auto start = std::chrono::high_resolution_clock::now();
  buildTreeOptimalHorizontal(items, tree, 1, 0, items.size() - 1, CHILD_SIZE);
  auto finish = std::chrono::high_resolution_clock::now();
  std::chrono::duration<double> elapsed = finish - start;
  std::cout << elapsed.count() << " ";

  //Build tree vertically
  start = std::chrono::high_resolution_clock::now();
  buildTreeOptimalVertical(items, tree3, 1, 0, items.size() - 1, VAL_SIZE);
  finish = std::chrono::high_resolution_clock::now();
  elapsed = finish - start;
  std::cout << elapsed.count() << " ";

  //Construct random queries
  std::vector<dtype> queries;
  // std::generate_n(std::back_inserter(queries), itemsSize, RandomNumberBetween(1, itemsSize + 10));
  for (int i = 0; i < itemsSize; i++)
    queries[i] = items[i]; // non-random queries
  //std::vector<ll> queries = {-1, 2, 0, 3, 5, 16, 10, 17, 18, 200, 30};
  // std::cout << "tree:" << CHILD_SIZE - 1;
  auto totalNodes = (tree.capacity() - 1) / (CHILD_SIZE - 1);
  //auto totalNodes = itemsSize;
  //***********************************************************
  //query the tree sequentially
  start = std::chrono::high_resolution_clock::now();
  auto resultSeq = batchSearchQueriesSeq(tree, totalNodes, queries, VAL_SIZE);
  finish = std::chrono::high_resolution_clock::now();
  elapsed = finish - start;
  //output search time
  std::cout << elapsed.count() << " ";
  //***********************************************************
  //query the tree binary
  start = std::chrono::high_resolution_clock::now();
  auto resultBinary = batchQuerySearchBinary(tree, totalNodes, queries, VAL_SIZE);
  finish = std::chrono::high_resolution_clock::now();
  elapsed = finish - start;
  //output search time
  std::cout << elapsed.count() << " ";
  //***********************************************************
  //query the tree SIMD
  //std::cout << (sizeof(items[0]) * VAL_SIZE);
  if ( (sizeof(items[0]) * VAL_SIZE ) % 64 == 0)
  {
    start = std::chrono::high_resolution_clock::now();
    auto resultSIMD = batchQuerySearchSIMD(tree, totalNodes, queries, VAL_SIZE);
    finish = std::chrono::high_resolution_clock::now();
    elapsed = finish - start;
    //output search time
    std::cout << elapsed.count() << " ";
    
    for (int i = 0; i < resultSIMD.capacity(); i++)
    {
      if (resultSIMD[i] != resultBinary[i])
      {
        std::cout << i << " ";
      }
      // std::cout << resultBinary[i] << " ";
    }
  }
  //***********************************************************
  for (int i = 0; i < resultBinary.capacity(); i++)
    {
      if (resultSeq[i] != resultBinary[i])
      {
        std::cout << i << " ";
      }
      // std::cout << resultBinary[i] << " ";
    }
  std::cout << std::endl;
  return 0;
}
