#include <cstdlib>
#include <iostream>

void printAscii() {
  for (char cur = 'a'; cur <= 'z'; ++cur) {
    std::cout << cur << " " << static_cast<int>(cur) << std::endl;
  }
}

void printInverted() {
  for (int i = 5; i > 0; --i) {
    for (int j = i; j > 0; --j) {
      std::cout << j << " ";
    }

    std::cout << std::endl;
  }
}

void printDoubleInverted() {
  for (int i = 5; i > 0; --i) {
    for (int j = 0; j < i; ++j) {
      std::cout << "  ";
    }

    for (int j = 6 - i; j > 0; --j) {
      std::cout << j << " ";
    }

    std::cout << std::endl;
  }
}

int main() {
  // printAscii();
  // printInverted();
  printDoubleInverted();
  return EXIT_SUCCESS;
}
