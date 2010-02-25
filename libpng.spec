%define libname_orig libpng
%define major 3
%define libname	%mklibname png %{major}
%define develname %mklibname png -d
%define staticname %mklibname png -d -s

%bcond_without	uclibc

Summary:	A library of functions for manipulating PNG image format files
Name:		libpng
Version:	1.2.43
Release:	%mkrel 1
Epoch:		2
License:	zlib
Group:		System/Libraries
URL:		http://www.libpng.org/pub/png/libpng.html
Source:		http://prdownloads.sourceforge.net/libpng/%{name}-%{version}.tar.xz
# (tpg) APNG support http://littlesvr.ca/apng/
# (tpg) http://hp.vector.co.jp/authors/VA013651/freeSoftware/apng.html
# (tpg) http://sourceforge.net/projects/libpng-apng/ <- use this one
Patch0:		libpng-1.2.43-apng.patch
Patch1:		libpng-1.2.36-pngconf-setjmp.patch
BuildRequires: 	zlib-devel
%if %{with uclibc}
BuildRequires:	uClibc-devel
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
Provides:	%{libname_orig} = %{epoch}:%{version}-%{release}

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked with libpng.

%package -n	%{develname}
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

%package -n	%{staticname}
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
./autogen.sh

%build
export CONFIGURE_TOP=`pwd`
%if %{with uclibc}
mkdir -p uclibc
cd uclibc
%configure2_5x	CC="%{uclibc_cc}" \
		CFLAGS="%{uclibc_cflags}" \
		--enable-shared=no \
		--enable-static=yes \
		--with-pic
%make
cd ..
%endif

mkdir -p shared
cd shared
CFLAGS="%{optflags} -O3 -funroll-loops" \
%configure2_5x	--with-pic
%make
cd ..

%check
make -C shared check

%install
rm -rf %{buildroot}
%makeinstall_std -C shared
%if %{with uclibc}
install -m644 uclibc/.libs/libpng12.a -D %{buildroot}%{uclibc_root}%{_libdir}/libpng12.a
ln -s libpng12.a %{buildroot}%{uclibc_root}%{_libdir}/libpng.a
%endif

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
%if %{with uclibc}
%{uclibc_root}%{_libdir}/libpng*.a
%endif

%files -n %{libname_orig}-source
%defattr(-,root,root)
%{_prefix}/src/%{libname_orig}


%changelog
* Thu Feb 25 2010 Oden Eriksson <oeriksson@mandriva.com> 2:1.2.43-1mdv2010.1
+ Revision: 511256
- 1.2.43

* Wed Feb 24 2010 Oden Eriksson <oeriksson@mandriva.com> 2:1.2.42-1mdv2010.1
+ Revision: 510653
- 1.2.42
- rediffed the apng patch

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - make uclibc file in %%files conditional (thx to Matthew Dawkins for noticing!)

* Sat Dec 05 2009 Per Øyvind Karlsen <peroyvind@mandriva.org> 2:1.2.41-2mdv2010.1
+ Revision: 473715
- build with -fPIC

* Sat Dec 05 2009 Funda Wang <fwang@mandriva.org> 2:1.2.41-1mdv2010.1
+ Revision: 473664
- new version 1.2.41

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - compile with '-O3 -funroll-loops' (as suggested by upstream)
    - don't pass -DPNG_NO_MMX_CODE, it's already handled automatically by configure
    - build static uclibc linked library

* Sun Sep 13 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 2:1.2.40-1mdv2010.0
+ Revision: 439029
- update to new version 1.2.40

* Sun Aug 30 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 2:1.2.39-1mdv2010.0
+ Revision: 422506
- update to new version 1.2.39
- update patch0

* Sat Jun 06 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 2:1.2.37-1mdv2010.0
+ Revision: 383290
- update to new version 1.2.37
- Patch0: new version of apng patch

* Fri May 08 2009 Funda Wang <fwang@mandriva.org> 2:1.2.36-2mdv2010.0
+ Revision: 373374
- raise rel
- New version 1.2.36
- rediff p1

* Thu Feb 19 2009 Oden Eriksson <oeriksson@mandriva.com> 2:1.2.35-1mdv2009.1
+ Revision: 342891
- 1.2.35

* Thu Dec 18 2008 Oden Eriksson <oeriksson@mandriva.com> 2:1.2.34-1mdv2009.1
+ Revision: 315702
- 1.2.34
- new P0

* Thu Dec 18 2008 Oden Eriksson <oeriksson@mandriva.com> 2:1.2.33-3mdv2009.1
+ Revision: 315590
- rebuild

* Wed Nov 05 2008 Oden Eriksson <oeriksson@mandriva.com> 2:1.2.33-2mdv2009.1
+ Revision: 300156
- added P1 to fix build problem with mysql-gui-tools-5.0r14

* Fri Oct 31 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 2:1.2.33-1mdv2009.1
+ Revision: 299045
- update to new version 1.2.33

* Sun Sep 21 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 2:1.2.32-1mdv2009.1
+ Revision: 286394
- update to noew version 1.2.32
- drop patch 1 as it is fixed upstream
- Patch0: new version

* Tue Sep 09 2008 Frederik Himpe <fhimpe@mandriva.org> 2:1.2.31-2mdv2009.0
+ Revision: 283256
- Add 1.2.31beta01 patch fixing buffer overflow CVE-2008-3964

* Sat Aug 23 2008 Funda Wang <fwang@mandriva.org> 2:1.2.31-1mdv2009.0
+ Revision: 275373
- update apng patch with archlinux

  + Tomasz Pawel Gajc <tpg@mandriva.org>
    - update to new version 1.2.31
    - update to new version 1.2.30
    - use lzma'd tarball from upstream

* Wed Aug 06 2008 Thierry Vignaud <tvignaud@mandriva.org> 2:1.2.29-2mdv2009.0
+ Revision: 264888
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Thu May 08 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 2:1.2.29-1mdv2009.0
+ Revision: 204605
- new version

* Fri May 02 2008 Frederik Himpe <fhimpe@mandriva.org> 2:1.2.28-1mdv2009.0
+ Revision: 200472
- New upstream version (fixes security issues)
- Run ./autogen.sh, like Debian is doing, otherwise it does not build
- Update apng patch to version which applies without problem, from
  SourceMage

* Tue Apr 15 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 2:1.2.25-3mdv2009.0
+ Revision: 193502
- update APNG patch

* Thu Feb 28 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 2:1.2.25-2mdv2008.1
+ Revision: 176548
- add support for APNG images, this is a mandatory for upcoming Firefox 3

* Tue Feb 19 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 2:1.2.25-1mdv2008.1
+ Revision: 172842
- new version
- remove docs from static library

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Wed Dec 26 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 2:1.2.24-1mdv2008.1
+ Revision: 137841
- new version
- new license policy

  + Thierry Vignaud <tvignaud@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Nov 09 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 2:1.2.23-1mdv2008.1
+ Revision: 107203
- new version
- be more consistant on macros naming
- fix mixture of tabs and spaces
- some mino cleans in a spec file

* Sun Oct 14 2007 Funda Wang <fwang@mandriva.org> 2:1.2.22-1mdv2008.1
+ Revision: 98137
- New version 1.2.22

* Thu Oct 11 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 2:1.2.22-0.rc1.1mdv2008.1
+ Revision: 97198
- update to 1.2.22rc1 to close bug #34647

* Wed Oct 10 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 2:1.2.21-1mdv2008.1
+ Revision: 96614
- drop patch 0 and 1 since there is a configure script in use, which take care of everything
- remove dead entries in spec file
- let's see how libpng will work with mmx support on ix86
- new version
- new version

* Sat Aug 25 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 2:1.2.19-2mdv2008.0
+ Revision: 71324
- remove wrong obsoletes

* Sat Aug 25 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 2:1.2.19-1mdv2008.0
+ Revision: 71212
- export -DPNG_NO_MMX_CODE for x86_64 arch
- correct requires and provides
- rediff patch 0
- new devel library policy
- drop patch 2 (there is better way)
- new version

* Mon Aug 06 2007 David Walluck <walluck@mandriva.org> 2:1.2.18-3mdv2008.0
+ Revision: 59535
- move %%{_mandir}/man5/* to devel package in order to avoid multiarch conflict

* Mon Jul 02 2007 Olivier Blin <oblin@mandriva.com> 2:1.2.18-2mdv2008.0
+ Revision: 47129
- add a libpng-source package (to be used for software rebuilding libpng, such as syslinux)
- remove obsolete conflicts

* Wed May 16 2007 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2:1.2.18-1mdv2008.0
+ Revision: 27297
- Updated to 1.2.18.

* Fri Apr 20 2007 Olivier Blin <oblin@mandriva.com> 2:1.2.16-1mdv
+ Revision: 16258
- 1.2.16


* Sun Feb 18 2007 Götz Waschk <waschk@mandriva.org> 1.2.13-2mdv2007.0
+ Revision: 122407
- fix buildrequires

* Fri Nov 17 2006 Olivier Blin <oblin@mandriva.com> 2:1.2.13-1mdv2007.1
+ Revision: 85128
- 1.2.13

* Tue Oct 31 2006 Oden Eriksson <oeriksson@mandriva.com> 2:1.2.12-5mdv2007.1
+ Revision: 74600
- rebuild
- bzip2 cleanup
- rebuild

* Thu Oct 12 2006 Oden Eriksson <oeriksson@mandriva.com> 2:1.2.12-3mdv2007.1
+ Revision: 63449
- bunzip patches
- Import libpng

* Thu Aug 03 2006 Gwenole Beauchesne <gbeauchesne@mandriva.com> 1.2.12-2mdv2007.0
- Drop broken x86_64 patches (including from #23692). Time to be spent
  for making the MMX code 64-bit safe is the same as writing correct
  SSE2+ code. And, without proper data for validating semantics and
  performance, this currently is not worth the effort for MDV2007.0
- Henceforth, make sure to enable MMX optimisations on 32-bit x86
  platforms only (Patch2)

* Sun Jul 02 2006 Giuseppe Ghib� <ghibo@mandriva.com> 1.2.12-1mdv2007.0
- Release 1.2.12.
- Added Patch2 from Alex Simon to allow Assembler support in pnggccrd.c
  (needs Gwenole review), to allow ImageMagick 6.2.8.1 building on X86-64.

* Sun Jun 18 2006 Warly <warly@mandriva.com>  1.2.10-4mdv2007.0
- This seem to be a desired behavior, need to recompile the packages requiring the old devel(libpng)

* Sun Jun 18 2006 Warly <warly@mandriva.com>  1.2.10-3mdv2007.0
- also workarround the problem for x86_64

* Sat Jun 17 2006 Warly <warly@mandriva.com>  1.2.10-2mdv2007.0
- workarround the non providing of devel(libpng)

* Fri Jun 16 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 1.2.10-1mdv2007.0
- 1.2.10
- do configure
- %%mkrel
- regenerate P0 & P1
- move tests to new %%check stage
- multiarch

* Sun Jan 01 2006 Mandriva Linux Team <http://www.mandrivaexpert.com/> 1.2.8-2mdk
- Rebuild

* Wed Dec 22 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.2.8-1mdk
- 1.2.8
- fix summary-ended-with-dot

* Tue Nov 09 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 1.2.7-1mdk
- new release

* Fri Oct 01 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.2.6-2mdk
- lib64 fixes to pkgconfig files

* Wed Aug 18 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.2.6-1mdk
- new release
- fix url
- kill patch 1 (merged upstream)

* Fri Jun 18 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.2.5-11mdk
- security fix for CAN-2004-0421 (Vincent Danen)
- misc spec file fixes

