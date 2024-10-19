#include "Python.h"

#include <QUrl>
#include <QVariantMap>

#include <QDBusContext>
#include <QDBusConnection>
#include <QDBusMessage>
#include <QDBusPendingCall>

#include <SDL2/SDL_mouse.h>

#include "Utilities.hpp"

static constexpr auto Intent_Service = "ru.omp.RuntimeManager";
static constexpr auto Intent_Path = "/ru/omp/RuntimeManager/Intents1";
static constexpr auto Intent_IFace = "ru.omp.RuntimeManager.Intents1";
static constexpr auto Intent_Method = "InvokeIntent";
static constexpr auto Intent_Hints = "";
static constexpr auto Intent_IntentMethod = "OpenURI";

static PyObject * AuroraEmbedException;

static PyObject *auroraembed_get_mouse(PyObject *self, PyObject *args) {
    using namespace renpy;

    auto window = SDL_GL_GetCurrentWindow();
    if(!window) {
        PyErr_SetString(AuroraEmbedException, "SDL Window does not exist");
        return NULL;
    }

    int sourceW, sourceH;
    SDL_GL_GetDrawableSize(window, &sourceW, &sourceH);

    const bool fbNativePortrait = (sourceW < sourceH);
    
    int mouseX = 0, mouseY = 0;
    SDL_GetMouseState(&mouseX, &mouseY);

    if(fbNativePortrait) {
        float x = float(mouseX) / sourceW;
        float y = float(mouseY) / sourceH;

        vec2 rotated = rotateUV(vec2(x, y), degreesToRadians(90.0));

        mouseX = rotated.x * sourceH;
        mouseY = rotated.y * sourceW;
    }

    return Py_BuildValue("ii", mouseX, mouseY);
}

static PyObject *auroraembed_set_mouse(PyObject *self, PyObject *args) {
    using namespace renpy;

    int mouseX, mouseY;

    if ( !PyArg_ParseTuple(args, "ii", &mouseX, &mouseY) ) {
        return NULL;
    }

    auto window = SDL_GL_GetCurrentWindow();
    if(!window) {
        PyErr_SetString(AuroraEmbedException, "SDL Window does not exist");
        return NULL;
    }

    int sourceW, sourceH;
    SDL_GL_GetDrawableSize(window, &sourceW, &sourceH);

    const bool fbNativePortrait = (sourceW < sourceH);

    if(fbNativePortrait) {
        float x = float(mouseX) / sourceH;
        float y = float(mouseY) / sourceW;

        vec2 rotated = rotateUV(vec2(x, y), degreesToRadians(-90.0));

        mouseX = rotated.x * sourceW;
        mouseY = rotated.y * sourceH;
    }

    SDL_WarpMouseInWindow(NULL, mouseX, mouseY);

    Py_RETURN_NONE;
}

static PyObject *auroraembed_open_url(PyObject *self, PyObject *args) {
    char* url_string = NULL;

    if (!PyArg_Parse(args, "s", &url_string)) {
        return NULL; // Oops, something went wrong!
    }
    
    auto request = QDBusMessage::createMethodCall(Intent_Service, Intent_Path, Intent_IFace, Intent_Method);
    request << Intent_IntentMethod;
    request << QVariantMap ();
    request << QVariantMap { { QString("uri"), url_string } } ;
    auto async = QDBusConnection::sessionBus().asyncCall(request);

    Py_RETURN_NONE;
}

static PyMethodDef AuroraEmbedMethods[] = {
    {"open_url", auroraembed_open_url, 0, "OpenURL on Aurora OS"},
    {"get_mouse", auroraembed_get_mouse, 0, "Get mouse coords on Aurora OS"},
    {"set_mouse", auroraembed_set_mouse, METH_VARARGS, "Set mouse coords on Aurora OS"},
    {NULL, NULL, 0, NULL}
};

extern "C" {

PyMODINIT_FUNC 
init_auroraembed(void) {
    PyObject *m;

    m = Py_InitModule("auroraembed", AuroraEmbedMethods);

    if (m == NULL)
        return;
    
    AuroraEmbedException = PyErr_NewException("auroraembed.error", NULL, NULL);
    Py_INCREF(AuroraEmbedException);
    
    PyModule_AddObject(m, "error", AuroraEmbedException);
}

}