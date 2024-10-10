import jinja2
import shlex
import subprocess
import sys
import sysconfig


def build_environment(c):
    """
    Sets up the build environment inside the context.
    """

    c.var("make", "make -j12")

    # c.var("sysroot", c.tmp / f"sysroot.{c.platform}-{c.arch}")
    c.var("build_platform", sysconfig.get_config_var("HOST_GNU_TYPE"))

    c.env("CPPFLAGS", "-I{{ install }}/include")
    c.env("CFLAGS", "-I{{ install }}/include")
    c.env("CPPFLAGS", "-I{{ install }}/include/SDL2")
    c.env("CFLAGS", "-I{{ install }}/include/SDL2")

    c.env("PATH", "{{ host }}/bin:{{ PATH }}")

    if (c.platform == "linux") and (c.arch == "x86_64"):
        c.var("host_platform", "x86_64-pc-linux-gnu")
    elif (c.platform == "linux") and (c.arch == "i686"):
        c.var("host_platform", "i686-pc-linux-gnu")
    elif (c.platform == "linux") and (c.arch == "armv7l"):
        c.var("host_platform", "armv7hl-meego-linux-gnueabi")
    elif (c.platform == "windows") and (c.arch == "x86_64"):
        c.var("host_platform", "x86_64-w64-mingw32")
    elif (c.platform == "windows") and (c.arch == "i686"):
        c.var("host_platform", "i686-w64-mingw32")
    elif (c.platform == "mac") and (c.arch == "x86_64"):
        c.var("host_platform", "x86_64-apple-darwin14")
    elif (c.platform == "android") and (c.arch == "x86_64"):
        c.var("host_platform", "x86_64-linux-android")
    elif (c.platform == "android") and (c.arch == "arm64_v8a"):
        c.var("host_platform", "aarch64-linux-android")
    elif (c.platform == "android") and (c.arch == "armeabi_v7a"):
        c.var("host_platform", "armv7a-linux-androideabi")
    elif (c.platform == "ios") and (c.arch == "arm64"):
        c.var("host_platform", "arm-apple-darwin")
    elif (c.platform == "ios") and (c.arch == "armv7s"):
        c.var("host_platform", "arm-apple-darwin")
    elif (c.platform == "ios") and (c.arch == "sim-arm64"):
        c.var("host_platform", "arm-apple-darwin")
    elif (c.platform == "ios") and (c.arch == "sim-x86_64"):
        c.var("host_platform", "x86_64-apple-darwin")

    if (c.platform == "ios") and (c.arch == "arm64"):
        c.var("sdl_host_platform", "arm-ios-darwin21")
    elif (c.platform == "ios") and (c.arch == "armv7s"):
        c.var("sdl_host_platform", "arm-ios-darwin21")
    elif (c.platform == "ios") and (c.arch == "sim-arm64"):
        c.var("sdl_host_platform", "arm-ios-darwin21")
    elif (c.platform == "ios") and (c.arch == "sim-x86_64"):
        c.var("sdl_host_platform", "x86_64-ios-darwin21")
    else:
        c.var("sdl_host_platform", "{{ host_platform }}")

    if (c.platform == "ios") and (c.arch == "arm64"):
        c.var("ffi_host_platform", "aarch64-ios-darwin21")
    elif (c.platform == "ios") and (c.arch == "sim-arm64"):
        c.var("ffi_host_platform", "aarch64-ios-darwin21")
    else:
        c.var("ffi_host_platform", "{{ host_platform }}")

    c.env("LDFLAGS", "-L{{install}}/lib")

    if (c.platform == "ios") and (c.arch == "arm64"):
        c.env("IPHONEOS_DEPLOYMENT_TARGET", "13.0")
    elif (c.platform == "ios") and (c.arch == "armv7s"):
        c.env("IPHONEOS_DEPLOYMENT_TARGET", "13.0")
    elif (c.platform == "ios") and (c.arch == "sim-arm64"):
        c.env("IPHONEOS_DEPLOYMENT_TARGET", "13.0")
    elif (c.platform == "ios") and (c.arch == "sim-x86_64"):
        c.env("IPHONEOS_DEPLOYMENT_TARGET", "13.0")

    if c.kind == "host":

        # c.env("CC", "gcc")
        # c.env("CXX", "g++")
        # c.env("CPP", "gcc")
        # c.env("LD", "ld")
        # c.env("AR", "ar")
        # c.env("RANLIB", "ranlib")

        c.env("LDFLAGS", "{{ LDFLAGS }} -L{{install}}/lib")

    elif c.kind == "cross":

        if (c.platform == "mac") or (c.platform == "ios"):

            c.env("CC", "ccache clang")
            c.env("CXX", "ccache clang++")
            c.env("CPP", "ccache clang -E")
            c.env("LD", "ccache llvm-ld")
            c.env("AR", "ccache llvm-ar")
            c.env("RANLIB", "ccache llvm-ranlib")

            c.env("LDFLAGS", "{{ LDFLAGS }} -L{{install}}/lib64")

        else:

            c.env("CC", "ccache gcc -fPIC")
            c.env("CXX", "ccache g++ -fPIC")
            c.env("CPP", "ccache gcc -E")
            c.env("LD", "ccache ld")
            c.env("AR", "ccache ar")
            c.env("RANLIB", "ccache ranlib")

            c.env("LDFLAGS", "{{ LDFLAGS }} -L{{install}}/lib64")

    elif (c.platform == "linux") and (c.arch == "x86_64"):

        c.var("crossbin", "{{ cross }}/bin/{{ host_platform}}-")

        c.env("CC", "ccache {{ crossbin }}gcc -m64 -O3 -fPIC -pthread")
        c.env("CXX", "ccache {{ crossbin }}g++ -m64 -O3 -fPIC -pthread")
        c.env("CPP", "ccache {{ crossbin }}gcc -m64 -E ")
        c.env("LD", "ccache ld -fPIC")
        c.env("AR", "ccache gcc-ar")
        c.env("RANLIB", "ccache gcc-ranlib")
        c.env("STRIP", "ccache strip")
        c.env("NM", "nm")

        c.env("LDFLAGS", "{{ LDFLAGS }} -Wl,-rpath-link")
        c.env("LDFLAGS", "{{ LDFLAGS }} -Wl,-rpath-link")
        c.env("LDFLAGS", "{{ LDFLAGS }} -Wl,-rpath-link")
        c.env("LDFLAGS", "{{ LDFLAGS }} -L{{install}}/lib")

        c.env("PKG_CONFIG_LIBDIR", "{{ PKG_CONFIG_LIBDIR }}:/usr/lib/pkgconfig")

    elif (c.platform == "linux") and (c.arch == "i686"):

        c.var("crossbin", "{{ cross }}/bin/{{ host_platform }}-")

        c.env("CC", "ccache {{ crossbin }}gcc -m32 -fPIC -O3 -pthread")
        c.env("CXX", "ccache {{ crossbin }}g++ -m32 -fPIC -O3 -pthread")
        c.env("CPP", "ccache {{ crossbin }}gcc -m32 -E")
        c.env("LD", "ccache ld -fPIC")
        c.env("AR", "ccache gcc-ar")
        c.env("RANLIB", "ccache gcc-ranlib")
        c.env("STRIP", "ccache strip")
        c.env("NM", "nm")

        c.env("LDFLAGS", "{{ LDFLAGS }} -Wl,-rpath-link")
        c.env("LDFLAGS", "{{ LDFLAGS }} -Wl,-rpath-link")
        c.env("LDFLAGS", "{{ LDFLAGS }} -Wl,-rpath-link")
        c.env("LDFLAGS", "{{ LDFLAGS }} -L{{install}}/lib")

        c.env("PKG_CONFIG_LIBDIR", "{{ PKG_CONFIG_LIBDIR }}:/usr/lib/pkgconfig")

    elif (c.platform == "linux") and (c.arch == "armv7l"):

        c.var("crossbin", "/usr/bin/{{ host_platform }}-")

        c.env("CC", "ccache {{ crossbin }}gcc -fPIC -O3 -pthread")
        c.env("CXX", "ccache {{ crossbin }}g++ -fPIC -O3 -pthread")
        c.env("CPP", "ccache {{ crossbin }}gcc -E")
        c.env("LD", "ccache ld -fPIC")
        c.env("AR", "ccache gcc-ar")
        c.env("RANLIB", "ccache gcc-ranlib")
        c.env("STRIP", "ccache strip")
        c.env("NM", "nm")

        c.env("LDFLAGS", "{{ LDFLAGS }} -Wl,-rpath-link")
        c.env("LDFLAGS", "{{ LDFLAGS }} -Wl,-rpath-link")
        c.env("LDFLAGS", "{{ LDFLAGS }} -L{{install}}/lib ")

        c.env("PKG_CONFIG_LIBDIR", "{{ PKG_CONFIG_LIBDIR }}:/usr/lib/pkgconfig")

    elif (c.platform == "linux") and (c.arch == "arm64"):

        c.var("crossbin", "/usr/bin/{{ host_platform }}-")

        c.env("CC", "ccache {{ crossbin }}gcc -fPIC -O3 -pthread")
        c.env("CXX", "ccache {{ crossbin }}g++ -fPIC -O3 -pthread")
        c.env("CPP", "ccache {{ crossbin }}gcc -E")
        c.env("LD", "ccache ld -fPIC")
        c.env("AR", "ccache gcc-ar")
        c.env("RANLIB", "ccache gcc-ranlib")
        c.env("STRIP", "ccache strip")
        c.env("NM", "nm")

        c.env("LDFLAGS", "{{ LDFLAGS }} -Wl,-rpath-link")
        c.env("LDFLAGS", "{{ LDFLAGS }} -Wl,-rpath-link")
        c.env("LDFLAGS", "{{ LDFLAGS }} -L{{install}}/lib ")

        c.env("PKG_CONFIG_LIBDIR", "{{ PKG_CONFIG_LIBDIR }}:/usr/lib/pkgconfig")

    elif (c.platform == "windows") and (c.arch == "x86_64"):

        c.var("crossbin", "/usr/bin/{{ host_platform }}-")

        c.env("CC", "ccache {{ crossbin }}gcc --ccache-skip -specs --ccache-skip {{root}}/specs/x86_64-ucrt -fPIC -O3")
        c.env("CXX", "ccache {{ crossbin }}g++ --ccache-skip -specs --ccache-skip {{root}}/specs/x86_64-ucrt -fPIC -O3")
        c.env("CPP", "ccache {{ crossbin }}gcc --ccache-skip -specs --ccache-skip {{root}}/specs/x86_64-ucrt -E")
        c.env("LD", "ccache {{ crossbin}}ld")
        c.env("AR", "ccache {{ crossbin }}gcc-ar")
        c.env("RANLIB", "ccache {{ crossbin }}gcc-ranlib")
        c.env("WINDRES", "ccache {{ crossbin }}windres")
        c.env("STRIP", "ccache llvm-strip")
        c.env("NM", "{{ crossbin}}nm")

    elif (c.platform == "windows") and (c.arch == "i686"):

        c.var("crossbin", "/usr/bin/{{ host_platform }}-")

        c.env("CC", "ccache {{ crossbin }}gcc --ccache-skip -specs --ccache-skip {{root}}/specs/i686-ucrt -fPIC -O3")
        c.env("CXX", "ccache {{ crossbin }}g++ --ccache-skip -specs --ccache-skip {{root}}/specs/i686-ucrt -fPIC -O3")
        c.env("CPP", "ccache {{ crossbin }}gcc --ccache-skip -specs --ccache-skip {{root}}/specs/i686-ucrt -E")
        c.env("LD", "ccache {{ crossbin}}ld")
        c.env("AR", "ccache {{ crossbin }}ar")
        c.env("RANLIB", "ccache {{ crossbin }}ranlib")
        c.env("WINDRES", "ccache {{ crossbin }}windres")
        c.env("STRIP", "ccache llvm-strip")
        c.env("NM", "{{ crossbin}}nm")

    elif (c.platform == "mac") and (c.arch == "x86_64"):

        c.var("crossbin", "{{ cross }}/bin/{{ host_platform }}-")

        c.env("MACOSX_DEPLOYMENT_TARGET", "10.10")

        c.env("CC", "ccache {{ crossbin }}clang -fPIC -O3 -pthread")
        c.env("CXX", "ccache {{ crossbin }}clang++ -fPIC -O3 -pthread")
        c.env("CPP", "ccache {{ crossbin }}clang -E ")
        c.env("LD", "ccache {{ crossbin}}ld")
        c.env("AR", "ccache {{ crossbin }}ar")
        c.env("RANLIB", "ccache {{ crossbin }}ranlib")
        c.env("STRIP", "ccache  {{ crossbin }}strip")
        c.env("NM", "{{ crossbin}}nm")

    elif (c.platform == "android") and (c.arch == "x86_64"):

        c.var("crossbin", "{{ cross }}/android-ndk-r21d/toolchains/llvm/prebuilt/linux-x86_64/bin/{{ host_platform }}-")
        c.var("crossclang", "{{ cross }}/android-ndk-r21d/toolchains/llvm/prebuilt/linux-x86_64/bin/{{ host_platform }}21-")

        c.env("CC", "ccache {{ crossclang }}clang -fPIC -O3 -pthread")
        c.env("CXX", "ccache {{ crossclang }}clang++ -fPIC -O3 -pthread")
        c.env("CPP", "ccache {{ crossclang }}clang -E")
        c.env("LD", "ccache {{ crossbin}}ld")
        c.env("AR", "ccache {{ crossbin }}ar")
        c.env("RANLIB", "ccache {{ crossbin }}ranlib")
        c.env("STRIP", "ccache  {{ crossbin }}strip")
        c.env("NM", "{{ crossbin}}nm")

        c.env("CFLAGS", "{{ CFLAGS }} -DSDL_MAIN_HANDLED")

    elif (c.platform == "android") and (c.arch == "arm64_v8a"):

        c.var("crossbin", "{{ cross }}/android-ndk-r21d/toolchains/llvm/prebuilt/linux-x86_64/bin/{{ host_platform }}-")
        c.var("crossclang", "{{ cross }}/android-ndk-r21d/toolchains/llvm/prebuilt/linux-x86_64/bin/{{ host_platform }}21-")

        c.env("CC", "ccache {{ crossclang }}clang -fPIC -O3 -pthread")
        c.env("CXX", "ccache {{ crossclang }}clang++ -fPIC -O3 -pthread")
        c.env("CPP", "ccache {{ crossclang }}clang -E")
        c.env("LD", "ccache {{ crossbin}}ld")
        c.env("AR", "ccache {{ crossbin }}ar")
        c.env("RANLIB", "ccache {{ crossbin }}ranlib")
        c.env("STRIP", "ccache  {{ crossbin }}strip")
        c.env("NM", "{{ crossbin}}nm")

        c.env("CFLAGS", "{{ CFLAGS }} -DSDL_MAIN_HANDLED")

    elif (c.platform == "android") and (c.arch == "armeabi_v7a"):

        c.var("crossbin", "{{ cross }}/android-ndk-r21d/toolchains/llvm/prebuilt/linux-x86_64/bin/arm-linux-androideabi-")
        c.var("crossclang", "{{ cross }}/android-ndk-r21d/toolchains/llvm/prebuilt/linux-x86_64/bin/{{ host_platform }}21-")

        c.env("CC", "ccache {{ crossclang }}clang -fPIC -O3 -pthread -fno-integrated-as")
        c.env("CXX", "ccache {{ crossclang }}clang++ -fPIC -O3 -pthread  -fno-integrated-as")
        c.env("CPP", "ccache {{ crossclang }}clang -E")
        c.env("LD", "ccache {{ crossbin}}ld")
        c.env("AR", "ccache {{ crossbin }}ar")
        c.env("RANLIB", "ccache {{ crossbin }}ranlib")
        c.env("STRIP", "ccache  {{ crossbin }}strip")
        c.env("NM", "{{ crossbin}}nm")

        c.env("CFLAGS", "{{ CFLAGS }} -DSDL_MAIN_HANDLED")

    elif (c.platform == "ios") and (c.arch == "arm64"):

        c.var("llver", "13")
        c.var("clang_args", "-fuse-ld=lld -target arm64-apple-ios13.0 -isysroot {{cross}}/sdk -Wno-unused-command-line-argument")

        c.env("CC", "ccache clang-{{ llver }} {{ clang_args }} -fPIC -O3 -pthread")
        c.env("CXX", "ccache clang++-{{ llver }} {{ clang_args }} -fPIC -O3 -pthread")
        c.env("CPP", "ccache clang-{{ llver }} {{ clang_args }} -E --sysroot {{ cross }}/sdk ")
        c.env("AR", "ccache llvm-ar-{{ llver }}")
        c.env("RANLIB", "ccache llvm-ranlib-{{ llver }}")
        c.env("STRIP", "ccache llvm-strip-{{ llver }}")
        c.env("NM", "llvm-nm-{{ llver }}")

        c.env("CFLAGS", "{{ CFLAGS }} -DSDL_MAIN_HANDLED -miphoneos-version-min=13.0")
        c.env("LDFLAGS", "{{ LDFLAGS }} -miphoneos-version-min=13.0 -lmockrt")

    elif (c.platform == "ios") and (c.arch == "sim-arm64"):

        c.var("llver", "13")
        c.var("clang_args", "-fuse-ld=lld -target arm64-apple-ios13.0-simulator -isysroot {{cross}}/sdk -Wno-unused-command-line-argument")

        c.env("CC", "ccache clang-{{ llver }} {{ clang_args }} -fPIC -O3 -pthread")
        c.env("CXX", "ccache clang++-{{ llver }} {{ clang_args }} -fPIC -O3 -pthread")
        c.env("CPP", "ccache clang-{{ llver }} {{ clang_args }} -E --sysroot {{ cross }}/sdk ")
        c.env("AR", "ccache llvm-ar-{{ llver }}")
        c.env("RANLIB", "ccache llvm-ranlib-{{ llver }}")
        c.env("STRIP", "ccache llvm-strip-{{ llver }}")
        c.env("NM", "llvm-nm-{{ llver }}")

        c.env("CFLAGS", "{{ CFLAGS }} -DSDL_MAIN_HANDLED -mios-simulator-version-min=13.0")
        c.env("LDFLAGS", "{{ LDFLAGS }} -mios-version-min=13.0 -lmockrt")

    elif (c.platform == "ios") and (c.arch == "sim-x86_64"):

        c.var("llver", "13")
        c.var("clang_args", "-fuse-ld=lld -target x86_64-apple-ios13.0-simulator -isysroot {{cross}}/sdk -Wno-unused-command-line-argument")

        c.env("CC", "ccache clang-{{ llver }} {{ clang_args }} -fPIC -O3 -pthread")
        c.env("CXX", "ccache clang++-{{ llver }} {{ clang_args }} -fPIC -O3 -pthread")
        c.env("CPP", "ccache clang-{{ llver }} {{ clang_args }} -E --sysroot {{ cross }}/sdk ")
        c.env("AR", "ccache llvm-ar-{{ llver }}")
        c.env("RANLIB", "ccache llvm-ranlib-{{ llver }}")
        c.env("STRIP", "ccache llvm-strip-{{ llver }}")
        c.env("NM", "llvm-nm-{{ llver }}")

        c.env("CFLAGS", "{{ CFLAGS }} -DSDL_MAIN_HANDLED -mios-simulator-version-min=13.0")
        c.env("LDFLAGS", "{{ LDFLAGS }} -mios-simulator-version-min=13.0 -lmockrt")

    c.env("PKG_CONFIG_PATH", "{{ install }}/lib/pkgconfig")
    c.env("PKG_CONFIG", "pkg-config --libs")

    c.env("CFLAGS", "{{ CFLAGS }} -DRENPY_BUILD")

    if c.kind != "host":
        c.var("cross_config", "--host={{ host_platform }} --build={{ build_platform }}")
        c.var("sdl_cross_config", "--host={{ sdl_host_platform }} --build={{ build_platform }}")
        c.var("ffi_cross_config", "--host={{ ffi_host_platform }} --build={{ build_platform }}")


def run(command, context, verbose=False, quiet=False):
    args = shlex.split(command)

    if verbose:
        print(" ".join(shlex.quote(i) for i in args))

    if not quiet:
        p = subprocess.run(args, cwd=context.cwd, env=context.environ)
    else:
        with open("/dev/null", "w") as f:
            p = subprocess.run(args, cwd=context.cwd, env=context.environ, stdout=f, stderr=f)

    if p.returncode != 0:
        print(f"{context.task_name}: process failed with {p.returncode}.")
        print("args:", args)
        import traceback
        traceback.print_stack()
        sys.exit(1)
