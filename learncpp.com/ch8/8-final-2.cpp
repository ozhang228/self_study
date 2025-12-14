// Make sure that assert triggers even if we compile in release mode
#include <cmath>
#include <vector>
#undef NDEBUG

#include <cassert>  // for assert
#include <iostream>

bool isPrime(int x) {
  if (x < 2) return false;

  std::vector<bool> sieve(x + 1, true);

  for (int i{2}; i * i <= x; ++i) {
    int cur{i + i};

    while (cur <= x) {
      sieve[cur] = false;
      cur += i;
    }
  }

  return sieve[x];
}

int main() {
  assert(!isPrime(0));  // terminate program if isPrime(0) is true
  assert(!isPrime(1));
  assert(isPrime(2));  // terminate program if isPrime(2) is false
  assert(isPrime(3));
  assert(!isPrime(4));
  assert(isPrime(5));
  assert(isPrime(7));
  assert(!isPrime(9));
  assert(isPrime(11));
  assert(isPrime(13));
  assert(!isPrime(15));
  assert(!isPrime(16));
  assert(isPrime(17));
  assert(isPrime(19));
  assert(isPrime(97));
  assert(!isPrime(99));
  assert(isPrime(13417));

  std::cout << "Success!\n";

  return 0;
}
