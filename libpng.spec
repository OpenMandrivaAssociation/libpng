%define major 15
%define libname	%mklibname png %{major}
%define develname %mklibname png -d
%define	static	%mklibname -d -s png

%bcond_without	uclibc

Summary:	A library of functions for manipulating PNG image format files
Name:		libpng
Version:	1.5.13
Release:	2
Epoch:		2
License:	zlib
Group:		System/Libraries
URL:		http://www.libpng.org/pub/png/libpng.html
Source0:	http://prdownloads.sourceforge.net/libpng/files/%{name}-%{version}.tar.xz
# (tpg) APNG support http://littlesvr.ca/apng/
# (tpg) http://hp.vector.co.jp/authors/VA013651/freeSoftware/apng.html
# (tpg) http://sourceforge.net/projects/libpng-apng/ <- use this one
Patch0:		http://downloads.sourceforge.net/libpng-apng/files/libpng-devel/%{version}/%{name}-1.5.13-apng.patch.gz
Patch2:		libpng-1.5.4-fix-cmake-files-libpath.patch
Patch3:		libpng-1.5.13-fix-libdir-pkgconfig-lib64-conflict.diff
BuildRequires: 	zlib-devel
BuildRequires:	cmake >= 1:2.8.6-7
%if %{with uclibc}
BuildRequires:	uClibc-devel
%endif

%description
The libpng package contains a library of functions for creating and
manipulating PNG (Portable Network Graphics) image format files.  PNG is
a bit-mapped graphics format similar to the GIF format.  PNG was created to
replace the GIF format, since GIF uses a patented data compression
algorithm.

Libpng should be installed if you need to manipulate PNG format image
files.

%package -n	%{libname}
Summary:	A library of functions for manipulating PNG image format files
Group:		System/Libraries
%define	ouchie	%mklibname png %{major} %{major}
%rename		%{ouchie}

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked with libpng.

%package -n	%{develname}
Summary:	Development tools for programs to manipulate PNG image format files
Group:		Development/C
Requires:	%{libname} >= %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Provides:	png-devel = %{EVRD}

%description -n	%{develname}
The libpng-devel package contains the header files and libraries
necessary for developing programs using the PNG (Portable Network
Graphics) library.

If you want to develop programs which will manipulate PNG image format
files, you should install libpng-devel.  You'll also need to install the
libpng package.

%package -n	%{static}
Summary:	Static development library of %{name}
Group:		Development/C
Requires:	%{develname} = %{EVRD}
Provides:	png-static-devel

%description -n	%{static}
This package contains a static library for development using %{name}.

%package	source
Summary:	Source code of %{name}
Group:		Development/C
BuildArch:	noarch

%description	source
This package contains the source code of %{name}.

%prep
%setup -q
%patch0 -p1 -b .apng
%patch2 -p0 -b .fix-cmake-files-libpath
%patch3 -p1 -b .lib64~

%build
%if %{with uclibc}
export CONFIGURE_TOP=$PWD
mkdir -p uclibc
pushd uclibc
# building out of source by default with cmake is causing troubles if one
# wanna do several builds using the cmake macro, this needs to be fixed in
# cmake package, but we'll just do it the old autofoo way in stay for now..
%configure2_5x	CC="%{uclibc_cc}" \
		CFLAGS="%{uclibc_cflags}" \
		--disable-shared
%make
popd
%endif

%cmake	-DPNG_SHARED:BOOL=ON \
	-DPNG_STATIC:BOOL=ON \
	-DCMAKE_C_FLAGS_RELWITHDEBINFO="%{optflags} -Ofast -funroll-loops" \
	-DCMAKE_EXE_LINKER_FLAGS="%{ldflags}"
%make

%install
%makeinstall_std -C build

%if %{with uclibc}
install -m644 uclibc/.libs/libpng15.a -D %{buildroot}%{uclibc_root}%{_libdir}/libpng15.a
ln -s libpng15.a %{buildroot}%{uclibc_root}%{_libdir}/libpng.a
%endif

install -d %{buildroot}%{_prefix}/src/%{name}
cp -a *.c *.h %{buildroot}%{_prefix}/src/%{name}

%files -n %{libname}
%{_libdir}/libpng%{major}.so.%{major}*

%files -n %{develname}
%doc libpng-manual.txt example.c README TODO CHANGES
%{_bindir}/libpng-config
%{_bindir}/libpng%{major}-config
%{_includedir}/*
%{_libdir}/libpng%{major}.so
%{_libdir}/libpng.so
%{_libdir}/libpng/libpng%{major}*.cmake
%{_libdir}/pkgconfig/libpng*.pc
%{_mandir}/man?/*

%files -n %{static}
%{_libdir}/libpng.a
%{_libdir}/libpng15.a
%if %{with uclibc}
%{uclibc_root}%{_libdir}/libpng.a
%{uclibc_root}%{_libdir}/libpng15.a
%endif

%files source
%{_prefix}/src/%{name}/
