from renpybuild.model import task, Context

# 1.5.3 is the last version that supported ./configure.
version = "3.0.4"

@task()
def download(c: Context):
    c.var("version", version)

    c.clean("{{ tmp }}/source/libjpeg-turbo-{{version}}")
    c.chdir("{{ tmp }}/source")

    c.run("git clone --branch {{ version }} --depth 1 https://github.com/libjpeg-turbo/libjpeg-turbo libjpeg-turbo-{{version}}")


@task()
def build(c):
    c.var("version", version)
    c.run("""mkdir -p libjpeg-turbo-{{version}}-build""")

    previous_libdir = c.get_env("PKG_CONFIG_LIBDIR")
    previous_pkg_conf = c.get_env("PKG_CONFIG_LIBDIR")
    c.env("PKG_CONFIG_LIBDIR", "/usr/lib/pkgconfig:{{ PKG_CONFIG_LIBDIR }}")
    c.env("PKG_CONFIG", "pkg-config")

    c.run("""
        cmake
        -B libjpeg-turbo-{{version}}-build
        -S {{ tmp }}/source/libjpeg-turbo-{{version}}
        -G Ninja
        -DCMAKE_INSTALL_PREFIX={{install}}
        -DCMAKE_CXX_COMPILER_LAUNCHER=ccache
        -DCMAKE_C_COMPILER_LAUNCHER=ccache
        -DENABLE_SHARED=FALSE
        """)

    c.env("PKG_CONFIG", previous_pkg_conf)
    c.env("PKG_CONFIG_LIBDIR", previous_libdir)

    c.run("""
          cmake
          --build libjpeg-turbo-{{version}}-build
          --target install
          """)


