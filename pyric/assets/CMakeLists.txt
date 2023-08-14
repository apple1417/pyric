cmake_minimum_required(VERSION 3.24)

project(pyric)

add_library(pyric MODULE)

target_compile_features(pyric PUBLIC cxx_std_20)
set_target_properties(pyric PROPERTIES
    COMPILE_WARNING_AS_ERROR True
    INTERPROCEDURAL_OPTIMIZATION True
    EXPORT_COMPILE_COMMANDS True
    PREFIX ""
    DEBUG_POSTFIX "_d"
    SUFFIX ".pyd"
)
if(MSVC)
    target_compile_options(pyric PRIVATE /W4)
else()
    target_compile_options(pyric PRIVATE -Wall -Wextra -Wpedantic)
endif()

add_subdirectory(pyunrealsdk EXCLUDE_FROM_ALL)

file(GLOB sources CONFIGURE_DEPENDS "src/*.cpp" "src/*.h")
target_sources(pyric PRIVATE ${sources})

target_link_libraries(pyric PUBLIC pyunrealsdk)

if(MSVC)
    # Enable Edit and Continue - replace /Zi with /ZI
    string(REPLACE "/Zi" "" CMAKE_C_FLAGS_DEBUG "${CMAKE_C_FLAGS_DEBUG}")
    string(REPLACE "/Zi" "" CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG}")
    target_compile_options(pyric PUBLIC "$<$<CONFIG:DEBUG>:/ZI>")

    target_link_options(pyric PUBLIC "/INCREMENTAL")

    # Only enable /GL (which conflicts with /ZI) in release mode
    string(REPLACE "/GL" "" CMAKE_C_COMPILE_OPTIONS_IPO "${CMAKE_C_COMPILE_OPTIONS_IPO}")
    string(REPLACE "/GL" "" CMAKE_CXX_COMPILE_OPTIONS_IPO "${CMAKE_CXX_COMPILE_OPTIONS_IPO}")
    target_compile_options(pyric PUBLIC "$<$<CONFIG:RELEASE>:/GL>")

    # UTF-8 encoded source files
    target_compile_options(pyric PUBLIC "/utf-8")
endif()

if(MINGW)
    # Link `libc++.dll` and `libunwind.dll` statically
    target_link_options(pyric PRIVATE "-static-libstdc++" "-Wl,-Bstatic" "-lunwind")

    # Workaround until llvm-project 692518d04b makes it into a release (i.e. 17)
    target_compile_definitions(pyric PRIVATE _LIBCXXABI_DISABLE_VISIBILITY_ANNOTATIONS)
endif()
