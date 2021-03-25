/*
Tesing build and search for long integers (64 bits). 
Compile this file as follows:
g++ -std=c++17 -Ddtype=long -mavx2 ../src/serial/mathHeader.cpp test-simd-search-long.cpp
*/

#include <iostream>
#include "../src/serial/mathHeader.h"
#include "../src/serial/simdSearch.h"
#include "../src/serial/seqHorizontalBuild.h"
#include "../src/serial/seqVerticalBuild.h"

using namespace std;


int main(int argc, char **argv)
{
    const int n = 648, B = 8; // set parameters for a tree with 3 levels
    int nblocks = n / B;
    int height = floor(log(nblocks) / log(B + 1));
    int power = binPow(B + 1, height);
    int z = n - power;
    int totalNodes = binPow(B + 1, height + 1) / B;
    cout << "Total tree Nodes: " << totalNodes << endl;
    vector<dtype> tree(totalNodes * B + 1);

    vector<dtype> items(n);
    for (int i = 0; i < n; i++)
        items[i] = i;

    buildPerfectTreeVertical(items, tree, 1, 0, totalNodes * B + 1, height, B);
    vector<ll> ans(items.size());

    for (int i = 0; i < items.size(); i++)
    {
        ans[i] = searchSimd(items[i], B, totalNodes, tree, B/4);
    }
    cout << "assert every element existing in the tree is found: ";
    bool allFound = true;
    for (int i = 0; i < ans.size(); i++)
    {
        if (tree[ans[i]] != items[i])
        {
            cout << ans[i] << " ";
            allFound = false;
        }
    }
    if (allFound)
        cout << "OK!" << endl;
    else
        cout << "Found errors" << endl;

    vector<dtype> keys = {n, 5000, 6000};
    cout << "assert boundary cases: ";

    vector<unsigned int> ansBoundary(keys.size());
    for (int i = 0; i < keys.size(); i++)
    {
        ansBoundary[i] = searchSimd(keys[i], B, totalNodes, tree, B/4);
    }
    allFound = true;
    for (int i = 0; i < ansBoundary.size(); i++)
    {
        if (ansBoundary[i] != -1)
        {
            cout << ansBoundary[i] << " ";
            allFound = false;
        }
    }

    if (allFound)
        cout << "OK!" << endl;
    else
        cout << "Found errors" << endl;
    cout << "Done testing long!!" << endl;
    return 0;
}

// good notes: https://richardstartin.github.io/posts/finding-bytes
// https://arxiv.org/pdf/1611.07612.pdf
// more details: https://gms.tf/stdfind-and-memchr-optimizations.html