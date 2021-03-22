#include "mathHeader.h"

//return base^exponenet
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

//get the next node to visit
int go(int k, int i, int B) { return k * (B + 1) + i + 1; }
