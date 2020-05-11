---
layout: post
title: "C++ Smart Pointers - What they do and How they work?"
date: 2019-12-18
categories: [C++]
tags: [C++, Smartpointers]
---

I recently had a chance to watch an interesting CppCon lecture by Arthur O'Dwyer titled __Back__ __To__ __Basics:__ __Smart__ __Pointers__. Atleast for me, the talk was a pretty good review/refresher of what Smart Pointers are capable of and how they operate. In the talk, Arthur
summarized all the smart pointers in a neat, succinct way. I thought writing the below article would be a good way to cement my understanding of smart pointers.

**As you all may know, following are the Smart Pointers available in C++ today**

- *std::unique_ptr*  - use it for "Exclusive-Ownership Resource Management" (Scott Meyers' EMC++ Item 18)
- *std::shared_ptr*  - use it for "Shared-Ownership Resource Management" (Scott Meyers' EMC++ Item 19)
- *std::weak_ptr*    - use it for "std::shared_ptr like pointers that can dangle" (Scott Meyers' EMC++ Item 20)

**std::unique_ptr**

One of the elegant things about *std::unique_ptr* is how *"Transfer of Ownership"* is made seamless.

- *std::unique_ptr* is non copyable but only movable; Moving a std::unique_ptr transfers ownership to destination leaving source in an undefined state.

Another elegant thing is its ability to accept custom deleters.

- Not all resources are same. There are resources which need to be treated in a special way when its deleted or released.

For example, your code may look like the below code using C Style I/O. Here we could utilize the unique to manage exclusive ownership of the file pointer. Custom Deleter comes in handy here to perform file closing automatically, once we are done reading or writing from the file pointer we got from unique_ptr.

```cpp

//ModernC++/item18.h file

struct FileCloser {
    void operator()(std::FILE* fp){
        assert (fp != nullptr);
        std::fclose(fp);
        std::cout << "File Closed using custom File Closer" << std::endl;
    }
};

std::unique_ptr<std::FILE, FileCloser> make_unique_file_ptr(std::string fileName, std::string fileMode){
    std::cout << "Creating Unique File Ptr" << std::endl << fileName << std::endl;
    return std::unique_ptr<std::FILE, FileCloser>(std::fopen(fileName.c_str(), fileMode.c_str()));
}

//main.cpp file

#include "ModernC++/item18.h"

int main()
{
    auto fptr = make_unique_file_ptr(std::string("./Files/demo.txt"), std::string("r"));
    if(fptr){
        char c;
        while ( (c = std::fgetc(fptr.get())) != EOF )
        {
            std::cout << c;
        }
        std::cout << std::endl;
    }
}
```
*std::unique_ptr* also comes with an added advantage of efficiently converting to a *std::shared_ptr*.

**std::shared_ptr**

The design of the *std::shared_ptr* is fascinating. Unlike *std::unique_ptr*, *std::shared_ptr* doesn't take ownership of controlled object. It essentially participates in reference counted or otherwise shared ownership of control block (i.e. only one heap allocated control block) which in turn is responsible of managing the controlled object.

When you copy a *std::shared_ptr*, ownership of control block is shared.

Like *std::unique_ptr*, *std::shared_ptr* also can be provided a custom deleter.

**Factory Functions**

Always use *std::make_unique*, *std::make_shared* to create *std::unique_ptr* and *std::shared_ptr*. There are few reasons behind this. The main reason is, it just looks cleaner. We have avoided the usage of *delete*. So, Why keep using *new* in our code, when it has been abstracted away for us. Also, there are allocation efficiencies when using *std::make_shared*.

**std::weak_ptr**

Among plenty of misnomers in C++, *std::weak_ptr* is one. The ideal name I could think of is *std::aspiring_shared_ptr*. I am using this name
because *std::weak_ptr* is essentially a ticket to receive a *std::shared_ptr* of the object sometime in the future, provided that
object still exists.

Lot of people actually wonder - why on earth would we need *std::weak_ptr*? There is actually a valid use case especially when we are working on a large scale software. For instance, say we have a factory function that creates relatively expensive object. As object creation is expensive, we are caching or pooling *std::shared_ptr* that we have returned to clients. But, in this case, we make the cached pointer *std::weak_ptr* as they can tell us about the object's lifetime - meaning, when the clients of this factory function is done using the object, the cached pointer will dangle. But, when the object still has life, we will be able to acquire or receive a *std::shared_ptr* of the object from the *std::weak_ptr* we hold.



