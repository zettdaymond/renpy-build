cmake_minimum_required(VERSION 3.12)
project(auroraintegration CXX)

option(BUILD_PYTHON_MODULE "Buld python module or not" ON)

include(FindPkgConfig)

include(FindPkgConfig)
pkg_search_module(WAYLAND REQUIRED wayland-client )
pkg_search_module(DBUS REQUIRED dbus-1)
pkg_search_module(GLIB REQUIRED glib-2.0)
pkg_search_module(AUDIORESOURCE REQUIRED audioresource)

add_library(${PROJECT_NAME} STATIC
    src/AuroraOSAudio.cpp
    include/AuroraOSAudio.hpp
    src/ComposerAdapter.cpp
    include/ComposerAdapter.hpp
    src/DBus.cpp
    include/DBus.hpp
    src/InputAdapter.cpp
    include/InputAdapter.hpp
    src/Utilities.cpp
    include/Utilities.hpp
    src/DisplayBlankerController.cpp
    include/DisplayBlankerController.hpp

    src/AuroraIntegration.cpp
    include/AuroraIntegration.h # C API
)

list(APPEND LIB_PUBLIC_HEADERS "include/AuroraIntegration.h")

if(BUILD_PYTHON_MODULE)
    find_package(Qt5 COMPONENTS Core Gui REQUIRED)
    find_package(Python 2.7 COMPONENTS Development REQUIRED)

    target_sources(${PROJECT_NAME} 
        PUBLIC 
            src/PythonModule.cpp
            include/PythonModule.h # C API
    )
    target_link_libraries(${PROJECT_NAME} 
        PUBLIC 
            Qt5::Core 
            Qt5::Gui 
            Python::Module
    )
    list(APPEND LIB_PUBLIC_HEADERS "include/PythonModule.h")
endif()

target_include_directories(${PROJECT_NAME}
    PUBLIC
        include
        "/usr/include/dbus-1.0" # pkgconfig does not pass include directrories
        "/usr/lib/dbus-1.0/include" # pkgconfig does not pass include directrories
        ${AUDIORESOURCE_INCLUDE_DIRS}
        ${GLIB_INCLUDE_DIRS}
        
)

target_link_libraries(${PROJECT_NAME}
    PUBLIC
        ${AUDIORESOURCE_LIBRARIES}
        ${GLIB_LIBRARIES}
        ${WAYLAND_LIBRARIES}
)

message(STATUS "LIB_PUBLIC_HEADERS : ${LIB_PUBLIC_HEADERS}")
set_target_properties(${PROJECT_NAME} 
    PROPERTIES 
        PUBLIC_HEADER "${LIB_PUBLIC_HEADERS}"
)

install(TARGETS ${PROJECT_NAME}
    LIBRARY DESTINATION ${CMAKE_INSTALL_PREFIX}/lib
    PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_PREFIX}/include
)
