#!/bin/sh
#
#  Copyright 2016 CUBRID Corporation
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# Builds the manager server on its own against an existing CUBRID. When CUBRID is built
# from its own top-level CMakeLists.txt the manager comes along with it and this script
# is not needed.
#
# The CUBRID given with -c may be a source directory, a build directory, or an
# installation; what it has to contain either way is a built libcubridcs, the public
# headers, and the OpenSSL the server was built with.

set -e

progname=$(basename "$0")
source_dir=$(cd "$(dirname "$0")" && pwd)

cubrid_dir="$CUBRID"
build_dir="$source_dir/build_cmake"
build_type="Release"
prefix=""
do_install="no"

usage()
{
  cat <<EOF
Usage: $progname [options]

  -c, --with-cubrid <dir>  CUBRID source, build, or install directory
                           (default: \$CUBRID, currently "${CUBRID:-unset}")
  -p, --prefix <dir>       install prefix (default: the CUBRID directory above)
  -b, --build-dir <dir>    build directory (default: $build_dir)
  -t, --build-type <type>  Release or Debug (default: $build_type)
  -i, --install            install after building
  -h, --help               this message

Examples:
  $progname -c ~/source/cubrid                       # a source tree that has been built
  $progname -c ~/source/cubrid/build_x86_64_release  # a build tree
  $progname -c \$CUBRID -i                            # an installation, then install into it
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    -c|--with-cubrid) cubrid_dir="$2"; shift 2 ;;
    -p|--prefix)      prefix="$2"; shift 2 ;;
    -b|--build-dir)   build_dir="$2"; shift 2 ;;
    -t|--build-type)  build_type="$2"; shift 2 ;;
    -i|--install)     do_install="yes"; shift ;;
    -h|--help)        usage; exit 0 ;;
    *) echo "$progname: unknown option $1" >&2; usage; exit 1 ;;
  esac
done

if [ -z "$cubrid_dir" ]; then
  echo "$progname: no CUBRID given. Use -c <dir> or set \$CUBRID." >&2
  exit 1
fi
if [ ! -d "$cubrid_dir" ]; then
  echo "$progname: $cubrid_dir is not a directory" >&2
  exit 1
fi
cubrid_dir=$(cd "$cubrid_dir" && pwd)

is_install_layout()
{
  [ -f "$1/include/cas_cci.h" ] && [ -f "$1/include/cm_dep.h" ] &&
  [ -f "$1/include/cm_stat.h" ] && [ -n "$(echo "$1"/lib/libcubridcs.so*)" ] &&
  [ -e "$(echo "$1"/lib/libcubridcs.so* | cut -d' ' -f1)" ]
}

cubrid_install=""
if is_install_layout "$cubrid_dir"; then
  cubrid_install="$cubrid_dir"
else
  for candidate in $(find "$cubrid_dir" -maxdepth 4 -type d -name CUBRID -path "*_install*" 2>/dev/null); do
    if is_install_layout "$candidate"; then
      cubrid_install="$candidate"
      break
    fi
  done
fi

if [ -z "$cubrid_install" ]; then
  echo "$progname: no installed CUBRID found at or under $cubrid_dir." >&2
  echo "  Point -c at an installed CUBRID (\$CUBRID), or at a source or build directory" >&2
  echo "  that build.sh has installed into (it leaves one at <build>/_install/CUBRID)." >&2
  exit 1
fi

cubrid_include_dir="$cubrid_install/include"
cubrid_lib_dir="$cubrid_install/lib"

openssl_include_dir="$cubrid_install/include/3rdparty"
openssl_lib_dir="$cubrid_install/lib/3rdparty"
if [ ! -f "$openssl_include_dir/openssl/evp.h" ] || [ ! -f "$openssl_lib_dir/libssl.a" ]; then
  echo "$progname: $cubrid_install has no OpenSSL development files." >&2
  echo "  They are installed under include/3rdparty and lib/3rdparty by a CUBRID built" >&2
  echo "  with WITH_LIBOPENSSL=EXTERNAL; reinstall the server to get them." >&2
  exit 1
fi

if [ -z "$prefix" ]; then
  prefix="$cubrid_install"
fi

echo "CUBRID           : $cubrid_dir"
echo "  headers        : $cubrid_include_dir"
echo "  libraries      : $cubrid_lib_dir"
echo "OpenSSL headers  : $openssl_include_dir"
echo "OpenSSL libraries: $openssl_lib_dir"
echo "install prefix   : $prefix"
echo "build type       : $build_type"

cmake -S "$source_dir" -B "$build_dir" \
  -DCMAKE_BUILD_TYPE="$build_type" \
  -DCMAKE_INSTALL_PREFIX="$prefix" \
  -DCUBRID_INCLUDE_DIR="$cubrid_include_dir" \
  -DCUBRID_LIB_DIR="$cubrid_lib_dir" \
  -DOPENSSL_INCLUDE_DIR="$openssl_include_dir" \
  -DOPENSSL_LIBRARIES="$openssl_lib_dir/libssl.a;$openssl_lib_dir/libcrypto.a"

cmake --build "$build_dir" -j "$(getconf _NPROCESSORS_ONLN 2>/dev/null || echo 4)"

if [ "$do_install" = "yes" ]; then
  cmake --install "$build_dir"
fi

echo "$progname: done"
