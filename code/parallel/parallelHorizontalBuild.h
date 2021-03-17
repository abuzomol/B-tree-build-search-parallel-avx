#ifndef PARALLEL_HOR_H
#define PARALLEL_HOR_H

#include <vector>
#include "mathHeader.h"
#if isLong
using ll = long long;
#else
using ll = int;
#endif


#ifndef processors
#define processors 8;
#endif

//B is number of items in a node
//build perfect tree vertically
//size of items must equal B (B+1)^height
template <typename T, typename S>
void buildPerfectTreeHorizontal(std::vector<S> &items, std::vector<T> &tree,
                                ll nodeIndex, ll start, ll end, ll height,
                                ll B)
{
    ll powerH = binPow(B, height);
    ll powerI = powerH;
    ll powerHMinusI = 1;
    // copy items first to last level
    #pragma omp parallel for num_threads(processors)
    for (ll j = 0; j < powerH * (B - 1); j++)
    {
        tree[powerH + j] = T(items[j]);
    }
    //copy internal nodes
    for (ll i = height - 1; i >= 0; i--)
    {
        powerI /= B;
        powerHMinusI *= B;
        #pragma omp parallel for num_threads(processors)
        for (ll j = 0; j < powerI; j++)
        {
            ll alpha = j * powerHMinusI;
            for (ll k = 0; k < B - 1; k++)
            {
                ll beta = (k + 1) * powerHMinusI / B;
                tree[powerI + j * (B - 1) + k] =
                    tree[powerH + (alpha + beta) * (B - 1) - 1];
            }
        }
    }
}

//B is number of items in a node
//build complete tree horizontally
//size of items must be between  B*(B+1)^height and B*(B+1)^{height + 1}
template <typename T, typename S>
void fillCompleteTreeHorizontal(std::vector<S> &items, std::vector<T> &tree,
                                ll height, ll treeSize, ll B, ll x,
                                ll y)
{
    ll powerHPlusOne = binPow(B, height + 1);
    ll powerI = powerHPlusOne / B; // powerI = B^i
    ll end = items.size() - 1;
    // fill in last level with overflow
    #pragma omp parallel for num_threads(processors)
    for (ll j = 0; j < x * (B - 1); j++)
    {
        tree[powerHPlusOne + j] = T(items[j]);
    }

    // get medians from last level and fill in the y nodes in level h
    #pragma omp parallel for num_threads(processors)
    for (ll j = 0; j < y - 1; j++)
    {
        ll alpha = j * B;
        // go through every item in node j
        for (ll k = 0; k < B - 1; k++)
        {
            ll beta = (k + 1);
            ll medianIndex = powerHPlusOne + (alpha + beta) * (B - 1) - 1;
            tree[powerI + j * (B - 1) + k] = tree[medianIndex];
        }
    }

    // fill in last node y
    ll alpha = (y - 1) * B;
    for (ll k = 0; k < B - 1; k++)
    {
        ll beta = (k + 1);
        ll medianIndex;
        if (alpha + beta <= x)
        {
            medianIndex = powerHPlusOne + (alpha + beta) * (B - 1) - 1;
        }
        else
        {
            ll medianIndex = powerHPlusOne + x * (B - 1) - 1;
        }
        tree[powerI + (y - 1) * (B - 1) + k] = tree[medianIndex];
    }

    // copy rest of elements to level h
    for (ll j = 0; j < end - x * (B - 1) + 1; j++)
    {
        tree[powerI + y * (B - 1) + j] = T(items[j + x * (B - 1)]);
    }

    //fill in level h-1 to level 0
    ll powerHMinusI = 1; // powerHMinusI = B^{h - i}

    ll levelUp = floor(log(y * (B)) / log(B));
    ll hPowersLevelUp = binPow(B, levelUp);
    ll endFakeLeaves = (y + 1) * B;
    // ll endFakeLeaves = std::min((ll)ceil(y * B * 1.0 / hPowersLevelUp) * hPowersLevelUp, (y + 1) * B);
    for (ll i = height - 1; i >= 0; i--)
    {
        powerI /= B;
        powerHMinusI *= B;
        // go through every node j in level i
        #pragma omp parallel for num_threads(processors)
        for (ll j = 0; j < powerI; j++)
        {
            ll alpha = j * powerHMinusI * B;
            // go through every item in node j at level i
            for (ll k = 0; k < B - 1; k++)
            {
                ll beta = (k + 1) * powerHMinusI;
                // case medianIndex at the last level
                if (alpha + beta <= x)
                {
                    ll medianIndex = powerHPlusOne + (alpha + beta) * (B - 1) - 1;
                    tree[powerI + j * (B - 1) + k] = tree[medianIndex];
                }
                else
                {

                    // if (x > alpha && (x - alpha > (k + 1) * powerHMinusI / B) &&
                    //     (x - alpha < (k + 2) * powerHMinusI / B))
                    // {
                    //   ll medianIndex = powerHPlusOne + x * (B - 1) - 1;
                    //   tree[powerI + j * (B - 1) + k] = tree[medianIndex];
                    // }
                    // case medianIndex at the last level for last node y
                    if (x > alpha && alpha + beta < endFakeLeaves)
                    {
                        ll medianIndex = powerHPlusOne + x * (B - 1) - 1;
                        tree[powerI + j * (B - 1) + k] = tree[medianIndex];
                    }
                    // case medianIndex in the level before last
                    else
                    {
                        ll alphaa = alpha / B;
                        beta /= B;
                        ll medianIndex =
                            powerHPlusOne / B + (alphaa + beta) * (B - 1) - 1;
                        tree[powerI + j * (B - 1) + k] = tree[medianIndex];
                    }
                }
            }
        }
        //  }
    }
}

//B is number of items in a node
//build a tree horizontally
//size of items must be between  B*(B+1)^height and B*(B+1)^{height + 1}
template <typename T, typename S>
void buildTreeOptimalHorizontal(std::vector<S> &items, std::vector<T> &tree,
                                ll nodeIndex, ll start, ll end, ll B)
{
    ll remainder = (end - start + 1) % (B - 1);
    // pad with infinities at the end
    if (remainder != 0)
    {
        ll infty = std::numeric_limits<ll>::max();
        for (ll i = 0; i < (B - 1) - remainder; i++)
        {
            items.emplace_back(S(infty));
        }
        end = items.size() - 1;
    }

    ll N = end - start + 1;
    ll n = N / (B - 1);
    ll height = floor(log(n) / log(B));
    ll power = binPow(B, height);
    ll z = n - power;

    if (z == 0)
    {
        tree.reserve(power * B);
        buildPerfectTreeHorizontal(items, tree, nodeIndex, start, end, height, B);
    }
    else
    {
        ll x = ceil(B * z * 1.0 / (B - 1));
        ll y = ceil(x * 1.0 / B);
        tree.reserve(power * B + x * (B - 1));

        fillCompleteTreeHorizontal(items, tree, height, tree.capacity() - 1, B, x, y);
    }
}
#endif
