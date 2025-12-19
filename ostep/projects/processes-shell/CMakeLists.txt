cmake_minimum_required(VERSION 4.1.1)
project(wish LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(DOWNLOAD_EXTRACT_TIMESTAMP, true)

add_library(wish_lib
  wish_lib.cpp
)

target_compile_options(wish_lib PRIVATE -Wall -Wextra)

add_executable(wish
  wish.cpp
)

target_link_libraries(wish PRIVATE wish_lib)

# Create a copy of the binary after
add_custom_command(
  TARGET wish
  POST_BUILD
  COMMAND ${CMAKE_COMMAND} -E copy
          $<TARGET_FILE:wish>
          ${CMAKE_SOURCE_DIR}/wish
)

# Googletest
include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/03597a01ee50ed33e9dfd640b249b4be3799d395.zip
)
# For Windows: Prevent overriding the parent project's compiler/linker settings
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

enable_testing()

add_executable(wish_test
  wish_test.cpp
)

target_link_libraries(wish_test
  PRIVATE
    wish_lib
    GTest::gtest_main
)

include(GoogleTest)
gtest_discover_tests(wish_test)
