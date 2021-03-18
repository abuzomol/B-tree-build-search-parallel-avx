cd code/parallel/ ; pwd
HASAVX2=$(gcc -mavx2 -dM -E - < /dev/null | egrep "AVX2" | sort)
if [ -z "$HASAVX2" ]; 
then 
  echo "ERROR: This device doesn't have AVX2"; exit;
else
  echo -e "This device has AVX2"
  echo -e "Compiling sequential files:"
  echo "compiling for type int"
  #check CPUs
  CPUs=$(nproc)
  echo -e "Found $CPUs CPUs in this device"
  for (( p=1; p<=$CPUs; p = p *2 ))
  do  
    g++ -std=c++17 -Ddtype=int -mavx2 -Dprocessors=$p -O3 mathHeader.cpp parallel-build-search.cpp -o parallelBuildSearchInt$p
    echo "compiling for type long"
    g++ -std=c++17 -Ddtype=long -mavx2 -Dprocessors=$p -O3 mathHeader.cpp parallel-build-search.cpp -o parallelBuildSearchLong$p
    echo "compiling for type float"
    g++ -std=c++17 -Ddtype=float -mavx2 -Dprocessors=$p -O3 mathHeader.cpp parallel-build-search.cpp -o parallelBuildSearchFloat$p
    echo "compiling for type double"
    g++ -std=c++17 -Ddtype=double -mavx2 -Dprocessors=$p -O3 mathHeader.cpp parallel-build-search.cpp -o parallelBuildSearchDouble$p
  done
  echo "Done compiling!"
  echo "Running python script: it will take many hours!"
  cd ../../
  # python3 parallel-build-script.py -p $CPUs
fi