%define api	16
%define major	16
%define libname	%mklibname png %{api} %{major}
%define devname %mklibname png -d
%define	static	%mklibname -d -s png

%bcond_with	uclibc

Summary:	A library of functions for manipulating PNG image format files
Name:		libpng
Epoch:		2
Version:	1.6.2
Release:	2
License:	zlib
Group:		System/Libraries
Url:		http://www.libpng.org/pub/png/libpng.html
Source0:	http://garr.dl.sourceforge.net/project/libpng/libpng%{api}/%{version}/%{name}-%{version}.tar.xz
# (tpg) APNG support http://littlesvr.ca/apng/
# (tpg) http://hp.vector.co.jp/authors/VA013651/freeSoftware/apng.html
# (tpg) http://sourceforge.net/projects/libpng-apng/ <- use this one
Patch0:		http://garr.dl.sourceforge.net/project/libpng-apng/libpng%{api}/%{version}/libpng-%{version}-apng.patch.gz
Patch3:		libpng-1.6.2-fix-libdir-pkgconfig-lib64-conflict.diff

#BuildRequires:	cmake >= 1:2.8.6-7
BuildRequires:	pkgconfig(zlib)
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

%package -n %{libname}
Summary:	A library of functions for manipulating PNG image format files
Group:		System/Libraries

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked with libpng.

%if %{with uclibc}
%package -n uclibc-%{libname}
Summary:	A library of functions for manipulating PNG image format files
Group:		System/Libraries

%description -n	uclibc-%{libname}
This package contains the library needed to run programs dynamically
linked with libpng.
%endif

%package -n %{devname}
Summary:	Development tools for programs to manipulate PNG image format files
Group:		Development/C
Requires:	%{libname} >= %{EVRD}
%if %{with uclibc}
Requires:	uclibc-%{libname} >= %{EVRD}
%endif
Provides:	%{name}-devel = %{EVRD}
Provides:	png-devel = %{EVRD}
# FIXME this is not quite right, but will fix a great many builds...
%if "%_lib" == "lib64"
Provides:	devel(libpng15(64bit))
%else
Provides:	devel(libpng15)
%endif

%description -n	%{devname}
The libpng-devel package contains the header files and libraries
necessary for developing programs using the PNG (Portable Network
Graphics) library.

%package -n %{static}
Summary:	Static development library of %{name}
Group:		Development/C
Requires:	%{devname} = %{EVRD}
Provides:	png-static-devel

%description -n	%{static}
This package contains a static library for development using %{name}.

%package source
Summary:	Source code of %{name}
Group:		Development/C
BuildArch:	noarch

%description source
This package contains the source code of %{name}.

%prep
%setup -q
%apply_patches

%build
%if %{with uclibc}
export CONFIGURE_TOP=$PWD
mkdir -p uclibc
pushd uclibc
# building out of source by default with cmake is causing troubles if one
# wanna do several builds using the cmake macro, this needs to be fixed in
# cmake package, but we'll just do it the old autofoo way in stay for now..
%uclibc_configure
%make
popd
%endif

# Do not use cmake, it is in bad shape in libpng -
# doesn't set symbol versions which are required by LSB
%configure2_5x
%make

%install
%if %{with uclibc}
%makeinstall_std -C uclibc
rm -r %{buildroot}%{uclibc_root}%{_libdir}/pkgconfig
rm -r %{buildroot}%{uclibc_root}%{_bindir}
%endif

%makeinstall_std 
#-C build

install -d %{buildroot}%{_prefix}/src/%{name}
cp -a *.c *.h %{buildroot}%{_prefix}/src/%{name}

%files -n %{libname}
%{_libdir}/libpng%{api}.so.%{major}*

%if %{with uclibc}
%files -n uclibc-%{libname}
%{uclibc_root}%{_libdir}/libpng%{api}.so.%{major}*
%endif

%files -n %{devname}
%doc libpng-manual.txt example.c README TODO CHANGES
%{_bindir}/libpng-config
%{_bindir}/libpng%{api}-config
%{_includedir}/*
%{_libdir}/libpng%{api}.so
%{_libdir}/libpng.so
%if %{with uclibc}
%{uclibc_root}%{_libdir}/libpng%{api}.so
%{uclibc_root}%{_libdir}/libpng.so
%endif
#%{_libdir}/libpng/libpng%{api}*.cmake
%{_libdir}/pkgconfig/libpng*.pc
%{_mandir}/man?/*

%files -n %{static}
%{_libdir}/libpng.a
%{_libdir}/libpng%{api}.a
%if %{with uclibc}
%{uclibc_root}%{_libdir}/libpng.a
%{uclibc_root}%{_libdir}/libpng%{api}.a
%endif

%files source
%{_prefix}/src/%{name}/

