%define libname_orig libpng
%define major 3
%define libname	%mklibname png %{major}
%define develname %mklibname png -d
%define staticname %mklibname png -d -s

Summary:	A library of functions for manipulating PNG image format files
Name:		libpng
Version:	1.2.36
Release:	%mkrel 2
Epoch:		2
License:	zlib
Group:		System/Libraries
URL:		http://www.libpng.org/pub/png/libpng.html
Source:		http://prdownloads.sourceforge.net/libpng/%{name}-%{version}.tar.lzma
# (tpg) APNG support http://littlesvr.ca/apng/
# (tpg) http://hp.vector.co.jp/authors/VA013651/freeSoftware/apng.html
Patch0:		libpng-1.2.34-apng.patch
Patch1:		libpng-1.2.36-pngconf-setjmp.patch
BuildRequires: 	zlib-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
Provides:	%{libname_orig} = %{epoch}:%{version}-%{release}

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked with libpng.

%package -n %{develname}
Summary:	Development tools for programs to manipulate PNG image format files
Group:		Development/C
Requires:	%{libname} = %{epoch}:%{version}-%{release}
Requires:	zlib-devel
Provides:	%{libname_orig}-devel = %{epoch}:%{version}-%{release}
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
Requires:	%{develname} = %{epoch}:%{version}-%{release}
Requires:	zlib-devel
Provides:	%{libname_orig}-static-devel = %{epoch}:%{version}-%{release}
Provides:	png-static-devel = %{epoch}:%{version}-%{release}
Obsoletes:	%{mklibname png 3 -d -s} < 1.2.30
Provides:	%mklibname png 3 -d -s

%description -n	%{staticname}
Libpng development static libraries.

%package -n	%{libname_orig}-source
Summary:	Source code of %{libname_orig}
Group:		Development/C

%description -n	%{libname_orig}-source
This package contains the source code of %{libname_orig}.

%prep
%setup -q
%patch0 -p1 -b .apng
%patch1 -p0 -b .pngconf-setjmp

%build

%ifnarch %{ix86}
export CFLAGS="%{optflags} -DPNG_NO_MMX_CODE"
%else
export CFLAGS="%{optflags}"
%endif

./autogen.sh
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

install -d %{buildroot}%{_prefix}/src/%{libname_orig}
cp -a *.c *.h %{buildroot}%{_prefix}/src/%{libname_orig}

# remove unpackaged files
rm -rf %{buildroot}{%{_prefix}/man,%{_libdir}/lib*.la}

#multiarch
%multiarch_binaries %{buildroot}%{_bindir}/libpng12-config

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*
%{_libdir}/libpng12.so.*

%files -n %{develname}
%defattr(-,root,root)
%doc *.txt example.c README TODO CHANGES
%{_bindir}/libpng-config
%{_bindir}/libpng12-config
%multiarch %{multiarch_bindir}/libpng12-config
%{_includedir}/*
%{_libdir}/libpng12.so
%{_libdir}/libpng.so
%{_libdir}/pkgconfig/*
%{_mandir}/man?/*

%files -n %{staticname}
%defattr(-,root,root)
%{_libdir}/libpng*.a

%files -n %{libname_orig}-source
%defattr(-,root,root)
%{_prefix}/src/%{libname_orig}
