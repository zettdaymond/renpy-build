cmake_minimum_required(VERSION 3.11)
project(auroraintegration CXX)

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

set_target_properties(${PROJECT_NAME} 
    PROPERTIES 
        PUBLIC_HEADER "include/AuroraIntegration.h"
)

install(TARGETS ${PROJECT_NAME}
    LIBRARY DESTINATION ${CMAKE_INSTALL_PREFIX}/lib
    PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_PREFIX}/include
)
