cmake_minimum_required(VERSION 3.25)

project("dankdownloader")
set(CMAKE_CXX_STANDARD 20)
add_executable(${PROJECT_NAME})

add_subdirectory(src)
include(CMake/modules/dependencies.cmake)

add_executable(
  hello_test
  tests/hello_test.cpp
)

target_link_libraries(
  ${PROJECT_NAME} PRIVATE
  OpenGL::GL
  glfw
  imgui
)

include_directories(
  include
  ${imgui_SOURCE_DIR}
  ${imgui_SOURCE_DIR}/backends
)

enable_testing()

target_link_libraries(
  hello_test
  GTest::gtest_main
)

include(GoogleTest)
gtest_discover_tests(hello_test)
