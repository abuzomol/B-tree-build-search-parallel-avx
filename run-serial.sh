#!/bin/bash
DIR="$(pwd)"
SRC="$DIR/src/serial/" #location of source files
cd $SRC
HASAVX2=$(gcc -mavx2 -dM -E - < /dev/null | egrep "AVX2" | sort)
if [ -z "$HASAVX2" ]; 
then 
  echo "ERROR: This device doesn't have AVX2"; exit;
else
  echo "This device has AVX2"
  echo "Compiling sequential files:"
  echo "compiling for type int"
  g++ -std=c++17 -mavx2 -O3 mathHeader.cpp seq-build-search.cpp -o seqBuildSearchInt
  echo "compiling for type long"
  g++ -std=c++17 -Ddtype=long -mavx2 -O3 mathHeader.cpp seq-build-search.cpp -o seqBuildSearchLong
  echo "compiling for type float"
  g++ -std=c++17 -Ddtype=float -mavx2 -O3 mathHeader.cpp seq-build-search.cpp -o seqBuildSearchFloat
  echo "compiling for type double"
  g++ -std=c++17 -Ddtype=double -mavx2 -O3 mathHeader.cpp seq-build-search.cpp -o seqBuildSearchDouble
  echo "Done compiling!"
  echo "Running python script: it will take 1 hour to 2 hours!"
  cd $DIR
  python3 seq-build-script.py
fi
