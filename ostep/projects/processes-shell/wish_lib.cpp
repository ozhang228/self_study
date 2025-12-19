
#include <sys/wait.h>
#include <unistd.h>

#include <iostream>
#include <sstream>
#include <string>
#include <vector>

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
    }

    return true;
  } else if (tokens[0] == "path") {
    path.assign(tokens.begin() + 1, tokens.end());
    return true;
  }

  return false;
}

void execute_command(const std::vector<std::string>& tokens,
                     const std::vector<std::string>& path) {
  std::string cmd_path{};

  for (const auto& p : path) {
    std::string full_path = p + "/" + tokens[0];
    if (access(full_path.c_str(), X_OK) == 0) {
      cmd_path = full_path;
      break;
    }
  }

  if (cmd_path.empty()) {
    std::cout << "Error: could not find the command in path" << std::endl;
    return;
  }

  int rc = fork();

  bool is_child = rc == 0;
  bool had_error = rc == -1;

  if (had_error) {
    std::cout << "Error: fork failed" << std::endl;
    return;
  } else if (is_child) {
    std::vector<char*> argv;
    argv.reserve(tokens.size());

    argv.push_back(const_cast<char*>(cmd_path.c_str()));

    for (size_t i{1}; i < tokens.size(); ++i) {
      argv.push_back(const_cast<char*>(tokens[i].c_str()));
    }

    argv.push_back(nullptr);
    execv(cmd_path.c_str(), argv.data());
  } else {
    waitpid(rc, NULL, 0);
  }
}
