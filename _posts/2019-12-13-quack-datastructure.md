---
layout: post
title: "Quack - A Queue and a Stack in one"
date: 2019-12-13
---

Quack is an unique data structure that combines the properties of both Stack and a Queue. The structure can be viewed as a list of items written from left to right. It lets you perform following three operations on the structure.

    1. **push** - add an element on to the left side of the structure
    2. **pop**  - remove an element from the left end of the structure
    3. **pull** - remove an element from the right end of the structure

The great thing about this data structure is that these operations can be elegantly implemented using three stacks, performing at amortized O(1)time. Here we are going to look at the technique of this implementation.