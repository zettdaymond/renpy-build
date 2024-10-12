#include "Python.h"

#include <iostream>
#include <QDesktopServices>
#include <QUrl>

static PyObject *auroraembed_open_url(PyObject *self, PyObject *args) {
    char* url_string = NULL;

    if (!PyArg_Parse(args, "s", &url_string)) {
        return NULL; // Oops, something went wrong!
    }

    std::cout << "Try to open url: " << url_string << std::endl;
    QUrl url(url_string);
    
    std::cout << "Parsed url: " << url.toString().toStdString() << std::endl;
    
    auto result = QDesktopServices::openUrl(url);

    if(result) {
        Py_RETURN_TRUE;
    }
    else {
        Py_RETURN_FALSE;
    }
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