---
layout: post
title: "Quack - A Queue and a Stack in one"
date: 2019-12-13
---

Quack is an unique data structure that combines the properties of both Stack and a Queue. The structure can be viewed as a list of items written from left to right. 

It lets you perform following three operations on the structure.
        1. *push* - add an element on to the left side of the structure
        2. *pop*  - remove an element from the left end of the structure
        3. *pull* - remove an element from the right end of the structure

The great thing about this data structure is that these operations can be elegantly implemented using three stacks, performing at amortized O(1)time. Here we are going to look at the technique of this implementation in Python.

Let's declare a class for Quack in Python. The key thing to note here is *total* variable. This will let us keep track of elements in the structure. 

```python
@dataclass
class Quack(object):

    arr1 : list
    arr2 : list
    arr3 : list
    total: int = 0
```

When we do push operation, we append to both *arr1* and *arr2*. Then, increment the *total* by 1.

```python
    def push(self, elem):
        self.arr1.append(elem)
        self.arr2.append(elem)
        self.total += 1
```

When we do pop operation, we first check if *total* is 0. If so, we clear both *arr1* and *arr3* and raise Exception.
Otherwise, move on to pop an element from *arr2* if non empty; decrement the *total* and return poped element from *arr1*

```python
    def pop(self):
        if self.total == 0:
            del self.arr1[:]
            del self.arr3[:]
            raise Exception("Nothing to pop")
        
        if self.arr2:
            self.arr2.pop()
        self.total -= 1
        return self.arr1.pop()
```
