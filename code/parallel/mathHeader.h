
#ifndef MATH_HEADER_H
#define MATH_HEADER_H

#include <math.h>

#if isLong
using ll = long long;
#else
using ll = int;
#endif

//return base^exponenet
ll binPow(ll base, ll exponent);
//get the next node to visit
int go(int k, int i, int B);

#endif

