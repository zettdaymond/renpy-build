#include "Python.h"

#include <QUrl>
#include <QVariantMap>

#include <QDBusContext>
#include <QDBusConnection>
#include <QDBusMessage>
#include <QDBusPendingCall>

static constexpr auto Intent_Service = "ru.omp.RuntimeManager";
static constexpr auto Intent_Path = "/ru/omp/RuntimeManager/Intents1";
static constexpr auto Intent_IFace = "ru.omp.RuntimeManager.Intents1";
static constexpr auto Intent_Method = "InvokeIntent";
static constexpr auto Intent_Hints = "";
static constexpr auto Intent_IntentMethod = "OpenURI";

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
    {NULL, NULL, 0, NULL}
};

extern "C" {

PyMODINIT_FUNC 
init_auroraembed(void) {
    (void) Py_InitModule("auroraembed", AuroraEmbedMethods);
}

}