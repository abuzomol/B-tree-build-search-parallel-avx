/*
Tesing build and search for floats. 
Compile this file as follows:
g++ -std=c++17 -Ddtype=float -mavx2 ../src/serial/mathHeader.cpp test-simd-search-float.cpp
*/

#include <iostream>
#include "../src/serial/mathHeader.h"
#include "../src/serial/simdSearch.h"
#include "../src/serial/seqHorizontalBuild.h"
#include "../src/serial/seqVerticalBuild.h"

using namespace std;

int main(int argc, char **argv)
{
    const int n = 4624, B = 16; // set parameters for a tree with 3 levels
    ll nblocks = n / B;

    ll height = floor(log(nblocks) / log(B + 1));
    ll power = binPow(B + 1, height);
    ll z = n - power;
    ll totalNodes = binPow(B + 1, height + 1) / B;
    cout << "Tree total Nodes: " << totalNodes << endl;
    vector<dtype> tree(totalNodes * B + 1);

    vector<dtype> items(n);
    for (int i = 0; i < n; i++)
        items[i] = i * 1.0 + .5;

    buildPerfectTreeVertical(items, tree, 1, 0, totalNodes * B + 1, height, B);

    bool allFound = true;
    vector<int> ans(items.size());
    for (int i = 0; i < items.size(); i++)
    {
        ans[i] = searchSimd(items[i],B,totalNodes, tree, B/8);
    }

    cout << "assert every element existing in the tree is found: ";
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

    vector<dtype> keys = {0, 16.8, n, 5000, 6000};
    cout << "assert boundary cases: ";

    vector<int> ansBoundary(keys.size());
    for (int i = 0; i < keys.size(); i++)
    {
        ansBoundary[i] = searchSimd(keys[i], B, totalNodes, tree, B/8);
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

    cout << "Done testing float!!" << endl;
    return 0;
}

// good notes: https://richardstartin.github.io/posts/finding-bytes
// https://arxiv.org/pdf/1611.07612.pdf
// more details: https://gms.tf/stdfind-and-memchr-optimizations.html
//https://stackoverflow.com/questions/1737087/will-the-comparison-of-two-float-numbers-consume-more-cpu-time-than-two-ints