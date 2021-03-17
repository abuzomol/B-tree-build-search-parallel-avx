
#ifndef SEQ_VERTICAL_H
#define SEQ_VERTICAL_H

#include <vector>
#include "mathHeader.h"

#if isLong
using ll = long long;
#else
using ll = int;
#endif


//function returns the first index i in hPowers that with value doesn't divide (k+1)/ B mod (B+1)^i not zero
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
template <typename T, typename S>
void buildPerfectTreeVertical(std::vector<S> &items, std::vector<T> &tree, ll nodeIndex, ll start, ll end, ll height, ll B)
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
      //std::cout << k+1 << "," <<  i << "," << j << " ";
      tree[hPowers[height - i] + j] = items[k];
    }
  }
}

//method to build a tree in vertical way to speed reduce the IO complexity.
//B is number of items in a node
template <typename T, typename S>
void buildCompleteTreeVertical(std::vector<S> &items, std::vector<T> &tree,
                               ll nodeIndex, ll start, ll end, ll height,
                               ll B, ll x, ll y)
{
  std::vector<ll> hPowers;
  hPowers.reserve(height + 3);
  hPowers.emplace_back(1);

  for (ll i = 1; i < height + 3; i++)
  {
    hPowers.emplace_back((B + 1) * hPowers.back());
  }

  //fill last level (overflow) with x leaves and all their ancestors
  for (ll k = 0; k < x * B; k++)
  {
    tree[hPowers[height + 1] + k] = items[k];

    if ((k + 1) % B == 0)
    {
      ll i = findIf(hPowers, B, k);
      ll j = ((k + 1) / B) / hPowers[i - 1] - ((k + 1) / B) / hPowers[i] - 1;
      //std::cout << k+1 << "," <<  i << "," << j << " ";
      tree[hPowers[height + 1 - i] + j] = items[k];
    }
  }

  ll levelUp = floor(log(y * (B + 1)) / log(B + 1));
  ll endFakeLeaves = ceil(y * (B + 1) * 1.0 / hPowers[levelUp]) * hPowers[levelUp] * B;
  //filling in internal nodes with complete subtrees but not perfect
  ll beginFakeLeaves = B * (x + 1) - 1; // index of max value in the last leaf of node y

  for (ll k = beginFakeLeaves; k < endFakeLeaves; k = k + B)
  {
    //std::cout << "k: " << k << " ";
    ll i = findIf(hPowers, B, k);
    ll j = ((k + 1) / B) / hPowers[i - 1] - ((k + 1) / B) / hPowers[i] - 1;
    tree[hPowers[height + 1 - i] + j] = items[x * B - 1];
  }

  // //make sure that node y at level h is monotone if not full
  // if (x  / (B + 1) < y)
  // {
  //   for (int k = y * (B - 1) + 1; k < y * B; k++)
  //   {
  //     if (tree[hPowers[height] + k] < tree[hPowers[height] + k - 1])
  //     {
  //       tree[hPowers[height] + k] = items[x*B-1];
  //     }
  //   }
  // }

  //fill n - x leaves in level h, and all their ancestors.
  for (ll kk = x * B; kk < items.size(); kk++) //typo notes jan 23 complete tree vertical
  {
    ll k = kk - x * B + y * B; // relative index in level h = height
    tree[hPowers[height] + k] = items[kk];
    if ((k + 1) % B == 0)
    {
      ll i = findIf(hPowers, B, k);
      ll j = ((k + 1) / B) / hPowers[i - 1] - ((k + 1) / B) / hPowers[i] - 1;
      //std::cout << k+1 << "," <<  i << "," << j << " ";
      tree[hPowers[height - i] + j] = items[kk];
    }
  }
}

//B is number of items in a node
template <typename T, typename S>
void buildTreeOptimalVertical(std::vector<S> &items, std::vector<T> &tree,
                              ll nodeIndex, ll start, ll end, ll B)

{
  ll remainder = (end - start + 1) % B;
  // pad with infinities at the end
  if (remainder != 0)
  {
    ll infty = std::numeric_limits<ll>::max();
    for (ll i = 0; i < B - remainder; i++)
    {
      items.emplace_back(S(infty));
    }
    end = items.size() - 1;
  }

  ll N = end - start + 1;
  ll n = N / B;
  ll height = floor(log(n) / log(B + 1));
  ll power = binPow(B + 1, height);
  ll z = n - power;

  if (z == 0)
  {
    tree.reserve(power * (B + 1));
    buildPerfectTreeVertical(items, tree, nodeIndex, start, end, height, B);
  }
  else
  {
    ll x = ceil((B + 1) * z * 1.0 / B);
    ll y = ceil(x * 1.0 / (B + 1));
    tree.reserve(power * (B + 1) + x * B);

    buildCompleteTreeVertical(items, tree, nodeIndex, start, end, height, B, x, y);
  }
}

#endif