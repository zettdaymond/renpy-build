#include <stdlib.h>
#include <thread>

#include <SDL2/SDL_video.h>

#include "DisplayBlankerController.hpp"
#include "InputAdapter.hpp"
#include "ComposerAdapter.hpp"

using namespace renpy;

extern "C" {

typedef void (*AfterWindowCreationHook)(SDL_Window* window);
typedef void (*BeforeWindowDestroyHook)(SDL_Window* window);

void SDL_SetupAfterWindowCreationHook(AfterWindowCreationHook hook);
void SDL_SetupBeforeWindowDestroyHook(BeforeWindowDestroyHook hook);
void SDL_CleanAfterWindowCreationHook();
void SDL_CleanBeforeWindowDestroyHook();
}

void AfterWindowCreation(SDL_Window* window)
{
    WaylandComposerAdapter::SetWindowOrientation(window, SDL_ORIENTATION_LANDSCAPE_FLIPPED);
    AuroraOSInputAdapter::InstallInputEventsFilter(window);
}

void BeforeWindowDestroy(SDL_Window* window)
{
    AuroraOSInputAdapter::RemoveInputEventsFilter(window);
}

#ifdef __cplusplus
extern "C" {
#endif

struct AuroraIntegrationHandle
{
    std::unique_ptr<DisplayBlankerController> controller;
};

AuroraIntegrationHandle* AuroraIntergrationStartup()
{
    auto handle = new AuroraIntegrationHandle();
    
    handle->controller = std::make_unique<DisplayBlankerController>();
    handle->controller->Init();

    SDL_SetupAfterWindowCreationHook(AfterWindowCreation);
    SDL_SetupBeforeWindowDestroyHook(BeforeWindowDestroy);

    return handle;
}

void AuroraIntergrationShutdown(AuroraIntegrationHandle* handle) 
{
    if(!handle) {
        return;
    }

    SDL_SetupAfterWindowCreationHook(NULL);
    SDL_SetupBeforeWindowDestroyHook(NULL);
    
    handle->controller->Shutdown();
    handle->controller = NULL;
}

#ifdef __cplusplus
}
#endif
