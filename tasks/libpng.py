from renpybuild.model import task, Context

version = "1.6.37"


@task()
def unpack(c):
    c.clean()

    c.var("version", version)
    c.run("tar xzf {{source}}/libpng-{{version}}.tar.gz")


@task()
def build(c: Context) :
    c.var("version", version)
    c.chdir("libpng-{{version}}")
    c.run("""mkdir -p build""")

    c.env("CPPFLAGS", "{{ CPPFLAGS }} -DPNG_NO_CONSOLE_IO")

    previous_libdir = c.get_env("PKG_CONFIG_LIBDIR")
    previous_pkg_conf = c.get_env("PKG_CONFIG_LIBDIR")
    c.env("PKG_CONFIG_LIBDIR", "/usr/lib/pkgconfig:{{ PKG_CONFIG_LIBDIR }}")
    c.env("PKG_CONFIG", "pkg-config")

    c.run("""
        cmake
        -B build
        -G Ninja
        -DCMAKE_INSTALL_PREFIX={{install}}
        -DCMAKE_CXX_COMPILER_LAUNCHER=ccache
        -DCMAKE_C_COMPILER_LAUNCHER=ccache
        -DPNG_SHARED=OFF
        -DPNG_TESTS=OFF
        -DZLIB_ROOT={{ install }}
        """)

    c.env("PKG_CONFIG", previous_pkg_conf)
    c.env("PKG_CONFIG_LIBDIR", previous_libdir)

    c.run("""
          cmake
          --build build
          --target install
          """)

