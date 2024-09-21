#include "ComposerAdapter.hpp"

#include <SDL2/SDL.h>

#define SDL_VIDEO_DRIVER_WAYLAND
#include <SDL2/SDL_syswm.h>

#include <wayland-client-protocol.h>
#include <wayland-client.h>

namespace renpy {

void WaylandComposerAdapter::SetWindowOrientation(SDL_Window* window, SDL_DisplayOrientation orientation)
{
    if (!window) {
        return;
    }

    SDL_SysWMinfo info;
    SDL_VERSION(&info.version)
    SDL_GetWindowWMInfo(window, &info);

    auto wayland_orientation = (orientation == SDL_ORIENTATION_LANDSCAPE_FLIPPED) ? WL_OUTPUT_TRANSFORM_270
                               : (orientation == SDL_ORIENTATION_LANDSCAPE)       ? WL_OUTPUT_TRANSFORM_90
                                                                                  : WL_OUTPUT_TRANSFORM_NORMAL;

    wl_surface* sdl_wl_surface = info.info.wl.surface;
    wl_surface_set_buffer_transform(sdl_wl_surface, wayland_orientation);
}

} // namespace renpy
