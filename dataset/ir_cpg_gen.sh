#!/bin/bash

check_error() {
    if [ $? -ne 0 ]; then
        echo $1 >&2
        exit 1
    fi
}

if [ $# -lt 3 ]; then
    echo "./ir_cpg_gen.sh <git_repo_link> <commit_sha> <repo_dir_name> <result_dir_name> <func_1> .. <func_n>" >&2
    exit 1
fi
echo "./ir_cpg_gen.sh $@"
git_repo_link=$1
commit_sha=$2
repo_dir_name=$3
result_dir_name=$4
args_num=$#

if ! test -d "repo_clone"; then
    mkdir repo_clone
fi
cd repo_clone

if test -d $repo_dir_name; then
    cd $repo_dir_name
    make clean && make distclean || scons -c || python2 /usr/bin/scons -c
    git clean -f -d
else
    git clone $git_repo_link $repo_dir_name
    check_error "ERROR: Failed to clone $git_repo_link"
    cd $repo_dir_name
fi  

git reset --hard $commit_sha
if [ "$git_repo_link" == "https://github.com/ned14/nedmalloc.git" ]; then
    sed -i s%'url = git://github.com/ned14/nedtries.git'%'url = https://github.com/ned14/nedtries.git'%g ./.gitmodules
    sed -i s%'url = git://github.com/ned14/nedtries.git'%'url = https://github.com/ned14/nedtries.git'%g ./.git/config
    sed -i s%'-fargument-noalias'%''%g ./SConscript
elif [ "$git_repo_link" == "https://github.com/pgbouncer/pgbouncer.git" ]; then
    sed -i s%'url = git://github.com/markokr/libusual.git'%'url = https://github.com/markokr/libusual.git'%g ./.gitmodules
    sed -i s%'url = git://github.com/markokr/libusual.git'%'url = https://github.com/markokr/libusual.git'%g ./.git/config
elif [ "$git_repo_link" == "https://github.com/atheme/atheme.git" ]; then
    sed -i s%'url = git://github.com/atheme/libmowgli-2.git'%'url = https://github.com/atheme/libmowgli-2.git'%g ./.gitmodules
    sed -i s%'url = git://github.com/atheme/libmowgli-2.git'%'url = https://github.com/atheme/libmowgli-2.git'%g ./.git/config
    sed -i s%'url = git://github.com/atheme/atheme-contrib-modules.git'%'url = https://github.com/atheme/atheme-contrib-modules.git'%g ./.gitmodules
    sed -i s%'url = git://github.com/atheme/atheme-contrib-modules.git'%'url = https://github.com/atheme/atheme-contrib-modules.git'%g ./.git/config
    sed -i s%'url = git://git.savannah.gnu.org/libunwind.git'%'url = https://git.savannah.gnu.org/git/libunwind.git'%g ./.gitmodules
    sed -i s%'url = git://git.savannah.gnu.org/libunwind.git'%'url = https://git.savannah.gnu.org/git/libunwind.git'%g ./.git/config
elif [ "$git_repo_link" == "https://github.com/luke-jr/bfgminer.git" ]; then
    sed -i s%'url = git://gitorious.org/bitcoin/libblkmaker.git'%'url = https://github.com/bitcoin/libblkmaker.git'%g ./.gitmodules
    sed -i s%'url = git://gitorious.org/bitcoin/libblkmaker.git'%'url = https://github.com/bitcoin/libblkmaker.git'%g ./.git/config
elif [ "$git_repo_link" == "git://git.qemu.org/qemu.git" ] || [ "$git_repo_link" == "https://github.com/qemu/qemu.git" ]; then
    sed -i s%'url = git://github.com/rth7680/qemu-palcode.git'%'url = https://github.com/rth7680/qemu-palcode.git'%g ./.gitmodules
    sed -i s%'url = git://github.com/rth7680/qemu-palcode.git'%'url = https://github.com/rth7680/qemu-palcode.git'%g ./.git/config
elif [ "$git_repo_link" == "https://gitlab.freedesktop.org/spice/spice.git" ]; then
    sed -i s%'url = ../spice-common'%'url = https://gitlab.freedesktop.org/spice/spice-common.git'%g ./.gitmodules
    sed -i s%'url = ../spice-common'%'url = https://gitlab.freedesktop.org/spice/spice-common.git'%g ./.git/config
fi
git submodule update --init

extra_flags=""

if [ "$git_repo_link" == "git://anongit.mindrot.org/openssh.git" ] || [ "$git_repo_link" == "https://github.com/openssh/openssh-portable.git" ]; then
    extra_flags="--without-openssl-header-check"
elif [ "$git_repo_link" == "git://git.qemu.org/qemu.git" ] || [ "$git_repo_link" == "https://github.com/qemu/qemu.git" ]; then
    extra_flags="--disable-werror"
elif [ "$git_repo_link" == "git://git.exim.org/exim.git" ] || [ "$git_repo_link" == "https://github.com/krb5/krb5.git" ] || [ "$git_repo_link" == "https://github.com/Exim/exim.git" ] || [ "$git_repo_link" == "git://git.savannah.gnu.org/screen.git" ] || [ "$git_repo_link" == "https://github.com/veracrypt/VeraCrypt.git" ]; then
    cd src
elif [ "$git_repo_link" == "git://git.altlinux.org/people/ldv/packages/pam.git" ]; then
    cd "Linux-PAM"
elif [ "$git_repo_link" == "https://github.com/kyz/libmspack.git" ]; then
    cd libmspack
elif [ "$git_repo_link" == "https://github.com/iortcw/iortcw.git" ]; then
    cd MP
elif [ "$git_repo_link" == "https://github.com/pediapress/pyfribidi.git" ]; then
    cd fribidi-src
elif [ "$git_repo_link" == "https://github.com/illumos/illumos-gate.git" ]; then
    cd usr/src
elif [ "$git_repo_link" == "https://github.com/libexpat/libexpat.git" ]; then
    cd expat
elif [ "$git_repo_link" == "https://github.com/rpm-software-management/libcomps.git" ]; then
    cd libcomps
elif [ "$git_repo_link" == "https://github.com/plougher/squashfs-tools.git" ]; then
    cd squashfs-tools
elif [ "$git_repo_link" == "https://github.com/systemd/systemd.git" ]; then
    extra_flags="--sysconfdir=/etc --localstatedir=/var --libdir=/usr/lib --libexecdir=/usr/lib"
elif [ "$git_repo_link" == "git://git.gnupg.org/gnupg.git" ]; then
    extra_flags="--sysconfdir=/etc --enable-maintainer-mode --enable-symcryptrun --enable-mailto --enable-gpgtar"
elif [ "$git_repo_link" == "git://git.gnupg.org/libgcrypt.git" ]; then
    extra_flags="--enable-maintainer-mode"
elif [ "$git_repo_link" == "https://github.com/OISF/suricata.git" ] || [ "$git_repo_link" == "https://github.com/inliniac/suricata.git" ]; then
    extra_flags="--enable-non-bundled-htp"
elif [ "$git_repo_link" == "https://github.com/abrt/abrt.git" ]; then
    extra_flags="--without-pythontests"
elif [ "$git_repo_link" == "https://github.com/uriparser/uriparser.git" ]; then
    extra_flags="--disable-test"
elif [ "$git_repo_link" == "https://github.com/appneta/tcpreplay.git" ]; then
    extra_flags="--disable-local-libopts"
elif [ "$git_repo_link" == "https://github.com/apache/httpd.git" ]; then
    svn co http://svn.apache.org/repos/asf/apr/apr/branches/1.8.x srclib/apr
    svn co http://svn.apache.org/repos/asf/apr/apr-util/branches/1.7.x srclib/apr-util
    extra_flags="--with-included-apr"
elif [ "$git_repo_link" == "git://git.postgresql.org/git/postgresql.git" ] || [ "$git_repo_link" == "https://github.com/postgres/postgres.git" ]; then
    extra_flags="--disable-thread-safety"
elif [ "$git_repo_link" == "https://github.com/GNOME/gimp.git" ]; then
    extra_flags="--disable-python"
elif [ "$git_repo_link" == "https://github.com/rpm-software-management/rpm.git" ]; then
    extra_flags="--without-lua"
elif [ "$git_repo_link" == "https://gitlab.com/openconnect/openconnect.git" ]; then
    extra_flags="--with-vpnc-script=/etc/vpnc/vpnc-script"
elif [ "$git_repo_link" == "https://github.com/TeX-Live/texlive-source.git" ]; then
    extra_flags="--enable-build-in-source-tree"
elif [ "$git_repo_link" == "https://gitlab.freedesktop.org/spice/libcacard.git" ]; then
    extra_flags="--disable-dependency-tracking"
elif [ "$git_repo_link" == "git://git.samba.org/samba.git" ]; then
    extra_flags="--without-ad-dc"
fi

if test -f "bootstrap"; then
    ./bootstrap
fi

configured=0
cmake=0
build_dir_name=""

if test -f "autogen.sh"; then
    echo "./autogen.sh found"
    # autoupdate -f
    chmod +x ./autogen.sh
    autoreconf -f -i
    ./autogen.sh
    if [ "$git_repo_link" == "https://github.com/unrealircd/unrealircd.git" ]; then
        HOSTCC="clang-11 -fuse-ld=lld -flto -O2" HOSTCXX="clang++-11 -fuse-ld=lld -flto -O2" \
        CC="clang-11 -fuse-ld=lld -flto -O2" CXX="clang++-11 -fuse-ld=lld -flto -O2" ./Config $extra_flags
    else
        HOSTCC="clang-11 -fuse-ld=lld -flto -O2" HOSTCXX="clang++-11 -fuse-ld=lld -flto -O2" \
        CC="clang-11 -fuse-ld=lld -flto -O2" CXX="clang++-11 -fuse-ld=lld -flto -O2" ./configure $extra_flags
    fi
    # check_error "ERROR: Failed to prepare for building"
    configured=1

elif test -f "regen.sh"; then
    echo "./regen.sh found"
    # autoupdate -f
    chmod +x ./regen.sh
    autoreconf -f -i
    ./regen.sh
    HOSTCC="clang-11 -fuse-ld=lld -flto -O2" HOSTCXX="clang++-11 -fuse-ld=lld -flto -O2" \
    CC="clang-11 -fuse-ld=lld -flto -O2" CXX="clang++-11 -fuse-ld=lld -flto -O2" ./configure $extra_flags
    # check_error "ERROR: Failed to prepare for building"
    configured=1

elif test -f "buildconf"; then
    echo "./buildconf found"
    # autoupdate -f
    chmod +x ./buildconf
    ./buildconf || ./buildconf --force
    rm aclocal.m4
    autoreconf -f -i
    HOSTCC="clang-11 -fuse-ld=lld -flto -O2" HOSTCXX="clang++-11 -fuse-ld=lld -flto -O2" \
    CC="clang-11 -fuse-ld=lld -flto -O2" CXX="clang++-11 -fuse-ld=lld -flto -O2" ./configure $extra_flags
    # check_error "ERROR: Failed to prepare for building"
    configured=1

elif test -f "CMakeLists.txt"; then
    echo "./CMakeLists.txt found"
    cmake --build . --target clean
    cmake --build build_dir --target clean
    if [ "$git_repo_link" == "git://git.launchpad.net/oxide" ] || [ "$git_repo_link" == "https://github.com/KDE/plasma-workspace.git" ]; then
        cmake -S . -B . -Wno-dev
        build_dir_name="."
        configured=0
    elif [ "$git_repo_link" == "https://github.com/domoticz/domoticz.git" ];then
        sed -i s/'SET(DOMO_MIN_LIBBOOST_VERSION 106000)'/'SET(DOMO_MIN_LIBBOOST_VERSION 1.71.0)'/g ./CMakeLists.txt
        HOSTCC="clang-11 -fuse-ld=lld -flto -O2" HOSTCXX="clang++-11 -fuse-ld=lld -flto -O2" \
        CC="clang-11 -fuse-ld=lld -flto -O2" CXX="clang++-11 -fuse-ld=lld -flto -O2" cmake -S . -B build_dir
        build_dir_name="./build_dir"
        configured=1
    # elif [ "$git_repo_link" == "https://github.com/DanBloomberg/leptonica.git" ]; then
    #     cmake -S . -B build_dir
    #     build_dir_name="./build_dir"
    #     configured=0
    else
        HOSTCC="clang-11 -fuse-ld=lld -flto -O2" HOSTCXX="clang++-11 -fuse-ld=lld -flto -O2" \
        CC="clang-11 -fuse-ld=lld -flto -O2" CXX="clang++-11 -fuse-ld=lld -flto -O2" cmake -S . -B build_dir
        build_dir_name="./build_dir"
        configured=1
    fi
    # check_error "ERROR: Failed to prepare for building"
    cmake=1
    
    cd "$build_dir_name"
elif test -f "SConstruct"; then
    echo "./SConstruct found"
elif test -f "meson.build"; then
    echo "./meson.build found"
    HOSTCC="clang-11 -fuse-ld=lld -flto -O2" HOSTCXX="clang++-11 -fuse-ld=lld -flto -O2" \
    CC="clang-11 -fuse-ld=lld -flto -O2" CXX="clang++-11 -fuse-ld=lld -flto -O2" meson setup build_dir # -Dc_args="-flto=thin -O2" -Dcpp_args="-flto=thin -O2"
    cd build_dir

elif [ -f "configure.ac" ] || [ -f "configure.in" ]; then
    echo "./configure.ac found"
    autoupdate -f
    autoreconf -f -i
    automake -a -f -c
    if [ "$git_repo_link" == "https://github.com/ImageMagick/librsvg.git" ]; then
        HOSTCC="clang-11 -fuse-ld=lld -flto -O2 -fdeclspec" HOSTCXX="clang++-11 -fuse-ld=lld -flto -O2 -fdeclspec" \
        CC="clang-11 -fuse-ld=lld -flto -O2 -fdeclspec" CXX="clang++-11 -fuse-ld=lld -flto -O2 -fdeclspec" ./configure $extra_flags
        # check_error "ERROR: Failed to prepare for building"
    else
        HOSTCC="clang-11 -fuse-ld=lld -flto -O2" HOSTCXX="clang++-11 -fuse-ld=lld -flto -O2" \
        CC="clang-11 -fuse-ld=lld -flto -O2" CXX="clang++-11 -fuse-ld=lld -flto -O2" ./configure $extra_flags
        # check_error "ERROR: Failed to prepare for building"
    fi
    configured=1
    # fi

elif test -f "configure"; then
    echo "./configure found"
    chmod +x ./configure
    if [ "$git_repo_link" == "https://github.com/FFmpeg/FFmpeg.git" ]; then
        ./configure --cc="clang-11 -fuse-ld=lld -flto -O2" --cxx="clang++-11 -fuse-ld=lld -flto -O2" ||
        ./configure --cc="clang-11 -fuse-ld=lld -flto -O2"
        # check_error "ERROR: Failed to prepare for building"
        configured=1
    elif [ "$git_repo_link" == "https://github.com/libav/libav.git" ] || [ "$git_repo_link" == "git://git.libav.org/libav.git" ]; then
        ./configure --cc="clang-11 -fuse-ld=lld -flto -O2"
        # check_error "ERROR: Failed to prepare for building"
        configured=1
    elif [ "$git_repo_link" == "https://github.com/pornel/pngquant.git" ]; then
        ./configure
        # check_error "ERROR: Failed to prepare for building"
    else
        HOSTCC="clang-11 -fuse-ld=lld -flto -O2" HOSTCXX="clang++-11 -fuse-ld=lld -flto -O2" \
        CC="clang-11 -fuse-ld=lld -flto -O2" CXX="clang++-11 -fuse-ld=lld -flto -O2" ./configure $extra_flags
        # check_error "ERROR: Failed to prepare for building"
        configured=1
    fi

elif test -f "Configure"; then
    echo "./Configure found"
    chmod +x ./Configure
    if [ "$git_repo_link" == "git://git.openssl.org/openssl.git" ] || [ "$git_repo_link" == "https://github.com/openssl/openssl.git" ]; then
        sed -i s/'"linux-elf",  "gcc:-DL_ENDIAN -DTERMIO -O3 -fomit-frame-pointer -m486 -Wall::-D_REENTRANT:-ldl:BN_LLONG ${x86_gcc_des} ${x86_gcc_opts}:${x86_elf_asm}:dlfcn",'/'"linux-elf",  "clang-11 -flto -fuse-ld=lld:-DL_ENDIAN -DTERMIO -O3 -fomit-frame-pointer -mtune=i486 -Wall::-D_REENTRANT:-ldl:BN_LLONG ${x86_gcc_des} ${x86_gcc_opts}:${x86_elf_asm}:dlfcn",'/g ./Configure
        HOSTCC="clang-11 -fuse-ld=lld -flto -O2" HOSTCXX="clang++-11 -fuse-ld=lld -flto -O2" \
        CC="clang-11 -fuse-ld=lld -flto -O2" CXX="clang++-11 -fuse-ld=lld -flto -O2" ./config
    else
        HOSTCC="clang-11 -fuse-ld=lld -flto -O2" HOSTCXX="clang++-11 -fuse-ld=lld -flto -O2" \
        CC="clang-11 -fuse-ld=lld -flto -O2" CXX="clang++-11 -fuse-ld=lld -flto -O2" ./Configure $extra_flags
    fi
    configured=1
    # check_error "ERROR: Failed to prepare for building"

elif [ -f "Makefile" ] || [ -f "makefile" ]; then
    if [ -f "Kconfig" ] || [ "$git_repo_link" == "git://git.busybox.net/busybox.git" ]; then
        make CC="clang-11" LD="ld.lld-11" AR="llvm-ar-11" NM="llvm-nm-11" STRIP="llvm-strip-11" \
             OBJCOPY="llvm-objcopy-11" OBJDUMP="llvm-objdump-11" READELF="llvm-readelf-11" \
             HOSTCC="clang-11" HOSTCXX="clang++-11" HOSTAR="llvm-ar-11" HOSTLD="ld.lld-11" \
             CFLAGS="-flto -O2" CXXFLAGS="-flto -O2" defconfig
        # make defconfig HOSTCC="clang-11 -fuse-ld=lld -flto -O2" HOSTCXX="clang++-11 -fuse-ld=lld -flto -O2" \
        #                CC="clang-11 -fuse-ld=lld -flto -O2" CXX="clang++-11 -fuse-ld=lld -flto -O2"
    elif [ "$git_repo_link" == "git://git.exim.org/exim.git" ] || [ "$git_repo_link" == "https://github.com/Exim/exim.git" ]; then
        mkdir Local
        sed -i s/EXIM_USER=/EXIM_USER=$USER/g src/EDITME
        mv src/EDITME Local/Makefile
        mv exim_monitor/EDITME Local/eximon.conf
    fi
elif [ "$git_repo_link" == "https://github.com/miniupnp/miniupnp.git" ]; then
    for dir_name in `find -type d -name "mini*"`; do
        cd $dir_name
        make -i HOSTCC="clang-11 -fuse-ld=lld -flto -O2" HOSTCXX="clang++-11 -fuse-ld=lld -flto -O2" \
                CC="clang-11 -fuse-ld=lld -flto -O2" CXX="clang++-11 -fuse-ld=lld -flto -O2"
        cd ..
    done
elif [ "$git_repo_link" == "https://github.com/LawnGnome/php-radius.git" ] || [ "$git_repo_link" == "https://github.com/m6w6/ext-http.git" ]; then
    phpize
    HOSTCC="clang-11 -fuse-ld=lld -flto -O2" HOSTCXX="clang++-11 -fuse-ld=lld -flto -O2" \
    CC="clang-11 -fuse-ld=lld -flto -O2" CXX="clang++-11 -fuse-ld=lld -flto -O2" ./configure $extra_flags
    configured=1
elif [ "$git_repo_link" == "https://github.com/z3APA3A/3proxy.git" ]; then
    ln -s Makefile.Linux Makefile
elif [ "$git_repo_link" == "https://github.com/viabtc/viabtc_exchange_server.git" ]; then
    cd network
    make -i HOSTCC="clang-11 -fuse-ld=lld -flto -O2" HOSTCXX="clang++-11 -fuse-ld=lld -flto -O2" \
            CC="clang-11 -fuse-ld=lld -flto -O2" CXX="clang++-11 -fuse-ld=lld -flto -O2"
    cd ../utils
    make -i HOSTCC="clang-11 -fuse-ld=lld -flto -O2" HOSTCXX="clang++-11 -fuse-ld=lld -flto -O2" \
            CC="clang-11 -fuse-ld=lld -flto -O2" CXX="clang++-11 -fuse-ld=lld -flto -O2"
    cd ..
    ln -s makefile.inc Makefile
else
    echo "ERROR: ./autogen.sh NOT FOUND" >&2
    echo "ERROR: ./regen.sh NOT FOUND" >&2
    echo "ERROR: ./buildconf NOT FOUND" >&2
    echo "ERROR: ./CMakeLists.txt NOT FOUND" >&2
    echo "ERROR: ./SConstruct.txt NOT FOUND" >&2
    echo "ERROR: ./configure.ac NOT FOUND" >&2
    echo "ERROR: ./configure NOT FOUND" >&2
    echo "ERROR: ./Configure NOT FOUND" >&2
    echo "ERROR: ./Makefile NOT FOUND" >&2
    echo "ERROR: ./makefile NOT FOUND" >&2
    exit 1
fi
if [ -f "configure" ] || [ -f "Configure" ] || [ -d "CMakeFiles" ] || [ -f "Makefile" ] || [ -f "makefile" ]; then
    if [ "$git_repo_link" == "https://github.com/NagiosEnterprises/nagioscore.git" ]; then
        make all -i
    elif [ $configured -eq 1 ] && [ "$git_repo_link" != "https://github.com/netblue30/firejail.git" ] && [ "$git_repo_link" != "https://github.com/paulusmack/ppp.git" ] && [ "$git_repo_link" != "https://github.com/pingidentity/mod_auth_openidc.git" ] && [ "$git_repo_link" != "https://github.com/zmartzone/mod_auth_openidc.git" ] ; then
        make -i
    else
        if [ "$git_repo_link" == "http://git.haproxy.org/git/haproxy.git" ] || [ "$git_repo_link" == "http://git.haproxy.org/git/haproxy-1.5.git" ] || [ "$git_repo_link" == "http://git.haproxy.org/git/haproxy-1.8.git" ]; then
            make -i TARGET=generic \
                    HOSTCC="clang-11 -fuse-ld=lld -flto -O2" HOSTCXX="clang++-11 -fuse-ld=lld -flto -O2" \
                    CC="clang-11 -fuse-ld=lld -flto -O2" CXX="clang++-11 -fuse-ld=lld -flto -O2"
        elif [ -f "Kconfig" ] || [ "$git_repo_link" == "git://git.busybox.net/busybox.git" ]; then
            make CC="clang-11" LD="ld.lld-11" AR="llvm-ar-11" NM="llvm-nm-11" STRIP="llvm-strip-11" \
                 OBJCOPY="llvm-objcopy-11" OBJDUMP="llvm-objdump-11" READELF="llvm-readelf-11" \
                 HOSTCC="clang-11" HOSTCXX="clang++-11" HOSTAR="llvm-ar-11" HOSTLD="ld.lld-11" \
                 CFLAGS="-flto -O2" CXXFLAGS="-flto -O2" -i prepare
            make CC="clang-11" LD="ld.lld-11" AR="llvm-ar-11" NM="llvm-nm-11" STRIP="llvm-strip-11" \
                 OBJCOPY="llvm-objcopy-11" OBJDUMP="llvm-objdump-11" READELF="llvm-readelf-11" \
                 HOSTCC="clang-11" HOSTCXX="clang++-11" HOSTAR="llvm-ar-11" HOSTLD="ld.lld-11" \
                 CFLAGS="-flto -O2" CXXFLAGS="-flto -O2" -i
        elif [ "$git_repo_link" == "https://github.com/openbsd/src.git" ]; then
            make build -i HOSTCC="clang-11 -fuse-ld=lld -flto -O2" HOSTCXX="clang++-11 -fuse-ld=lld -flto -O2" \
                          CC="clang-11 -fuse-ld=lld -flto -O2" CXX="clang++-11 -fuse-ld=lld -flto -O2"
        else
            make -i HOSTCC="clang-11 -fuse-ld=lld -flto -O2" HOSTCXX="clang++-11 -fuse-ld=lld -flto -O2" \
                    CC="clang-11 -fuse-ld=lld -flto -O2" CXX="clang++-11 -fuse-ld=lld -flto -O2"
        fi
    fi

elif [ -f "SConstruct" ]; then
    sed -i s%"env=env.Clone()"%"env=env.Clone()\nenv['CC']='clang-11 -fuse-ld=lld -flto -O2'\nenv['CXX']='clang++-11 -fuse-ld=lld -flto -O2'"%g ./SConscript
    scons -i || python2 /usr/bin/scons -i
    
elif [ -f "meson.build" ]; then
    ninja

fi

check_error "ERROR: Failed to build"
echo "CWD: ${PWD}"
if [ "${PWD##*/}" == "build_dir" ]; then
    cd ..
fi
if [ "$git_repo_link" == "git://git.exim.org/exim.git" ] || [ "$git_repo_link" == "git://git.altlinux.org/people/ldv/packages/pam.git" ] || [ "$git_repo_link" == "https://github.com/krb5/krb5.git" ] || [ "$git_repo_link" == "https://github.com/kyz/libmspack.git" ] || [ "$git_repo_link" == "https://github.com/iortcw/iortcw.git" ] || [ "$git_repo_link" == "https://github.com/pediapress/pyfribidi.git" ] || [ "$git_repo_link" == "https://github.com/Exim/exim.git" ] || [ "$git_repo_link" == "git://git.savannah.gnu.org/screen.git" ] || [ "$git_repo_link" == "https://github.com/veracrypt/VeraCrypt.git" ] || [ "$git_repo_link" == "https://github.com/rpm-software-management/libcomps.git" ] || [ "$git_repo_link" == "https://github.com/libexpat/libexpat.git" ] || [ "$git_repo_link" == "https://github.com/plougher/squashfs-tools.git" ]; then
    cd ..
elif [ "$git_repo_link" == "https://github.com/illumos/illumos-gate.git" ]; then
    cd ../..
fi

if ! test -d "../../llvm_ir/$result_dir_name/$commit_sha"; then
    mkdir -p ../../llvm_ir/$result_dir_name/$commit_sha
fi

func_list=""
for func_name in ${@:5:args_num-4}; do
    if [ "$func_name" == "$5" ]; then
        func_list+="$func_name"
    else
        func_list+="\n$func_name"
    fi
    for o_file in `find ./ -name "*.o"`; do
        if grep "$func_name" "../../llvm_ir/$result_dir_name/$commit_sha/$func_name.ll" | grep -q "define"; then
            break
        else
            rm "../../llvm_ir/$result_dir_name/$commit_sha/$func_name.ll"
        fi
        llvm-extract-11 -S --func=$func_name -o="../../llvm_ir/$result_dir_name/$commit_sha/$func_name.ll" $o_file
    done
done
echo -e $func_list > function_list.txt
if ! [ "$(ls -A ../../llvm_ir/$result_dir_name/$commit_sha)" ]; then
    git clean -f -d
    make clean && make distclean || scons -c || python2 /usr/bin/scons -c
    if [ "$git_repo_link" == "https://github.com/miniupnp/miniupnp.git" ]; then
        for dir_name in `find -type d -name "mini*"`; do
            cd $dir_name
            make clean
            cd ..
        done
    fi
    if [ $cmake -eq 1 ]; then
        cmake --build $build_dir_name --target clean
    fi
    rm -rf ../../llvm_ir/$result_dir_name/$commit_sha
    echo "Error: NO IR Found"
    exit 1
fi
if ! test -d "../../cpg/$result_dir_name/$commit_sha"; then
    mkdir -p ../../cpg/$result_dir_name/$commit_sha
fi
llvm2cpg --output=$result_dir_name.cpg.bin.zip `find ../../llvm_ir/$result_dir_name/$commit_sha/ -name "*.ll"`
check_error "ERROR: llvm2cpg FAILED"
joern --script ../../parse_cpg.sc --params cpgFile=$result_dir_name.cpg.bin.zip,functionList=function_list.txt,outDir=../../cpg/$result_dir_name/$commit_sha
check_error "ERROR: joern FAILED"
rm -rf workspace
git clean -f -d