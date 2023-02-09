cmake_minimum_required(VERSION 3.25)

project("dankdownloader")

add_executable("${PROJECT_NAME}.exe")

include_directories(include)
add_subdirectory(src)