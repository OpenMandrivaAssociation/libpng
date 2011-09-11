%define major 15
%define libname	%mklibname png %{major} %{major}
%define develname %mklibname png -d
%define staticname %mklibname png -d -s

Summary:	A library of functions for manipulating PNG image format files
Name:		libpng
Version:	1.5.4
Release:	%mkrel 1
Epoch:		2
License:	zlib
Group:		System/Libraries
URL:		http://www.libpng.org/pub/png/libpng.html
Source0:	http://prdownloads.sourceforge.net/libpng/files/%{name}-%{version}.tar.xz
# (tpg) APNG support http://littlesvr.ca/apng/
# (tpg) http://hp.vector.co.jp/authors/VA013651/freeSoftware/apng.html
# (tpg) http://sourceforge.net/projects/libpng-apng/ <- use this one
Patch0:		http://downloads.sourceforge.net/libpng-apng/files/libpng-devel/%{version}/%{name}-%{version}-apng.patch.gz
Patch1:		libpng-1.5.4-cmake-fixes.patch
Patch2:		libpng-1.5.4-fix-cmake-files-libpath.patch
BuildRequires: 	zlib-devel
BuildRequires:	cmake

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
Obsoletes:	%{_lib}png3 < 2:1.2.46-2

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked with libpng.

%package -n %{develname}
Summary:	Development tools for programs to manipulate PNG image format files
Group:		Development/C
Requires:	%{libname} = %{epoch}:%{version}
Provides:	%{name}-devel = %{epoch}:%{version}-%{release}
Provides:	png-devel = %{epoch}:%{version}-%{release}
Obsoletes:	%{mklibname png 3 -d} < 1.2.30
Provides:	%mklibname png 3 -d

%description -n	%{develname}
The libpng-devel package contains the header files and libraries
necessary for developing programs using the PNG (Portable Network
Graphics) library.

If you want to develop programs which will manipulate PNG image format
files, you should install libpng-devel.  You'll also need to install the
libpng package.

%package -n %{staticname}
Summary:	Development static libraries
Group:		Development/C
Requires:	%{develname} = %{epoch}:%{version}
Provides:	%{name}-static-devel = %{epoch}:%{version}-%{release}
Provides:	png-static-devel = %{epoch}:%{version}-%{release}
Obsoletes:	%{mklibname png 3 -d -s} < 1.2.30
Provides:	%mklibname png 3 -d -s

%description -n	%{staticname}
Libpng development static libraries.

%package source
Summary:	Source code of %{name}
Group:		Development/C

%description source
This package contains the source code of %{name}.

%prep
%setup -q
%patch0 -p1 -b .apng
%patch1 -p0 -b .fix-symlink
%patch2 -p0 -b .fix-cmake-files-libpath

%build
export CFLAGS="%{optflags} -O3 -funroll-loops"
%cmake \
  -DPNG_SHARED:BOOL=ON \
  -DPNG_STATIC:BOOL=ON
%make

%install
rm -rf %{buildroot}
%makeinstall_std -C build

# die, die, die
rm -f %buildroot%_libdir/*.la

install -d %{buildroot}%{_prefix}/src/%{name}
cp -a *.c *.h %{buildroot}%{_prefix}/src/%{name}

#multiarch
%multiarch_binaries %{buildroot}%{_bindir}/libpng%{major}-config

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif


%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libpng%{major}.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%doc *.txt example.c README TODO CHANGES
%{_bindir}/libpng-config
%{_bindir}/libpng%{major}-config
%{_includedir}/*
%{_libdir}/libpng%{major}.so
%{_libdir}/libpng.so
%{_libdir}/libpng/libpng%{major}*.cmake
%{_libdir}/pkgconfig/libpng*.pc
%{_mandir}/man?/*
%multiarch %{multiarch_bindir}/libpng%{major}-config

%files -n %{staticname}
%defattr(-,root,root)
%{_libdir}/libpng.a
%{_libdir}/libpng%{major}.a

%files source
%defattr(-,root,root)
%{_prefix}/src/%{name}/
