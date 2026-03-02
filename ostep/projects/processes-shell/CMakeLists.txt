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
