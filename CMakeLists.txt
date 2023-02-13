cmake_minimum_required(VERSION 3.25)

project("dankdownloader")
set(CMAKE_CXX_STANDARD 20)
add_executable(${PROJECT_NAME}.exe)

find_package(OpenGL REQUIRED)

include(FetchContent)

# fetch google tests library
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/refs/tags/v1.13.0.zip
)

set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

# fetch GLFW library
FetchContent_Declare(
  glfw
  URL https://github.com/glfw/glfw/releases/download/3.3.8/glfw-3.3.8.zip
)
FetchContent_MakeAvailable(glfw)
FetchContent_GetProperties(glfw)

# fetch glad GL bindings
FetchContent_Declare(
  glad
  URL https://github.com/Dav1dde/glad/archive/refs/tags/v2.0.3.zip
)
FetchContent_MakeAvailable(glad)
FetchContent_GetProperties(glad)

target_link_libraries(
  ${PROJECT_NAME}.exe
  glfw
  OpenGL::GL
)

include_directories(include)
add_subdirectory(src)

enable_testing()

add_executable(
  hello_test
  tests/hello_test.cpp
)

target_link_libraries(
  hello_test
  GTest::gtest_main
)

include(GoogleTest)
gtest_discover_tests(hello_test)
