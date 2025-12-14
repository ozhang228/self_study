#include <iostream>
#include <ostream>

int calculate(int a, int b, char op) {
  switch (op) {
  case '+':
    return a + b;
  case '-':
    return a - b;
  case '*':
    return a * b;
  case '/':
    return a / b;
  case '%':
    return a % b;
  default:
    std::cout << "Invalid operator" << std::endl;
    return 0;
  }
}
