---
layout: post
title: "Linear Time Median"
date: 2020-01-05
categories: [Algorithms]
tags: [Algorithms, Python]
---
<p>
Median is considered one of the important measures in Statistics. Unlike Mean, it is not skewed by a few very large values in the dataset. Computing Median can seem like a trivial problem and it is trivial if the dataset (array) is sorted. If it is not sorted, it may not be trivial.</p>
<!--more-->

Median is considered one of the important measures in Statistics. Unlike Mean, it is not skewed by a few very large values in the dataset. Computing Median can seem like a trivial problem and it is trivial if the dataset (array) is sorted. If it is not sorted, it may not be trivial. Sorting an array, as you know, will take _O(nlogn)_ time. But thinking about median computation, we don't need to sort the entire array. We just need to make sure that median elements (middle one if length of array is odd and middle two elements if array length is even) is in their right place.

Putting elements in right place reminds us of [Quick Sort algo](https://www.geeksforgeeks.org/quick-sort/) which was invented by [Tony Hoare](https://en.wikipedia.org/wiki/Tony_Hoare). The algorithm employed to find median in linear time is a variation of _Quick Sort_ called _Quick Select_ which was also developed by [Tony Hoare](https://en.wikipedia.org/wiki/Tony_Hoare).

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

Essentially, partition puts the pivot element in its right place and everything greater after it and everything lesser/equal below it. Complete code which finds median employing the above guts is at [Quick Select Median](https://github.com/vivekgautham/codingchallenges/blob/c380d28cbcd038bd31c885c1f07b95688988e742/challenges/src/algos/arrays.py#L186).

As Andrei Alexandrescu says in one of his [CppCon 2019 talks](https://www.youtube.com/watch?v=FJJTYQYB1JQ), sorting (axiomatically selection) algos are one of the most researched problems in Computer Science. For a programmer, its good to implement or analyse these algos every now and then.

_Keep Calm and Start Coding_














