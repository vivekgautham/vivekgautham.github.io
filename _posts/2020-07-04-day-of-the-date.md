---
layout: post
title: "Day of the date"
date: 2020-07-04
categories: [Math, Algorithms, C++]
tags: [Gauss]
---

I like seeing elegant algorithms arise out of prodigious mathematical methods. One such is calculating day of any date in O(1).
Let's take a look at the implementation.

``` cpp
int getDay(std::vector<int> date){
    int m=date[0], d=date[1], y = date[2];
    std::array<int, 12> vy = {11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    y -= m < 3;
    auto r = (y + y/4 - y/100 + y/400 + (int)(float(vy[m-1])*2.6-0.2) + d);
    r %= 7;
    return r;
}
```

The variable _vy_ here represents month index of a year. But, that's weird, why are we assuming January as 11th month and March as 1st month? and why are we subtracting 1 from year if original month provided is less than 3. The reason is interesting which we will get into  towards the end.

First, we get into the meat of the formula where we adjust for the leap year. Explanation behind this part __y/4 - y/100 + y/400__ is fairly simple.

- _Divisible by 4_ --> then Leap Year, add 1 --> _Divisible by 100_, subtract 1 as its non-leap -> unless _Divisible by 400_, add 1 as its leap year.

Before we dig into rest of the formula, lets clarify what our function returns. Our function is goint to be returning integer ranging from 0-6 where 0 denotes Sunday & 6 is Saturday. [Year Y=1](https://www.timeanddate.com/calendar/?year=1&country=22) in Gregorian calendar _(Year Y=0 doesn't exist)_. Given any year, the same date next year will be the next day (_365%7 = 1_), unless the given year/next year is a leap year, in which case it shifts two days or one day depending on whether date falling in January/February or March to December. In order to avoid this complexity, if we consider March to be the start of the year, January & February to be the last two months of previous year, we can always add 1 to the end if its given year/previous year is leap year. As we set the concept of __Virtual Year__ clear, now, all it comes down to is

- subtracting 1 if month is Jan/Feb
- adding 1 if year obtained after previous step is leap

And finally, what is the mystery __vy[m-1])*2.6-0.2__?  This is where we do projections. Our first month (March) in the 1st Virual Year falls on Thursday, The previous year Year 0 which didn't exist is a hypothetical leap year consiting of 366 days. The first day of the first month (March) in the 1st Virual Year is Thursday. By rewinding 366 days back it is Tuesday (2). When we do this for all the first days of all the months in the 1st Virual Year, we get the following sequence.

- {0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4}

So, essentially we get the above sequence of days, which incidentically equals to floor(2.6*{11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10} - 0.2).





