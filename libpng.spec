%define api 16
%define major 16
%define libname %mklibname png %{api} %{major}
%define devname %mklibname png -d
%define static %mklibname -d -s png

Summary:	A library of functions for manipulating PNG image format files
Name:		libpng
Epoch:		2
Version:	1.6.33
Release:	1
License:	zlib
Group:		System/Libraries
Url:		http://www.libpng.org/pub/png/libpng.html
Source0:	http://download.sourceforge.net/%{name}/%{name}-%{version}.tar.xz
# (tpg) APNG support http://littlesvr.ca/apng/
# (tpg) http://hp.vector.co.jp/authors/VA013651/freeSoftware/apng.html
# (tpg) http://sourceforge.net/projects/libpng-apng/ <- use this one
Patch0:		https://sourceforge.net/projects/apng/files/libpng/libpng16/libpng-%{version}-apng.patch.gz
BuildRequires:	pkgconfig(zlib)

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

%package -n %{devname}
Summary:	Development tools for programs to manipulate PNG image format files
Group:		Development/C
Requires:	%{libname} >= %{EVRD}
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

%package tools
Summary:	Tools for working with/fixing up PNG files
Group:		Development/Other

%description tools
Tools for working with/fixing up PNG files

%prep
%setup -q
%patch0 -p0

%build
# Do not use cmake, it is in bad shape in libpng -
# doesn't set symbol versions which are required by LSB
%configure --enable-static
%make

%install
%makeinstall_std

install -d %{buildroot}%{_prefix}/src/%{name}
cp -a *.c *.h %{buildroot}%{_prefix}/src/%{name}

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

%files source
%{_prefix}/src/%{name}/
