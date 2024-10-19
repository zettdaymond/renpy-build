from renpybuild.model import task, Context

version = "2.2.2"

@task()
def download(c: Context):
    c.var("version", version)

    c.clean("{{ tmp }}/source/zlib-ng-{{version}}")
    c.chdir("{{ tmp }}/source")

    c.run("git clone --branch {{ version }} --depth 1 https://github.com/zlib-ng/zlib-ng zlib-ng-{{version}}")


@task()
def build(c):
    c.var("version", version)
    c.run("""mkdir -p zlib-ng-{{version}}-build""")

    previous_libdir = c.get_env("PKG_CONFIG_LIBDIR")
    previous_pkg_conf = c.get_env("PKG_CONFIG_LIBDIR")
    c.env("PKG_CONFIG_LIBDIR", "/usr/lib/pkgconfig:{{ PKG_CONFIG_LIBDIR }}")
    c.env("PKG_CONFIG", "pkg-config")

    c.run("""
        cmake
        -B zlib-ng-{{version}}-build
        -S {{ tmp }}/source/zlib-ng-{{version}}
        -G Ninja
        -DCMAKE_INSTALL_PREFIX={{install}}
        -DCMAKE_CXX_COMPILER_LAUNCHER=ccache
        -DCMAKE_C_COMPILER_LAUNCHER=ccache
        -DBUILD_SHARED_LIBS=FALSE
        -DWITH_OPTIM=ON
        -DZLIB_COMPAT=ON
        -DWITH_GTEST=OFF
        -DZLIB_ENABLE_TESTS=OFF
        -DWITH_RUNTIME_CPU_DETECTION=ON
        """)

    c.env("PKG_CONFIG", previous_pkg_conf)
    c.env("PKG_CONFIG_LIBDIR", previous_libdir)

    c.run("""
          cmake
          --build zlib-ng-{{version}}-build
          --target install
          """)


