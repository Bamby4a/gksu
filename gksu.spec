#
# Conditional builds:
%bcond_without	nautilus	# build without nautilus extensions
#
Summary:	GKsu is a GTK+ frontend to the su program
Summary(pl.UTF-8):	GKsu to nakładka graficzna na program su
Name:		gksu
Version:	2.0.0
Release:	2
License:	GPL
Group:		Applications/System
Source0:	http://people.debian.org/~kov/gksu/%{name}-%{version}.tar.gz
# Source0-md5:	f517302cff6f09e4f2f312c4b618bd40
URL:		http://www.nongnu.org/gksu/
BuildRequires:	GConf2-devel
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	gtk+2-devel >= 2:2.2
BuildRequires:	gtk-doc >= 1.0
BuildRequires:	intltool
BuildRequires:	libgksu-devel >= 2.0
BuildRequires:	libtool
%{?with_nautilus:BuildRequires:	gnome-vfs2-devel}
%{?with_nautilus:BuildRequires:	nautilus-devel}
BuildRequires:	pkgconfig
Requires:	/bin/su
Obsoletes:	gksu-devel
Obsoletes:	gksu-static
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	`pkg-config --cflags gnome-vfs-2.0`
%define		nautilus_extensiondir %( pkg-config --variable=extensiondir libnautilus-extension )

%description
GKsu is a GTK+ frontend to the su program.

%description -l pl.UTF-8
GKsu to graficzna nakładka na program su.

%package nautilus
Summary:	Gksu plugin for nautilus
Summary(pl.UTF-8):	Wtyczka gksu dla nautilusa
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	nautilus
Obsoletes:	gksu-nautilus-devel
Obsoletes:	gksu-nautilus-static

%description nautilus
Gksu plugin for nautilus.

%description nautilus -l pl.UTF-8
Wtyczka gksu dla nautilusa.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-static \
	--enable-gtk-doc \
	%{!?with_nautilus: --disable-nautilus-extension} \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	nautilus_extensiondir=%{nautilus_extensiondir} \
	DESTDIR=$RPM_BUILD_ROOT

# fix gksudo man link
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/gksudo.1
echo .so man1/gksu.1 > $RPM_BUILD_ROOT%{_mandir}/man1/gksudo.1

rm -f $RPM_BUILD_ROOT%{_libdir}/nautilus/extensions-1.0/*.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_bindir}/*
%{_desktopdir}/*.desktop
%{_mandir}/man1/*
%{_pixmapsdir}/*
%dir %{_datadir}/gksu
%attr(755,root,root) %{_datadir}/gksu/gksu-migrate-conf.sh

%if %{with nautilus}
%files nautilus
%defattr(644,root,root,755)
%attr (755,root,root) %{nautilus_extensiondir}/libnautilus-gksu.so
%endif
