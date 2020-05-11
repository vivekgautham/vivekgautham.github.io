---
layout: post
title: "Variadic Templates"
date: 2020-04-18
categories: [C++]
tags: [Templates]
---

One of the remarkable features of Modern C++ is **variadic templates**. Ability of templates to take variable number of was initially designed by __Douglas Gregor__ and __Jaakko Järvi__ and then standardized in Modern C++. This powerful tool has wide variety of cases such as recursive templates, variadic datastructures and catch-all functions. We'll talk about catch-all functions in this post.

Let's create a generic print function that prints any STL containers from below.

- array
- vector
- list
- deque
- set
- map
- multiset
- multimap
- unordered_set
- unordered_map
- unordered_multiset
- unordered_multimap
- stack
- queue
- priority_queue
- tuple


First, lets start with printing a vector/list/deque. The following print function which takes __template <typename, typename> class Container__, __typename Value__ and __typename Allocator__ should work.

```cpp

template <template <typename, typename> class Container, typename Value, typename Allocator>
void print(const Container<Value, Allocator>& container);

template <typename T>
void print(const T& elem)
{
    std::cout << elem;
}

template <template <typename, typename> class Container, typename Value, typename Allocator>
void print(const Container<Value, Allocator>& container)
{
    print("[");
    for (const auto& each: container){
        print(each);
        print(",");
    }
    print("]");
}

```

But, if we try to print map/set/multiset/multimap and its unordered counterparts, it won't work. This is because they take more than 2 arguments in their templates - 3 in the case of sets and 4 in the case or maps. **Variadic templates** to the rescue here. We modify the above code to take variable number of template arguments. We additionally add code to print std::pair, this should suffice printing maps and sets.


```cpp

template <typename T, typename U>
void print(const std::pair<T, U>& p);

template <template <typename, typename...> class Container, typename Value, typename... Args>
void print(const Container<Value, Args...>& container)
{
    print("[");
    for (const auto& each: container){
        print(each);
        print(",");
    }
    print("]");
}

template <typename T, typename U>
void print(const std::pair<T, U>& p) {
    print("(");
    print(p.first);
    print(",");
    print(p.second);
    print(")");
}


```

Now we are left with handling array and tuple. Printing array is should be easy, we add the following and we should be okay.

```cpp

template <typename T, std::size_t SIZE>
void print(const std::array<T, SIZE>& ar);

template <typename T, std::size_t SIZE>
void print(std::array<T, SIZE>& array)
{
    print("[");
    for (const auto& each: array){
        print(each);
        print(",");
    }
    print("]");
}

```

Printing tuple is little tricky. Again, **variadic templates** to the rescue here. With the sophistication C++17 gives us, we use __std::index_sequence/std::index_sequence_for__ to do template parameter pack expansion.

```cpp
template<class Tuple, std::size_t... Is>
void print_tuple_impl(const Tuple& t, std::index_sequence<Is...>)
{
    (print(std::make_pair(std::get<Is>(t), (Is == 0? "" : " "))), ...);
}

template<class... Args>
void print(const std::tuple<Args...>& t)
{
    print_tuple_impl(t, std::index_sequence_for<Args...>{});
}
```

**Variadic templates** could be quite useful in lot of cases. I encourage myself and other Cpp programmers to explore and experiment with this feature.

_Keep Calm and Start Coding_