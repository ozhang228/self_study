#include <unistd.h>

#include <cassert>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

// TODO: Write tests
// Interactive mode: empty command, all builtins, whitespace, redirection, path

std::vector<std::string> tokenize_line(const std::string& cmd) {
  std::vector<std::string> tokens{};
  std::stringstream ss(cmd);
  std::string item{};

  while (ss >> item) {
    tokens.push_back(item);
  }

  return tokens;
}

void print_arg_count_err(const std::string& cmd, size_t expected, size_t got) {
  std::cout << "Error: " << cmd << " expected " << expected
            << " argument(s), but got " << got << " argument(s)" << std::endl;
}

bool try_handle_builtin(const std::vector<std::string>& tokens,
                        std::vector<std::string>& path) {
  if (tokens[0] == "exit") {
    if (tokens.size() != 1) {
      print_arg_count_err("exit", 0, tokens.size() - 1);
      std::exit(EXIT_FAILURE);
    } else {
      std::exit(EXIT_SUCCESS);
    }
  } else if (tokens[0] == "cd") {
    if (tokens.size() != 2) {
      print_arg_count_err("cd", 1, tokens.size() - 1);
      return true;
    }

    int rc = chdir(tokens[1].c_str());

    if (rc == -1) {
      std::cout << "Error: failed to change directory to '" << tokens[1] << "'"
                << std::endl;
      return true;
    }
  } else if (tokens[0] == "path") {
    path.assign(tokens.begin() + 1, tokens.end());
  }

  return false;
}

int main(int argc, char* argv[]) {
  std::vector<std::string> path{"/bin"};

  const bool INTERACTIVE_MODE = argc == 1;
  const bool BATCH_MODE = argc == 2;

  if (BATCH_MODE) {
    std::ifstream cmd_file(argv[1]);

    if (!cmd_file.is_open()) {
      std::cout << "Error: File '" << argv[1] << "' failed to open"
                << std::endl;
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
      }
    }
  } else {
    return EXIT_FAILURE;
  }

  return EXIT_SUCCESS;
}
