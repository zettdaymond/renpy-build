#pragma once

#include <string_view>

namespace renpy {

class DBus {
public:
    static void Init();
    static void Shutdown();

    static bool CallVoidMethod(const std::string_view node, const std::string_view path,
                               const std::string_view interface, const std::string_view method, ...);
};

} // namespace renpy
