#pragma once

#include <optional>

#include <SDL2/SDL.h>

namespace renpy {
class WaylandComposerAdapter {
public:
    static void SetWindowOrientation(SDL_Window* window, SDL_DisplayOrientation orientation);
};
} // namespace renpy
