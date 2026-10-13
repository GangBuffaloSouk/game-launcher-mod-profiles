cmake_minimum_required(VERSION 3.20)
project(glmp_injector CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(glmp_injector main.cpp injector.cpp)
target_include_directories(glmp_injector PRIVATE .)

if (WIN32)
  target_link_libraries(glmp_injector PRIVATE kernel32 user32)
endif()