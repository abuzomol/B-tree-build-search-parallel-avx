Running experiments will generate csv files that will be stored here. All csv files contain the following header:
```
N,node size,build horizontal(s),build vertical(s),seq search(s),binary search(s), simd search(s)
```
To run the experiments, you can run the following command:

```
make run_serial
make run_parallel
```
