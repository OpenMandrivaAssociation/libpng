# The 32-bit library is needed by wine.

%define api 16
%define major 16
%define libname %mklibname png %{api} %{major}
%define lib32name libpng%{api}_%{major}
%define devname %mklibname png -d
%define dev32name libpng-devel
%define static %mklibname -d -s png

%global optflags %{optflags} -O3 -DPIC -fPIC -DPNG_SAFE_LIMITS_SUPPORTED -DPNG_SKIP_SETJMP_CHECK

# PGO causes bootstrapping problems (PGO requires imagemagick
# to get some libpng usage - imagemagick requires libpng).
# Disable PGO while bootstrapping.
%ifarch %{riscv}
%bcond_with pgo
%else
%bcond_without pgo
%endif

Summary:	A library of functions for manipulating PNG image format files
Name:		libpng
Version:	1.6.37
Release:	4
License:	zlib
Group:		System/Libraries
Url:		http://www.libpng.org/pub/png/libpng.html
Source0:	http://download.sourceforge.net/%{name}/%{name}-%{version}.tar.xz
# (tpg) APNG support http://littlesvr.ca/apng/
# (tpg) http://hp.vector.co.jp/authors/VA013651/freeSoftware/apng.html
# (tpg) http://sourceforge.net/projects/libpng-apng/ <- use this one
Patch0:		https://sourceforge.net/projects/apng/files/libpng/libpng16/libpng-%{version}-apng.patch.gz

BuildRequires:	pkgconfig(zlib)
%ifarch %{x86_64}
BuildRequires:	devel(libz)
%endif
%if %{with pgo}
BuildRequires:	imagemagick
BuildRequires:	openmandriva-kde-icons
BuildRequires:	oxygen-icons
%endif

%description
The libpng package contains a library of functions for creating and
manipulating PNG (Portable Network Graphics) image format files.  PNG is
a bit-mapped graphics format similar to the GIF format.  PNG was created to
replace the GIF format, since GIF uses a patented data compression
algorithm.

Libpng should be installed if you need to manipulate PNG format image
files.

%package -n %{libname}
Summary:	A library of functions for manipulating PNG image format files
Group:		System/Libraries

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with libpng.

%package -n %{devname}
Summary:	Development tools for programs to manipulate PNG image format files
Group:		Development/C
Requires:	%{libname} >= %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Provides:	png-devel = %{EVRD}

%description -n %{devname}
The libpng-devel package contains the header files and libraries
necessary for developing programs using the PNG (Portable Network
Graphics) library.

%ifarch %{x86_64}
%package -n %{lib32name}
Summary:	A library of functions for manipulating PNG image format files (32-bit)
Group:		System/Libraries

%description -n %{lib32name}
This package contains the library needed to run programs dynamically
linked with libpng.

%package -n %{dev32name}
Summary:	Development tools for programs to manipulate PNG image format files (32-bit)
Group:		Development/C
Requires:	%{lib32name} = %{EVRD}
Requires:	%{devname} = %{EVRD}

%description -n %{dev32name}
The libpng-devel package contains the header files and libraries
necessary for developing programs using the PNG (Portable Network
Graphics) library.
%endif

%package -n %{static}
Summary:	Static development library of %{name}
Group:		Development/C
Requires:	%{devname} = %{EVRD}
Provides:	png-static-devel

%description -n %{static}
This package contains a static library for development using %{name}.

%package tools
Summary:	Tools for working with/fixing up PNG files
Group:		Development/Other

%description tools
Tools for working with/fixing up PNG files

%prep
%autosetup -p0

autoreconf -fiv

%ifarch %{x86_64}
CONFIGURE_TOP=$(pwd)
mkdir build32
cd build32
%configure32
%endif

%build
# Do not use cmake, it is in bad shape in libpng -
# doesn't set symbol versions which are required by LSB

%ifarch %{x86_64}
cd build32
%make_build
cd ..
%endif

CONFIGURE_TOP=$(pwd)
mkdir build
cd build
%if %{with pgo}
CFLAGS="%{optflags} -fprofile-instr-generate" \
CXXFLAGS="%{optflags} -fprofile-instr-generate" \
LDFLAGS="%{build_ldflags} -fprofile-instr-generate" \
%configure \
    --enable-hardware-optimizations=yes \
%ifarch aarch64
    --enable-arm-neon=check \
%endif
    --enable-static

%make_build

if ! [ -e .libs/libpng%{major}.so.%{major} ]; then
	echo "Build system changed -- please fix PGO assumptions about locations."
	exit 1
fi
export LLVM_PROFILE_FILE=libpng-%p.profile.d
export LD_LIBRARY_PATH="$(pwd)/.libs"
find %{_datadir}/icons/oxygen -iname "*.png" |while read r; do
	convert $r /tmp/test.bmp
	convert /tmp/test.bmp /tmp/test.png
	rm -f /tmp/test.bmp /tmp/test.png
done
unset LD_LIBRARY_PATH
unset LLVM_PROFILE_FILE
llvm-profdata merge --output=libpng.profile *.profile.d
rm -f *.profile.d

make clean

CFLAGS="%{optflags} -fprofile-instr-use=$(realpath libpng.profile)" \
CXXFLAGS="%{optflags} -fprofile-instr-use=$(realpath libpng.profile)" \
LDFLAGS="%{build_ldflags} -fprofile-instr-use=$(realpath libpng.profile)" \
%endif
%configure \
    --enable-hardware-optimizations=yes \
%ifarch aarch64
    --enable-arm-neon=check \
%endif
    --enable-static

%make_build

%install
%ifarch %{x86_64}
%make_install -C build32
%endif

%make_install -C build

%files -n %{libname}
%{_libdir}/libpng%{api}.so.%{major}*

%files -n %{devname}
%doc libpng-manual.txt example.c README TODO CHANGES
%{_bindir}/libpng-config
%{_bindir}/libpng%{api}-config
%{_includedir}/*
%{_libdir}/libpng%{api}.so
%{_libdir}/libpng.so
%{_libdir}/pkgconfig/libpng*.pc
%{_mandir}/man?/*

%files -n %{static}
%{_libdir}/libpng.a
%{_libdir}/libpng%{api}.a

%files tools
%{_bindir}/pngfix
%{_bindir}/png-fix-itxt

%ifarch %{x86_64}
%files -n %{lib32name}
%{_prefix}/lib/libpng16.so.*

%files -n %{dev32name}
%{_prefix}/lib/*.so
%{_prefix}/lib/pkgconfig/*.pc
%endif
