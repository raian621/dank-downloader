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

# fetch glad GL bindings
FetchContent_Declare(
  glad
  URL https://github.com/Dav1dde/glad/archive/refs/tags/v2.0.3.zip
)
FetchContent_MakeAvailable(glad)

FetchContent_Declare(
  boost
  URL https://boostorg.jfrog.io/artifactory/main/release/1.81.0/source/boost_1_81_0.zip
)
FetchContent_MakeAvailable(boost)

# fetch Dear ImGui
FetchContent_Declare(
  imgui
  URL https://github.com/ocornut/imgui/archive/refs/tags/v1.89.2.zip
)
FetchContent_MakeAvailable(imgui)
FetchContent_GetProperties(imgui)

add_library(
  imgui
  ${imgui_SOURCE_DIR}/imgui.cpp
  ${imgui_SOURCE_DIR}/imgui_draw.cpp
  ${imgui_SOURCE_DIR}/imgui_widgets.cpp
  ${imgui_SOURCE_DIR}/imgui_tables.cpp
  ${imgui_SOURCE_DIR}/backends/imgui_impl_glfw.cpp
  ${imgui_SOURCE_DIR}/backends/imgui_impl_opengl3.cpp
)

target_include_directories(
  imgui
  PRIVATE
  ${glfw_SOURCE_DIR}/include
)

target_link_libraries(
  imgui PRIVATE
  OpenGL::GL
  glfw
)