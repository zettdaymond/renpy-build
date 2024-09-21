from renpybuild.context import Context
from renpybuild.task import task, annotator
import shutil
import os

version = "2.0.30"


@annotator
def annotate(c: Context):
    if c.name != "sdl2":
        c.include("{{ install }}/include/SDL2")


def download(c : Context):
    c.clean("{{ tmp }}/source/SDL2-{{version}}")
    c.chdir("{{ tmp }}/source")

    c.run("git clone --branch auroraos-sdl2 https://github.com/zettdaymond/SDL")


@task()
def build(c: Context):
    c.var("version", version)

    c.run("""mkdir -p SDL2-{{version}}-build""")

    previous_libdir = c.get_env("PKG_CONFIG_LIBDIR")
    previous_pkg_conf = c.get_env("PKG_CONFIG_LIBDIR")
    c.env("PKG_CONFIG_LIBDIR", "/usr/lib/pkgconfig:{{ PKG_CONFIG_LIBDIR }}")
    c.env("PKG_CONFIG", "pkg-config")

    c.run("""
        cmake
        -G Ninja
        -S {{ tmp }}/source/SDL2-{{version}}
        -B SDL2-{{version}}-build
        -DCMAKE_INSTALL_PREFIX={{install}}
        -DSDL_STATIC=ON
        -DSDL_SHARED=OFF
        """)

    c.env("PKG_CONFIG", previous_pkg_conf)
    c.env("PKG_CONFIG_LIBDIR", previous_libdir)

    c.run("""
          cmake
          --build SDL2-{{version}}-build
          --target install
          """)

    c.chdir("SDL2-{{version}}-build")