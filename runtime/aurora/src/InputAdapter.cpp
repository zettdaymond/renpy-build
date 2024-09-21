#include "InputAdapter.hpp"

#include <functional>
#include <memory>

#include "Utilities.hpp"

#include "AuroraOSAudio.hpp"
#include "ComposerAdapter.hpp"
#include "DisplayBlankerController.hpp"

#include <SDL2/SDL_video.h>

namespace renpy {

namespace {

struct WindowSizesProvider {
    SDL_Window* sdl_window = nullptr;
    bool isSuspended = false;
};

static SDL_EventFilter rotate_and_fit_filter = [](void* userdata, SDL_Event* event) -> int {
    auto window = static_cast<WindowSizesProvider*>(userdata);
    if (!window) {
        return 1;
    }

    int sourceW, sourceH;
    SDL_GL_GetDrawableSize(window->sdl_window, &sourceW, &sourceH);

    const bool fbNativePortrait = (sourceW < sourceH);

    if (fbNativePortrait && event->type == SDL_MOUSEMOTION) {
        float x = float(event->motion.x) / sourceW;
        float y = float(event->motion.y) / sourceH;

        vec2 rotated = rotateUV(vec2(x, y), degreesToRadians(90.0));

        event->motion.x = rotated.x * sourceH;
        event->motion.y = rotated.y * sourceW;
    }

    if (fbNativePortrait && (event->type == SDL_MOUSEBUTTONDOWN || event->type == SDL_MOUSEBUTTONUP)) {
        float x = float(event->button.x) / sourceW;
        float y = float(event->button.y) / sourceH;

        vec2 rotated = rotateUV(vec2(x, y), degreesToRadians(90.0));

        event->button.x = rotated.x * sourceH;
        event->button.y = rotated.y * sourceW;
    }

    if (fbNativePortrait
        && (event->type == SDL_FINGERDOWN || event->type == SDL_FINGERUP || event->type == SDL_FINGERMOTION)) {
        vec2 rotatedFingerUV = rotateUV(vec2(event->tfinger.x, event->tfinger.y), degreesToRadians(90.0));
        event->tfinger.x = rotatedFingerUV.x;
        event->tfinger.y = rotatedFingerUV.y;
    }

    if (event->type == SDL_WINDOWEVENT) {

        // Minimizing on Aurora os
        if (event->window.event == SDL_WINDOWEVENT_FOCUS_LOST) {
            DisplayBlankerController::SetPreventDisplayBlanking(false);

            //release audio lock
            if (AudioresourceHolder::audio_resource) {
                AudioresourceHolder::audio_resource = nullptr;
            }
        }

        //Maximizing
        if (event->window.event == SDL_WINDOWEVENT_FOCUS_GAINED) {
            DisplayBlankerController::SetPreventDisplayBlanking(true);

            //aquire audio lock
            if (!AudioresourceHolder::audio_resource) {
                AudioresourceHolder::audio_resource = AudioResource::Aquire();
            }
        }
    }

    if (event->type == SDL_WINDOWEVENT) {
        SDL_LogVerbose(SDL_LOG_CATEGORY_APPLICATION, "Gained window event %i", event->window.event);
        switch (event->window.event) {
            // renpy умеет реагировать на события SDL_APP_DIDENTERFOREGROUND / SDL_APP_WILLENTERBACKGROUND
            // И останавливать или воостанавливать свое состояние на основе этих событий

            case SDL_WINDOWEVENT_FOCUS_GAINED: {
                SDL_Event event;
                event.type = SDL_APP_DIDENTERFOREGROUND;
                SDL_PushEvent(&event);

                window->isSuspended = false;

                break;
            }
            case SDL_WINDOWEVENT_FOCUS_LOST: {
                SDL_Event event;
                event.type = SDL_APP_WILLENTERBACKGROUND;
                SDL_PushEvent(&event);

                window->isSuspended = true;

                break;
            }
        }
    }

    // renpy в режиме suspend ждет когда ему скажут что надо прибить приложение эвентом SDL_APP_TERMINATING
    // или продолжим работу отправив SDL_APP_DIDENTERFOREGROUND
    // Эмулируем поведение iOS/Android
    if(event->type == SDL_QUIT && window->isSuspended) {
        SDL_Event event;
        event.type = SDL_APP_TERMINATING;
        SDL_PushEvent(&event);
    }

    return 1;
};

std::unique_ptr<WindowSizesProvider> window_sizes_provider;

} // namespace

void AuroraOSInputAdapter::InstallInputEventsFilter(SDL_Window* window)
{
    if (!window) {
        return;
    }

    SDL_SetEventFilter(nullptr, window);

    window_sizes_provider = std::make_unique<WindowSizesProvider>();
    window_sizes_provider->sdl_window = window;

    SDL_SetEventFilter(rotate_and_fit_filter, window_sizes_provider.get());
}

void AuroraOSInputAdapter::RemoveInputEventsFilter(SDL_Window* window)
{
    SDL_SetEventFilter(nullptr, window);
}

} // namespace renpy
