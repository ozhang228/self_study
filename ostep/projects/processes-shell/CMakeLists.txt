cmake_minimum_required(VERSION 3.20)
project(wish LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_executable(wish
  wish.cpp
)

target_compile_options(wish PRIVATE
  -Wall
  -Wextra
)

# Create a copy of the binary after
add_custom_command(
  TARGET wish
  POST_BUILD
  COMMAND ${CMAKE_COMMAND} -E copy
          $<TARGET_FILE:wish>
          ${CMAKE_SOURCE_DIR}/wish
)
