---
layout: post
title: "Cartesian Matching Algorithm"
date: 2020-10-28
categories: [Math, Algorithms, C++]
tags: [Matching]
---

Every now and then I encounter algorithms that is both intuitive as well as far-reaching. The algorithm to be described in this post is called Cartesian Matching Algorithm. Bear with me here, as this is not the official name of the matching algorithm. I encountered this as a daily challenge in CodeSignal. As Cartesian axis is pivotal to intuitiveness of this algorithm, I named it that way. How it works is you simply map the given input data of numeric values on to a catesian x-axis, assuming its an array of numbers. After this step, grow a circle starting at unit radius. In every step/iteration, if there are intersections between two circles, you take those out and match them together.


The above discussed logic can be picturized like this. For the input [200, 100, 70, 130, 100, 800, 810], Initially we match [1, 4] as their circle conicides immediately as soon as inputs are mapped on to x-axis. After this, we keep growing the remaining circle. The circle at 800 and 810 as centers touches after 5 steps.

![Cartesian Matching Algorithm](https://i.ibb.co/JBy2Lkr/aww-board.png)

So, we take those two out and add [5, 6] to our list of matches. Algorithm proceeds like this until we are left with one or zero input data.

Here is the Cpp code that implements the algo.

```cpp

    std::vector< std::vector<int> > res;
    std::unordered_set<int> processed;

    while (true) {
        std::vector<std::pair<int, int> > xpi;
        for (auto i=0; i<xp.size(); i++){
            if (processed.find(i) == processed.end()){
                xpi.push_back(std::make_pair(xp[i], i));
            }
        }
        std::vector<int> diff(xpi.size(), 0);
        std::sort(
            xpi.begin(),
            xpi.end(),
            [] (const auto a, const auto b){
                if (a.first < b.first)
                    return true;
                if (a.first == b.first) {
                    return a.second < b.second;
                }
                return false;
            }
        );
        std::vector<int> sortedXp;
        std::vector<int> xpIdx;
        for (auto v: xpi){
            sortedXp.push_back(v.first);
            xpIdx.push_back(v.second);
        }
        if (xpIdx.size() >= 2) {
            std::adjacent_difference(sortedXp.begin(), sortedXp.end(), diff.begin());
            auto minEl = std::min_element(diff.begin()+1, diff.end());
            auto minDiffIdx = std::distance(diff.begin(), minEl);
            processed.insert(xpIdx[minDiffIdx-1]);
            processed.insert(xpIdx[minDiffIdx]);
            if (xpIdx[minDiffIdx-1] < xpIdx[minDiffIdx]){
                res.push_back(
                    {xpIdx[minDiffIdx-1], xpIdx[minDiffIdx]}
                );
            }
            else{
                res.push_back(
                    {xpIdx[minDiffIdx], xpIdx[minDiffIdx-1]}
                );
            }

        }
        else {
            break;
        }
    }

```