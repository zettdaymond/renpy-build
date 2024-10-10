#!/bin/bash

set -e


ROOT=$(cd $(dirname $0); pwd)
REFS=$ROOT
BASE="$ROOT"

zypper install python

zypper install autoconf autoconf-archive automake make clang llvm
zypper install python3-devel python3-pip

zypper install zlib zlib-devel bzip2 bzip2-devel  xz xz-devel
zypper install libopenssl libopenssl-devel libffi libffi-devel

zypper install libpng libpng-devel libjpeg libjpeg-devel libwebp libwebp-devel libyuv libyuv-devel

zypper install fribidi fribidi-devel freetype freetype-devel harfbuzz harfbuzz-devel
zypper install ffmpeg ffmpeg-devel

zypper install python3-jinja2

zypper install SDL2-devel SDL2_mixer-devel SDL2_image-devel SDL2_ttf-devel

zypper install bc libtool

zypper install libxkbcommon-devel wayland-egl-devel wayland-devel wayland-protocols-devel pulseaudio-devel 
zypper install mesa-llvmpipe-libGLESv2-devel mesa-llvmpipe-libEGL-devel

zypper install libaudioresource-devel glib2-devel dbus-devel 

curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py
python2 get-pip.py

pip2 install virtualenv

Set up the environment variables.

pip2 install -r requirements.txt

VENV="$ROOT/tmp/virtualenv.py2"

export RENPY_DEPS_INSTALL=/usr::/usr/lib/

# . $BASE/nightly/git.sh
. $BASE/nightly/python.sh
