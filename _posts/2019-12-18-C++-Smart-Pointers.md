---
layout: post
title: "C++ Smart Pointers - What do they do and How they work?"
date: 2019-12-18
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

Another elegant thing is its ability to accept custom deleters. Not all resources are same. There are resources which need to treated in a special way when its deleted. For example, your code may look like the below code using C Style I/O.

Here we could utilize the unique to manage exclusive ownership of the file pointer. Custom Deleter comes in handy here to perform file closing
automatically, once we are done reading or writing from the file pointer we got from unique_ptr.

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


**std::shared_ptr**


**std::weak_ptr**

Among plenty of misnomers in C++, *std::weak_ptr* is one. The ideal name I could think of is *std::aspiring_shared_ptr*. The rationale
behind this naming is *std::weak_ptr* is essentially a ticket to receive a *std::shared_ptr* of the object sometime in the future, assuming that
object still exists.

