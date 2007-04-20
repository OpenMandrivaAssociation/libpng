%define lib_name_orig	libpng
%define lib_major	3
%define lib_name	%mklibname png %{lib_major}

Summary: 	A library of functions for manipulating PNG image format files
Name: 		libpng
Version: 	1.2.16
Release:	%mkrel 1
License: 	GPL-like
Group: 		System/Libraries
BuildRequires: 	zlib-devel
URL: 		http://www.libpng.org/pub/png/libpng.html
Source: 	http://prdownloads.sourceforge.net/libpng/%{name}-%{version}.tar.bz2
Patch0:		libpng-1.2.10-mdkconf.patch
Patch1:		libpng-1.2.10-lib64.patch
Patch2:		libpng-1.2.12-x86-32-mmx.patch
Buildroot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Epoch: 		2

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
Conflicts:	gdk-pixbuf < 0.11.0-6mdk

# fredl: to allow upgrades to work, list all the libs from 8.1 packages that
# depends on libpng2:
Conflicts:	Epplets < 0.5-8mdk
Conflicts:	gdk-pixbuf-loaders < 0.16.0-1mdk
Conflicts:	gnome-core < 1.4.0.6-1mdk
Conflicts:	kdeaddons < 2.2.2-2mdk
Conflicts:	kdebase < 2.2.2-37mdk
Conflicts:	kdebase-nsplugins < 2.2.2-37mdk
Conflicts:	kdebindings < 2.2.2-4mdk
Conflicts:	kdegames < 2.2.2-4mdk
Conflicts:	kdegraphics < 2.2.2-4mdk
Conflicts:	kdelibs < 2.2.2-29mdk
Conflicts:	kdelibs-sound < 2.2.2-29mdk
Conflicts:	kdemultimedia < 2.2.2-3mdk
Conflicts:	kdemultimedia-aktion < 2.2.2-3mdk
Conflicts:	kdenetwork < 2.2.2-11mdk
Conflicts:	kdepim < 2.2.2-2mdk
Conflicts:	kdesdk < 2.2.2-4mdk
Conflicts:	kdetoys < 2.2.2-6mdk
Conflicts:	kdeutils < 2.2.2-6mdk
Conflicts:	kdevelop < 2.0.2-4mdk
Conflicts:	koffice < 1.1.1-8mdk
Conflicts:	kvirc < 2.1.1-5mdk
Conflicts:	libSDL_image1.2 < 1.2.1-1mdk
Conflicts:	libclanlib1-png < 0.5.1-5mdk
Conflicts:	libcups1 < 1.1.12-3mdk
Conflicts:	libeel0 < 1.0.2-6mdk
Conflicts:	libfnlib0 < 0.5-2mdk
Conflicts:	libgd1 < 1.8.4-4mdk
Conflicts:	libgtk+2 < 1.3.12-4mdk
Conflicts:	libgtkxmhtml1 < 1.4.1.4-1mdk
Conflicts:	libimlib1 < 1.9.11-8mdk
Conflicts:	libqt2 < 2.3.1-24mdk
Conflicts:	libwraster2 < 0.80.0-2mdk
Conflicts:	linuxconf < 1.26r5-2mdk
Conflicts:	nautilus < 1.0.6-8mdk
Conflicts:	sawfish < 1.0-7mdk


%description -n	%{lib_name}
This package contains the library needed to run programs dynamically
linked with libpng.

%package -n	%{lib_name}-devel
Summary:	Development tools for programs to manipulate PNG image format files
Group:		Development/C
Requires:	%{lib_name} = %{epoch}:%{version}-%{release} zlib-devel
Obsoletes:	%{lib_name_orig}-devel
Provides:	%{lib_name_orig}-devel = %{epoch}:%{version}-%{release}
Provides:	png-devel = %{epoch}:%{version}-%{release}

%description -n	%{lib_name}-devel
The libpng-devel package contains the header files and libraries
necessary for developing programs using the PNG (Portable Network
Graphics) library.

If you want to develop programs which will manipulate PNG image format
files, you should install libpng-devel.  You'll also need to install the
libpng package.

%package -n	%{lib_name}-static-devel
Summary:	Development static libraries
Group:		Development/C
Requires:	%{lib_name_orig}-devel = %{epoch}:%{version}-%{release} zlib-devel
Provides:	%{lib_name_orig}-static-devel = %{epoch}:%{version}-%{release}
Provides:	png-static-devel = %{epoch}:%{version}-%{release}

%description -n	%{lib_name}-static-devel
Libpng development static libraries.

%prep
%setup -q
%patch0 -p1 -b .mdkconf
%patch1 -p1 -b .lib64
%patch2 -p1 -b .x86-32-mmx

perl -pi -e 's|^prefix=.*|prefix=%{_prefix}|' scripts/makefile.linux
perl -pi -e 's|^(LIBPATH=.*)/lib\b|\1/%{_lib}|' scripts/makefile.linux
ln -s scripts/makefile.linux ./Makefile

%build
%configure2_5x
%make

%check
make check

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_prefix}
%makeinstall

install -d %{buildroot}%{_mandir}/man{3,5}
install -m0644 {libpng,libpngpf}.3 %{buildroot}%{_mandir}/man3
install -m0644 png.5 %{buildroot}%{_mandir}/man5/png3.5

# remove unpackaged files
rm -rf %{buildroot}{%{_prefix}/man,%{_libdir}/lib*.la}

#multiarch
%multiarch_binaries $RPM_BUILD_ROOT%{_bindir}/libpng12-config

%post -n %{lib_name} -p /sbin/ldconfig

%postun -n %{lib_name} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files -n %{lib_name}
%defattr(-,root,root)
%doc *.txt example.c README TODO CHANGES
%{_libdir}/libpng12.so.*
%{_libdir}/libpng.so.*
%{_mandir}/man5/*

%files -n %{lib_name}-devel
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

%files -n %{lib_name}-static-devel
%defattr(-,root,root)
%doc README
%{_libdir}/libpng*.a


