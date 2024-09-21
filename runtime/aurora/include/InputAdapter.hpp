#pragma once

#include <functional>

#include <SDL2/SDL.h>

namespace renpy {

class AuroraOSInputAdapter {
public:
    static void InstallInputEventsFilter(SDL_Window* window);
    static void RemoveInputEventsFilter(SDL_Window* window);
};

} // namespace renpy
