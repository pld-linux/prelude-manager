#
# TODO:
# - config file templates
# - system libev?
#
Summary:	A Network Intrusion Detection System
Summary(pl.UTF-8):	System do wykrywania intruzów w sieci
Name:		prelude-manager
Version:	1.0.0
Release:	1
License:	GPL v2+
Group:		Applications
#Source0Download: http://www.prelude-ids.com/developpement/telechargement/index.html
Source0:	http://www.prelude-ids.com/download/releases/prelude-manager/%{name}-%{version}.tar.gz
# Source0-md5:	d9236471bc7c0d420755249680261d18
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://www.prelude-ids.com/
BuildRequires:	gnutls-devel >= 1.0.17
BuildRequires:	libprelude-devel >= %{version}
BuildRequires:	libpreludedb-devel >= %{version}
BuildRequires:	libwrap-devel
BuildRequires:	libxml2-devel >= 2.0.0
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	rc-scripts
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
Requires:	libpreludedb >= %{version}

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
Requires:	libprelude-devel >= 0.9.7

%description devel
Header files for prelude-manager.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla prelude-managera.

%prep
%setup -q

%build
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# are generating wrong dependencies (and are not needed anyway)
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/*/*.la

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

install -d $RPM_BUILD_ROOT%{_sysconfdir}/prelude/profile/%{name}
install -d $RPM_BUILD_ROOT/var/spool/prelude/%{name}

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
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/%{name}
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/*
%attr(755,root,root) %{_libdir}/%{name}/*/*.so
%exclude %{_libdir}/%{name}/reports/db.*
%exclude %{_libdir}/%{name}/reports/xmlmod.*
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*.*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%dir %{_sysconfdir}/prelude/profile/%{name}
%{_datadir}/%{name}
%{_var}/run/%{name}
%{_var}/spool/%{name}
%{_var}/spool/prelude
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
