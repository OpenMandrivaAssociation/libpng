%define major 15
%define libname	%mklibname png %{major}
%define develname %mklibname png -d
%define	static	%mklibname -d -s png

%bcond_without	uclibc

Summary:	A library of functions for manipulating PNG image format files
Name:		libpng
Version:	1.5.14
Release:	1
Epoch:		2
License:	zlib
Group:		System/Libraries
URL:		http://www.libpng.org/pub/png/libpng.html
Source0:	http://prdownloads.sourceforge.net/libpng/files/%{name}-%{version}.tar.xz
# (tpg) APNG support http://littlesvr.ca/apng/
# (tpg) http://hp.vector.co.jp/authors/VA013651/freeSoftware/apng.html
# (tpg) http://sourceforge.net/projects/libpng-apng/ <- use this one
Patch0:		http://downloads.sourceforge.net/libpng-apng/files/libpng-devel/%{version}/%{name}-1.5.14-apng.patch.gz
Patch2:		libpng-1.5.4-fix-cmake-files-libpath.patch
Patch3:		libpng-1.5.13-fix-libdir-pkgconfig-lib64-conflict.diff
Patch4:		libpng-fpic-cmake.patch
BuildRequires:	zlib-devel
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

%package -n %{libname}
Summary:	A library of functions for manipulating PNG image format files
Group:		System/Libraries
%define	ouchie	%mklibname png %{major} %{major}
%rename		%{ouchie}

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

%package -n %{develname}
Summary:	Development tools for programs to manipulate PNG image format files
Group:		Development/C
Requires:	%{libname} >= %{EVRD}
%if %{with uclibc}
Requires:	uclibc-%{libname} >= %{EVRD}
%endif
Provides:	%{name}-devel = %{EVRD}
Provides:	png-devel = %{EVRD}

%description -n	%{develname}
The libpng-devel package contains the header files and libraries
necessary for developing programs using the PNG (Portable Network
Graphics) library.

If you want to develop programs which will manipulate PNG image format
files, you should install libpng-devel.  You'll also need to install the
libpng package.

%package -n %{static}
Summary:	Static development library of %{name}
Group:		Development/C
Requires:	%{develname} = %{EVRD}
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
%patch0 -p1 -b .apng
%patch2 -p0 -b .fix-cmake-files-libpath
%patch3 -p1 -b .lib64~
%patch4 -p1 -b .fpic

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
which gcc
%cmake	-DPNG_SHARED:BOOL=ON \
	-DPNG_STATIC:BOOL=ON \
	-DCMAKE_C_FLAGS_RELWITHDEBINFO="%{optflags} -Ofast -funroll-loops" \
	-DCMAKE_EXE_LINKER_FLAGS="%{ldflags}"
%make

%install
%if %{with uclibc}
%makeinstall_std -C uclibc
rm -r %{buildroot}%{uclibc_root}%{_libdir}/pkgconfig
rm -r %{buildroot}%{uclibc_root}%{_bindir}
%endif

%makeinstall_std -C build

install -d %{buildroot}%{_prefix}/src/%{name}
cp -a *.c *.h %{buildroot}%{_prefix}/src/%{name}

%files -n %{libname}
%{_libdir}/libpng%{major}.so.%{major}*

%if %{with uclibc}
%files -n uclibc-%{libname}
%{uclibc_root}%{_libdir}/libpng%{major}.so.%{major}*
%endif

%files -n %{develname}
%doc libpng-manual.txt example.c README TODO CHANGES
%{_bindir}/libpng-config
%{_bindir}/libpng%{major}-config
%{_includedir}/*
%{_libdir}/libpng%{major}.so
%{_libdir}/libpng.so
%if %{with uclibc}
%{uclibc_root}%{_libdir}/libpng%{major}.so
%{uclibc_root}%{_libdir}/libpng.so
%endif
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

%changelog
* Wed Dec 12 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.5.13-1
- make source package noarch
- update pkgconfig patch
- add back uclibc build
- add back static build of library
- libpng cmake file ignores standard variables for setting cflags & ldflags, so
  pass these with the variables it uses

  + Tomasz Pawel Gajc <tpg@mandriva.org>
    - update to new version 1.5.13

* Fri Jul 13 2012 Oden Eriksson <oeriksson@mandriva.com>1.5.12-1
+ Revision: 809163
- 1.5.12

* Sat Jun 16 2012 Oden Eriksson <oeriksson@mandriva.com>1.5.11-1
+ Revision: 805997
- rediff
- 1.5.11

* Fri Mar 30 2012 Oden Eriksson <oeriksson@mandriva.com>1.5.10-1
+ Revision: 788398
- new apng patch
- fix one patch
- 1.5.10

* Sun Feb 19 2012 Oden Eriksson <oeriksson@mandriva.com>1.5.9-1
+ Revision: 777386
- 1.5.9

* Sat Feb 04 2012 Oden Eriksson <oeriksson@mandriva.com>1.5.8-1
+ Revision: 771164
- 1.5.8 (fixes CVE-2011-3464)
- rediffed some patches

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - add a versioned build dependency on latest cmake and stop messing with
      CMAKE_BUILD_TYPE

* Tue Dec 20 2011 Z? <ze@mandriva.org>1.5.7-2
+ Revision: 743865
- set to Release mode to not change devel lib file, but needs to be set to Debug mode and rebuild all packages that need libpng, this is the proper way

* Sun Dec 18 2011 Oden Eriksson <oeriksson@mandriva.com>1.5.7-1
+ Revision: 743553
- 1.5.7

* Tue Dec 06 2011 Oden Eriksson <oeriksson@mandriva.com>1.5.6-2
+ Revision: 738311
- drop the static lib and its sub package

* Thu Nov 03 2011 Oden Eriksson <oeriksson@mandriva.com>1.5.6-1
+ Revision: 716269
- 1.5.6

* Wed Sep 28 2011 Oden Eriksson <oeriksson@mandriva.com>1.5.5-1
+ Revision: 701799
- 1.5.5

* Fri Sep 16 2011 Per Øyvind Karlsen <peroyvind@mandriva.org>1.5.4-6
+ Revision: 699938
- really fix file conflict..
- be more strict about what .txt files we include, so we don't ship with
  CMakeLists.txt as doc

* Thu Sep 15 2011 Per Øyvind Karlsen <peroyvind@mandriva.org>1.5.4-5
+ Revision: 699913
- fix pkgconfig lib64 conflict, avoiding %%multiarch hackage (P3)
- remove conflicts on older libpng devel packages

* Tue Sep 13 2011 Per Øyvind Karlsen <peroyvind@mandriva.org>1.5.4-4
+ Revision: 699666
- fix missing epoch in conflicts

* Tue Sep 13 2011 Per Øyvind Karlsen <peroyvind@mandriva.org>1.5.4-3
+ Revision: 699604
- fix so that -devel package can co-exist in repos with older version
- use %%{EVRD} macro

* Mon Sep 12 2011 Per Øyvind Karlsen <peroyvind@mandriva.org>1.5.4-2
+ Revision: 699438
- be sure to correct upgrade from incorrect package name due to duped major
- do some cleaning
- fix duplicate major in package name
- drop dangerous and incorrect obsoletes on older library package

* Sun Sep 11 2011 Z? <ze@mandriva.org>1.5.4-1
+ Revision: 699416
- version 1.5.4
- drop useless requires (already exist,no need to have them explict)
- drop useless provides
- set requires to version
- fix symlink
- fix .cmake files path
- fix source and patch URLs

* Thu Jul 21 2011 Oden Eriksson <oeriksson@mandriva.com>1.2.46-1
+ Revision: 690817
- 1.2.46

* Fri Apr 29 2011 Funda Wang <fwang@mandriva.org>1.2.44-3
+ Revision: 660654
- update multiarch usage

  + Oden Eriksson <oeriksson@mandriva.com>
    - mass rebuild

* Sat Aug 14 2010 Oden Eriksson <oeriksson@mandriva.com>1.2.44-2mdv2011.0
+ Revision: 569562
- sync with MDVSA-2010:133

* Fri Jul 09 2010 Funda Wang <fwang@mandriva.org>1.2.44-1mdv2011.0
+ Revision: 549888
- New version 1.2.44

  + Oden Eriksson <oeriksson@mandriva.com>
    - remove the changelog (how did that happen?)

* Thu Feb 25 2010 Oden Eriksson <oeriksson@mandriva.com>1.2.43-1mdv2010.1
+ Revision: 511259
- use a newer apng patch from upstream
- 1.2.43

* Wed Feb 24 2010 Oden Eriksson <oeriksson@mandriva.com>1.2.42-1mdv2010.1
+ Revision: 510653
- 1.2.42
- rediffed the apng patch

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - make uclibc file in %%files conditional (thx to Matthew Dawkins for noticing!)

* Sat Dec 05 2009 Per Øyvind Karlsen <peroyvind@mandriva.org>1.2.41-2mdv2010.1
+ Revision: 473715
- build with -fPIC

* Sat Dec 05 2009 Funda Wang <fwang@mandriva.org>1.2.41-1mdv2010.1
+ Revision: 473664
- new version 1.2.41

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - compile with '-O3 -funroll-loops' (as suggested by upstream)
    - don't pass -DPNG_NO_MMX_CODE, it's already handled automatically by configure
    - build static uclibc linked library

* Sun Sep 13 2009 Tomasz Pawel Gajc <tpg@mandriva.org>1.2.40-1mdv2010.0
+ Revision: 439029
- update to new version 1.2.40

* Sun Aug 30 2009 Tomasz Pawel Gajc <tpg@mandriva.org>1.2.39-1mdv2010.0
+ Revision: 422506
- update to new version 1.2.39
- update patch0

