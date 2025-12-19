#include <gtest/gtest.h>
#include <limits.h>

#include <cstdlib>
#include <string>
#include <vector>

bool try_handle_builtin(const std::vector<std::string>& tokens,
                        std::vector<std::string>& path);

TEST(BuiltIns, ExitSuccess) {
  std::vector<std::string> path{"/bin"};
  std::vector<std::string> tokens{"exit"};

  EXPECT_EXIT(try_handle_builtin(tokens, path),
              ::testing::ExitedWithCode(EXIT_SUCCESS), "");
}

TEST(BuiltIns, ExitWithArgumentsFailure) {
  std::vector<std::string> path{"/bin"};
  std::vector<std::string> tokens{"exit", "ARG"};

  EXPECT_EXIT(try_handle_builtin(tokens, path),
              ::testing::ExitedWithCode(EXIT_FAILURE), "");
}

TEST(BuiltIns, CdSuccessfullyChangesDirectory) {
  char original[PATH_MAX];
  ASSERT_NE(getcwd(original, sizeof(original)), nullptr);

  char tmp[] = "/tmp/wish_test_XXXXXX";
  char* dir = mkdtemp(tmp);
  ASSERT_NE(dir, nullptr);

  std::vector<std::string> path{"/bin"};
  std::vector<std::string> tokens{"cd", dir};

  bool handled = try_handle_builtin(tokens, path);

  EXPECT_TRUE(handled);

  char current[PATH_MAX];
  ASSERT_NE(getcwd(current, sizeof(current)), nullptr);

  EXPECT_STREQ(current, dir);

  ASSERT_EQ(chdir(original), 0);
  rmdir(dir);
}

TEST(BuiltIns, CdFailsWhenInvalidArguments) {
  std::vector<std::string> path{"/bin"};
  {
    std::vector<std::string> tokens{"cd"};

    testing::internal::CaptureStdout();
    bool handled = try_handle_builtin(tokens, path);
    std::string output = testing::internal::GetCapturedStdout();

    EXPECT_TRUE(handled);
    EXPECT_NE(output.find("Error: cd expected 1 argument(s), but got 0"),
              std::string::npos);
  }

  {
    std::vector<std::string> tokens{"cd", "a", "b"};

    testing::internal::CaptureStdout();
    bool handled = try_handle_builtin(tokens, path);
    std::string output = testing::internal::GetCapturedStdout();

    EXPECT_TRUE(handled);
    EXPECT_NE(output.find("Error: cd expected 1 argument(s), but got 2"),
              std::string::npos);
  }
}

TEST(BuiltIns, pathCorrectlySet) {
  std::vector<std::string> path{"/bin"};
  std::vector<std::string> cmd = {"path", "/new"};

  bool handled = try_handle_builtin(cmd, path);

  EXPECT_TRUE(handled);

  EXPECT_EQ(path.size(), 1);
  EXPECT_EQ(path[0], "/new");
}
