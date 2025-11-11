#include <iostream>
// getQuantityPhrase() should take a single int parameter representing the
// quantity of something and return the following descriptor:
//
// < 0 = “negative”
// 0 = “no”
// 1 = “a single”
// 2 = “a couple of”
// 3 = “a few”
// > 3 = “many”

std::string_view getQuantityPhrase(int qty) {
  if (qty < 0)
    return "negative";
  else if (qty == 0)
    return "no";
  else if (qty == 1)
    return "a single";
  else if (qty == 2)
    return "a couple of";
  else if (qty == 3)
    return "a few";
  else
    return "many";
}

// getApplesPluralized() should take a single int parameter parameter
// representing the quantity of apples and return the following:
//
// 1 = “apple”
// otherwise = “apples”
// This function should use the conditional operator.

std::string_view getApplesPluralized(int qty) {
  return qty == 1 ? "apple" : "apples";
}

int main() {
  constexpr int maryApples{3};
  std::cout << "Mary has " << getQuantityPhrase(maryApples) << ' '
            << getApplesPluralized(maryApples) << ".\n";

  std::cout << "How many apples do you have? ";
  int numApples{};
  std::cin >> numApples;

  std::cout << "You have " << getQuantityPhrase(numApples) << ' '
            << getApplesPluralized(numApples) << ".\n";

  return 0;
}
