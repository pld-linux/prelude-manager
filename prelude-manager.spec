#
# TODO:
# - config file templates
#
# Conditional build:
%bcond_without	maxminddb	# MaxMind GeoIP DB support
%bcond_with	system_libev	# system libev (expects libev built with EV_MULTIPLICITY=0)
#
Summary:	A Network Intrusion Detection System - events collector
Summary(pl.UTF-8):	System do wykrywania intruzów w sieci - serwer zbierający zdarzenia
Name:		prelude-manager
Version:	4.1.1
Release:	2
License:	GPL v2+
Group:		Applications/Networking
#Source0Download: https://www.prelude-siem.org/projects/prelude/files
Source0:	https://www.prelude-siem.org/attachments/download/836/%{name}-%{version}.tar.gz
# Source0-md5:	f821e3a5440b8a47117f2610d72174ab
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		https://www.prelude-siem.org/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9
BuildRequires:	gnutls-devel >= 1.0.17
%{?with_system_libev:BuildRequires:	libev-devel}
%{?with_maxminddb:BuildRequires:	libmaxminddb-devel >= 1.0.0}
BuildRequires:	libprelude-devel >= 4.1.0
BuildRequires:	libpreludedb-devel >= 4.1.0
BuildRequires:	libtool
BuildRequires:	libwrap-devel
BuildRequires:	libxml2-devel >= 2.0.0
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	rc-scripts
Requires:	gnutls-libs >= 1.0.17
%{?with_maxminddb:Requires:	libmaxminddb >= 1.0.0}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Prelude-Manager is a high-availability server which collects and
normalizes events from distributed sensors.

%description -l pl.UTF-8
Prelude-Manager to serwer o wysokiej dostępności zbierający i
normalizujący zdarzenia od rozproszonych czujników.

%package sql
Summary:	Prelude-manager SQL plugin
Summary(pl.UTF-8):	Wtyczka SQL dla prelude-managera
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libpreludedb >= 4.1.0

%description sql
Prelude-manager SQL plugin.

%description sql -l pl.UTF-8
Wtyczka SQL dla prelude-managera.

%package xml
Summary:	Prelude-manager XML plugin
Summary(pl.UTF-8):	Wtyczka XML dla prelude-managera
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description xml
Prelude-manager XML plugin.

%description xml -l pl.UTF-8
Wtyczka XML dla prelude-managera.

%package devel
Summary:	Header files for prelude-manager
Summary(pl.UTF-8):	Pliki nagłówkowe dla prelude-managera
Group:		Development/Libraries
Requires:	libprelude-devel >= 4.1.0

%description devel
Header files for prelude-manager.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla prelude-managera.

%prep
%setup -q

%if %{with system_libev}
# stub
echo 'all:' > libev/Makefile
%endif

%build
# rebuild auto* for as-needed to work
%{__libtoolize}
%{__aclocal} -I m4 -I libmissing/m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
%if %{with system_libev}
	LIBEV_CFLAGS=" " \
	LIBEV_LIBS="-lev" \
	--with-libev \
%endif
	%{!?with_libmaxminddb:--with-libmaxminddb}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# are generating wrong dependencies (and are not needed anyway)
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/*/*.la

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

install -d $RPM_BUILD_ROOT%{_sysconfdir}/prelude/profile/%{name}

install -d $RPM_BUILD_ROOT%{systemdtmpfilesdir}
cat >$RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf <<EOF
d /var/run/%{name} 0700 root root -
EOF

# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_docdir}/%{name}/smtp/template.example

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add prelude-manager
if [ "$1" = "1" ]; then
%banner -e %{name} <<EOF
Run "prelude-admin add prelude-manager --uid 0 --gid 0" before
starting Prelude Manager for the first time.

EOF
fi
%service prelude-manager restart "Prelude Manager"

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/prelude-manager ]; then
		%service prelude-manager stop 1>&2
	fi
	/sbin/chkconfig --del prelude-manager
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README plugins/reports/smtp/template.example
%attr(755,root,root) %{_bindir}/prelude-manager
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/decodes
%attr(755,root,root) %{_libdir}/%{name}/decodes/*.so
%dir %{_libdir}/%{name}/filters
%attr(755,root,root) %{_libdir}/%{name}/filters/*.so
%dir %{_libdir}/%{name}/reports
%attr(755,root,root) %{_libdir}/%{name}/reports/debug.so
%attr(755,root,root) %{_libdir}/%{name}/reports/smtp.so
%attr(755,root,root) %{_libdir}/%{name}/reports/textmod.so
%attr(700,root,root) %dir %{_sysconfdir}/%{name}
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/prelude-manager.conf
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%dir %{_sysconfdir}/prelude/profile/%{name}
%{_datadir}/%{name}
%attr(700,root,root) %dir %{_var}/run/%{name}
%{systemdtmpfilesdir}/prelude-manager.conf
%attr(700,root,root) %dir %{_var}/spool/prelude-manager
%attr(700,root,root) %dir %{_var}/spool/prelude-manager/failover
%attr(700,root,root) %dir %{_var}/spool/prelude-manager/scheduler
%{_mandir}/man1/prelude-manager.1*

%files xml
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/reports/xmlmod.so

%files sql
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/reports/db.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/%{name}
