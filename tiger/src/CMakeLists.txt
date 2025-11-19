cmake_minimum_required(VERSION 3.20)
project(tiger C)

set(CMAKE_C_STANDARD 23)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)

file(GLOB_RECURSE SOURCES *.c)
add_executable(my_program ${SOURCES})

target_include_directories(my_program PRIVATE . chap1)

    target_compile_options(my_program PRIVATE 
        -Wall
        -Wextra
        -Wpedantic
    )