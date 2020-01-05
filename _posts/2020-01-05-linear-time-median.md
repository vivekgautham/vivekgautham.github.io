---
layout: post
title: "Linear Time Median"
date: 2020-01-05
---

Median is considered one of the important measure in Statistics. Unlike Mean, it is not skewed by a few very large values in the dataset. Computing Median can seem like a trivial problem. And it is trivial if the dataset(array) is sorted. If it is not sorted, it may not be trivial. Sorting an array, as you know, will take _O(nlogn)_ time. But thinking about median computation, we don't need to sort the entire array. We just need to make sure that median elements (middle one if length of array is odd and middle two elements if array length is even) is in their right place.

This reminds us of [Quick Sort algo](https://www.geeksforgeeks.org/quick-sort/) which was invented by [Tony Hoare](https://en.wikipedia.org/wiki/Tony_Hoare). The algorithm employed to find median in linear time is called _Quick Select_ which was also developed by [Tony Hoare](https://en.wikipedia.org/wiki/Tony_Hoare).

The guts of the algorithm is as follows.

```python

def partition(arr, lowIdx, highIdx, pivotIdx):
    pivot = arr[pivotIdx]
    arr[highIdx], arr[pivotIdx] = arr[pivotIdx], arr[highIdx]
    i = lowIdx-1
    for j in range(lowIdx, highIdx):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i+1], arr[highIdx] = arr[highIdx], arr[i+1]
    return arr
```

Essentially, partition puts the pivot element in its right place and everything greater after it and everything lesser/equal below it. Complete code is at [Quick Select](https://github.com/vivekgautham/codingchallenges/blob/c380d28cbcd038bd31c885c1f07b95688988e742/challenges/src/algos/arrays.py#L186).

As Andrei Alexandrescu says in one of his [CppCon 2019 talks](https://github.com/CppCon/CppCon2019/blob/master/Presentations/speed_is_found_in_the_minds_of_people/speed_is_found_in_the_minds_of_people__andrei_alexandrescu__cppcon_2019.pdf), sorting (axiomatically selection) algos are one of the most researched problem in Computer Science. For a programmer, its good to implement/analyse these algos every now and then.

_Keep Calm and Start Coding_














