#
# TODO:		- config file templates
#
# Conditional build:
%bcond_without	tcp_wrappers	# build without tcp wrappers support
%bcond_without	sql		# don't build sql plugin
%bcond_without	xml		# don't build xml plugin
#
Summary:	A Network Intrusion Detection System
Summary(pl):	System do wykrywania intruzów w sieci
Name:		prelude-manager
Version:	0.9.7.1
Release:	2
License:	GPL
Group:		Applications
Source0:	http://www.prelude-ids.org/download/releases/%{name}-%{version}.tar.gz
# Source0-md5:	4af593e21b41faa220d9dc9648df4a85
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://www.prelude-ids.org/
BuildRequires:	gnutls-devel >= 1.0.17
BuildRequires:	libprelude-devel >= 0.9.7
%{?with_sql:BuildRequires:	libpreludedb-devel >= 0.9.4.1}
%{?with_xml:BuildRequires:	libxml2-devel >= 2.0.0}
%{?with_tcp_wrappers:BuildRequires:	libwrap-devel}
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Prelude-Manager is a high-availability server which collects and
normalizes events from distributed sensors.

%description -l pl
Prelude-Manager to serwer o wysokiej dostêpno¶ci zbieraj±cy i
normalizuj±cy zdarzenia od rozproszonych czujników.

%package sql
Summary:	Prelude-manager SQL plugin
Summary(pl):	Wtyczka SQL dla prelude-managera
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libpreludedb >= 0.9.4.1

%description sql
Prelude-manager SQL plugin.

%description sql -l pl
Wtyczka SQL dla prelude-managera.

%package xml
Summary:	Prelude-manager XML plugin
Summary(pl):	Wtyczka XML dla prelude-managera
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description xml
Prelude-manager XML plugin.

%description xml -l pl
Wtyczka XML dla prelude-managera.

%package devel
Summary:	Header files for prelude-manager
Summary(pl):	Pliki nag³ówkowe dla prelude-managera
Group:		Development/Libraries
Requires:	libprelude-devel >= 0.9.7

%description devel
Header files for prelude-manager.

%description devel -l pl
Pliki nag³ówkowe dla prelude-managera.

%prep
%setup -q

%build
%configure \
	--with%{!?with_tcp_wrappers:out}-libwrap \
	--with%{!?with_sql:out}-libpreludedb \
	--with%{!?with_xml:out}-xml
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
Run "prelude-adduser add prelude-manager --uid 0 --gid 0" before
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

%files xml
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/reports/xmlmod.so

%files sql
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/reports/db.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/%{name}
