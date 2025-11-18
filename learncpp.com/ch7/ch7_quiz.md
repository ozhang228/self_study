Fix the following program:

```cpp
#include <iostream>

int main()
{
	std::cout << "Enter a positive number: ";
	int num{};
	std::cin >> num;


	if (num < 0) {
		std::cout << "Negative number entered.  Making positive.\n";
		num = -num;
	}

	std::cout << "You entered: " << num;

	return 0;
}
```

Question #2

Write a file named constants.h that makes the following program run. If your compiler is C++17 capable, use an inline constexpr variable. Otherwise, use a normal constexpr variable. maxClassSize should have value 35.

main.cpp:

```cpp
#include "constants.h"
#include <iostream>

int main()
{
	std::cout << "How many students are in your class? ";
	int students{};
	std::cin >> students;


	if (students > Constants::maxClassSize)
		std::cout << "There are too many students in this class";
	else
		std::cout << "This class isn't too large";

	return 0;
}
```

```cpp
#ifndef LABEL
#define LABEL

namespace Constants {
  inline constexpr maxClassSize{35};
}

#endif
```

Question #3

Write a function int accumulate(int x). This function should return the sum of all of the values of x that have been passed to this function.

The following program should run and produce the output noted in comments:

```cpp
#include <iostream>

int main()
{
    std::cout << accumulate(4) << '\n'; // prints 4
    std::cout << accumulate(3) << '\n'; // prints 7
    std::cout << accumulate(2) << '\n'; // prints 9
    std::cout << accumulate(1) << '\n'; // prints 10

    return 0;
}
```

3b) Extra credit: What are two shortcomings of the accumulate() function above?

- cannot reset the value
- accumulate must be defined at compile time, rather than being able to pass in the starting
