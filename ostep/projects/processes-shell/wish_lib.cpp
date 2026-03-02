
#include <sys/wait.h>
#include <unistd.h>

#include <cstdlib>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

void print_error() { std::cerr << "An error had occurred" << std::endl; }
std::vector<std::string> tokenize_line(const std::string& cmd) {
  std::vector<std::string> tokens{};
  std::stringstream ss(cmd);
  std::string item{};

  while (ss >> item) {
    size_t gt_pos{item.find(">")};
    if (gt_pos == item.npos) {
      tokens.push_back(item);
      continue;
    }

    if (gt_pos == 0) {
      tokens.push_back(">");
      tokens.push_back(item.substr(1));
    } else if (gt_pos == item.size() - 1) {
      tokens.push_back(item.substr(0, item.size() - 1));
      tokens.push_back(">");
    } else {
      print_error();
      std::exit(EXIT_FAILURE);
    }
  }

  return tokens;
}

[[nodiscard]] bool try_handle_builtin(const std::vector<std::string>& tokens,
                                      std::vector<std::string>& path) {
  if (tokens.empty()) return true;

  if (tokens[0] == "exit") {
    if (tokens.size() != 1) {
      print_error();
      std::exit(EXIT_FAILURE);
    } else {
      std::exit(EXIT_SUCCESS);
    }
  } else if (tokens[0] == "cd") {
    if (tokens.size() != 2) {
      print_error();
      return true;
    }

    int rc = chdir(tokens[1].c_str());

    if (rc == -1) {
      print_error();
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
    print_error();
    return;
  }

  int rc = fork();

  bool is_child = rc == 0;
  bool had_error = rc == -1;

  if (had_error) {
    print_error();
    return;
  } else if (is_child) {
    std::vector<char*> argv;
    argv.reserve(tokens.size());

    argv.push_back(const_cast<char*>(cmd_path.c_str()));

    for (size_t i = 1; i < tokens.size(); ++i) {
      argv.push_back(const_cast<char*>(tokens[i].c_str()));
    }

    argv.push_back(nullptr);

    execv(cmd_path.c_str(), argv.data());
    print_error();
    std::exit(EXIT_FAILURE);
  } else {
    waitpid(rc, NULL, 0);
  }
}
