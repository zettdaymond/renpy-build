from renpybuild.context import Context
from renpybuild.task import task, annotator
import shutil
import os


@task()
def build(c: Context):
    c.run("""mkdir -p libauroraintegration-build""")

    previous_libdir = c.get_env("PKG_CONFIG_LIBDIR")
    previous_pkg_conf = c.get_env("PKG_CONFIG_LIBDIR")
    c.env("PKG_CONFIG_LIBDIR", "/usr/lib/pkgconfig:{{ PKG_CONFIG_LIBDIR }}")
    c.env("PKG_CONFIG", "pkg-config")

    c.run("""
        cmake
        -G Ninja
        -S {{ runtime }}/aurora
        -B libauroraintegration-build
        -DCMAKE_INSTALL_PREFIX={{install}}
        """)

    c.env("PKG_CONFIG", previous_pkg_conf)
    c.env("PKG_CONFIG_LIBDIR", previous_libdir)

    c.run("""
          cmake
          --build libauroraintegration-build
          --target install
          """)