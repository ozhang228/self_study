#include <cstdlib>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

std::vector<std::string> split(const std::string& cmd, char delim) {
  std::vector<std::string> tokens{};
  std::stringstream ss(cmd);
  std::string item{};

  while (std::getline(ss, item, delim)) {
    tokens.push_back(item);
  }

  return tokens;
}

void printArgumentCountError(size_t expected, size_t got) {
  std::cout << "Error: expected " << expected << " argument(s), but got " << got
            << " argument(s)" << std::endl;
}

int main(int argc, char* argv[]) {
  std::vector<std::string> path{"/bin"};

  if (argc > 2) {
    return EXIT_FAILURE;
  } else if (argc == 2) {
    std::ifstream commandFile(argv[1]);

    if (!commandFile.is_open()) {
      std::cout << "Error: File '" << argv[1] << "' failed to open"
                << std::endl;
      std::exit(EXIT_FAILURE);
    }
  } else {
    std::string line;
    while (true) {
      std::cout << "wish> ";
      std::string line{};

      std::getline(std::cin, line);
      std::vector<std::string> parts{split(line, ' ')};

      if (parts[0] == "exit") {
        if (parts.size() != 1) {
          printArgumentCountError(0, parts.size() - 1);
          std::exit(EXIT_FAILURE);
        } else {
          std::exit(EXIT_SUCCESS);
        }
      } else if (parts[0] == "cd") {
        if (parts.size() != 2) {
          printArgumentCountError(1, parts.size() - 1);
          std::exit(EXIT_FAILURE);
          // ENDED HERE DOING BUILTINs
        }
      }
    }
  }

  return EXIT_SUCCESS;
}
