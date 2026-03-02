#include <unistd.h>

#include <cassert>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

std::vector<std::string> tokenize_line(const std::string& cmd);
void print_error();
bool try_handle_builtin(const std::vector<std::string>& tokens,
                        std::vector<std::string>& path);
void execute_command(const std::vector<std::string>& tokens,
                     const std::vector<std::string>& path);

int main(int argc, char* argv[]) {
  std::vector<std::string> path{"/bin"};

  const bool INTERACTIVE_MODE = argc == 1;
  const bool BATCH_MODE = argc == 2;

  if (BATCH_MODE) {
    std::ifstream cmd_file(argv[1]);

    if (!cmd_file.is_open()) {
      print_error();
      std::exit(EXIT_FAILURE);
    }

    std::cerr << "Error: batch mode not implemented\n";
    return EXIT_FAILURE;
  } else if (INTERACTIVE_MODE) {
    while (true) {
      std::cout << "wish> ";
      std::string line;

      if (!std::getline(std::cin, line)) {
        break;
      }

      std::vector<std::string> parts{tokenize_line(line)};

      if (parts.empty()) {
        continue;
      }

      if (try_handle_builtin(parts, path)) {
        continue;
      } else {
        execute_command(parts, path);
      }
    }
  } else {
    print_error();
    std::exit(EXIT_FAILURE);
  }

  std::exit(EXIT_SUCCESS);
}
