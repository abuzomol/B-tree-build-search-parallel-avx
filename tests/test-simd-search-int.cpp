#include <iostream>
#include <immintrin.h>
#include <vector>
#include <limits>
#include <math.h>

#pragma GCC target("avx2")

using namespace std;

const int INF = numeric_limits<int>::max();

using dtype = int32_t;

using regi = __m256i; //register 256 bit for int

#if isLong
using ll = int64_t;
#else
using ll = int32_t;
#endif

//return base^exponent
ll binPow(ll base, ll exponent)
{
    if (exponent == 0)
        return 1;
    else
    {
        ll ans = binPow(base, exponent / 2);
        ans = ans * ans;
        return exponent % 2 == 0 ? ans : ans * base;
    }
}

//return the binary of an int
void bin(unsigned n)
{
    unsigned i;
    int counter = 0;
    for (i = 1 << 31; i > 0; i = i / 2)
    {
        (n & i) ? printf("1") : printf("0");
        counter++;
        if (counter % 4 == 0)
            printf(" ");
    }
}

//B is number of sorted keys in a node
//return the first index i in hPowers that with value doesn't divide (k+1)/ B mod (B+1)^i not zero
ll findIf(std::vector<ll> &hPowers, ll B, ll k)
{
    ll i = 1; // 1  divides any number
    for (; i < hPowers.size(); i++)
    {
        if (((k + 1) / B) % hPowers[i] == 0)
        {
            continue;
        }
        else
        {
            break;
        }
    }
    return i;
}

//B is number of items in a node
//build perfect tree vertically
//size of items must equal B (B+1)^height
void buildPerfectTreeVertical(vector<dtype> &items, vector<dtype> &tree, ll nodeIndex, ll start, ll end, ll height, ll B)
{
    std::vector<ll> hPowers;
    hPowers.reserve(height + 2);
    hPowers.emplace_back(1);

    for (ll i = 1; i < height + 2; i++)
    {
        hPowers.emplace_back((B + 1) * hPowers[i - 1]);
    }

    for (ll k = 0; k < items.size(); k++)
    {
        tree[hPowers[height] + k] = items[k];
        if ((k + 1) % B == 0)
        {
            ll i = findIf(hPowers, B, k);
            ll j = ((k + 1) / B) / hPowers[i - 1] - ((k + 1) / B) / hPowers[i] - 1;
            tree[hPowers[height - i] + j] = items[k];
        }
    }
}
//get the next node to visit
int go(int k, int i, int B) { return k * (B + 1) + i + 1; }
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
int search(dtype x, int B, int totalNodes, vector<int> &btree, int regBlocks)
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

int main(int argc, char **argv)
{
    const int n = 4624, B = 16; // set parameters for a tree with 3 levels
    ll nblocks = n / B;

    ll height = floor(log(nblocks) / log(B + 1));
    ll power = binPow(B + 1, height);
    ll z = n - power;
    ll totalNodes = binPow(B + 1, height + 1) / B;
    cout << "Tree total Nodes:" << totalNodes << endl;
    vector<dtype> tree(totalNodes * B + 1);

    vector<dtype> items(n);
    for (int i = 0; i < n; i++)
        items[i] = i;

    // SHOW(sizeof(int_fast8_t));
    // SHOW(sizeof(int_fast16_t));
    // SHOW(sizeof(int_fast32_t));
    // SHOW(sizeof(int_fast64_t));

    buildPerfectTreeVertical(items, tree, 1, 0, totalNodes * B + 1, height, B);

    vector<unsigned int> ans(items.size());
    for (int i = 0; i < items.size(); i++)
    {
        ans[i] = search(items[i], B, totalNodes, tree, B / 8);
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
        ansBoundary[i] = search(keys[i], B, totalNodes, tree, B / 8);
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

    cout << "Done testing int!!" << endl;
    return 0;
}

// good notes: https://richardstartin.github.io/posts/finding-bytes
// https://arxiv.org/pdf/1611.07612.pdf
// more details: https://gms.tf/stdfind-and-memchr-optimizations.html