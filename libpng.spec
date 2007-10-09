%define lib_name_orig	libpng
%define major		3
%define lib_name	%mklibname png %{major}
%define lib_devel	%mklibname png -d
%define lib_static	%mklibname png -d -s

Summary: 	A library of functions for manipulating PNG image format files
Name: 		libpng
Version: 	1.2.21
Release:	%mkrel 1
License: 	GPL-like
Group: 		System/Libraries
BuildRequires: 	zlib-devel
URL: 		http://www.libpng.org/pub/png/libpng.html
Source: 	http://prdownloads.sourceforge.net/libpng/%{name}-%{version}.tar.bz2
Patch0:		libpng-1.2.19-makefile.patch
Patch1:		libpng-1.2.10-lib64.patch
Epoch: 		2
Buildroot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The libpng package contains a library of functions for creating and
manipulating PNG (Portable Network Graphics) image format files.  PNG is
a bit-mapped graphics format similar to the GIF format.  PNG was created to
replace the GIF format, since GIF uses a patented data compression
algorithm.

Libpng should be installed if you need to manipulate PNG format image
files.

%package -n	%{lib_name}
Summary:	A library of functions for manipulating PNG image format files
Group:		System/Libraries
Obsoletes:	%{lib_name_orig}
Provides:	%{lib_name_orig} = %{epoch}:%{version}-%{release}

%description -n	%{lib_name}
This package contains the library needed to run programs dynamically
linked with libpng.

%package -n	%{lib_devel}
Summary:	Development tools for programs to manipulate PNG image format files
Group:		Development/C
Requires:	%{lib_name} = %{epoch}:%{version}-%{release}
Requires:	zlib-devel
Provides:	%{lib_name_orig}-devel = %{epoch}:%{version}-%{release}
Provides:	png-devel = %{epoch}:%{version}-%{release}
Obsoletes:	%mklibname png 3 -d
Provides:	%mklibname png 3 -d

%description -n	%{lib_devel}
The libpng-devel package contains the header files and libraries
necessary for developing programs using the PNG (Portable Network
Graphics) library.

If you want to develop programs which will manipulate PNG image format
files, you should install libpng-devel.  You'll also need to install the
libpng package.

%package -n	%{lib_static}
Summary:	Development static libraries
Group:		Development/C
Requires:	%{lib_name_orig}-devel = %{epoch}:%{version}-%{release}
Requires:	zlib-devel
Provides:	%{lib_name_orig}-static-devel = %{epoch}:%{version}-%{release}
Provides:	png-static-devel = %{epoch}:%{version}-%{release}
Obsoletes:	%mklibname png 3 -d -s
Provides:	%mklibname png 3 -d -s

%description -n	%{lib_static}
Libpng development static libraries.

%package -n	%{lib_name_orig}-source
Summary:	Source code of %{lib_name_orig}
Group:		Development/C

%description -n	%{lib_name_orig}-source
This package contains the source code of %{lib_name_orig}.

%prep
%setup -q
%patch0 -p1 -b .makefile
%patch1 -p1 -b .lib64

perl -pi -e 's|^prefix=.*|prefix=%{_prefix}|' scripts/makefile.linux
perl -pi -e 's|^(LIBPATH=.*)/lib\b|\1/%{_lib}|' scripts/makefile.linux
ln -s scripts/makefile.linux ./Makefile

%build
%ifarch ix86
ln -sf scripts/makefile.gcmmx ./Makefile
%else
ln -sf scripts/makefile.linux ./Makefile
%endif

%ifnarch ix86
export CFLAGS="%{optflags} -DPNG_NO_MMX_CODE"
%else
export CFLAGS="%{optflags}"
%endif

%configure2_5x
%make

%check
make check

%install
rm -rf %{buildroot}
%makeinstall_std

install -d %{buildroot}%{_mandir}/man{3,5}
install -m0644 {libpng,libpngpf}.3 %{buildroot}%{_mandir}/man3
install -m0644 png.5 %{buildroot}%{_mandir}/man5/png3.5

install -d %{buildroot}%{_prefix}/src/%{lib_name_orig}
cp -a *.c *.h %{buildroot}%{_prefix}/src/%{lib_name_orig}

# remove unpackaged files
rm -rf %{buildroot}{%{_prefix}/man,%{_libdir}/lib*.la}

#multiarch
%multiarch_binaries %{buildroot}%{_bindir}/libpng12-config

%post -n %{lib_name} -p /sbin/ldconfig

%postun -n %{lib_name} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files -n %{lib_name}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*
%{_libdir}/libpng12.so.*

%files -n %{lib_devel}
%defattr(-,root,root)
%doc *.txt example.c README TODO CHANGES
%{_bindir}/libpng-config
%{_bindir}/libpng12-config
%multiarch %{multiarch_bindir}/libpng12-config
%{_includedir}/*
%{_libdir}/libpng12.so
%{_libdir}/libpng.so
%{_libdir}/pkgconfig/*
%{_mandir}/man3/*
%{_mandir}/man5/*

%files -n %{lib_static}
%defattr(-,root,root)
%doc README
%{_libdir}/libpng*.a

%files -n %{lib_name_orig}-source
%defattr(-,root,root)
%{_prefix}/src/%{lib_name_orig}
