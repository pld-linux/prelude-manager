#
# TODO:		- config file templates
#
Summary:	A Network Intrusion Detection System
Summary(pl):	System do wykrywania intruzów w sieci
Name:		prelude-manager
Version:	0.9.4.1
Release:	0.3
License:	GPL
Group:		Applications
Source0:	http://www.prelude-ids.org/download/releases/%{name}-%{version}.tar.gz
# Source0-md5:	4641da26473496b2bc43647753ff0499
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://www.prelude-ids.org/
BuildRequires:	gnutls-devel
BuildRequires:	libprelude-devel >= 0.9.7.2
BuildRequires:	libpreludedb-devel >= 0.9.7.1
BuildRequires:	libxml2-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	rc-scripts
Requires:	libprelude >= 0.9.7.2
Requires:	libpreludedb >= 0.9.7.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Prelude-Manager is a high-availability server which collects and
normalizes events from distributed sensors.

%description -l pl
Prelude-Manager to serwer o wysokiej dostêpno¶ci zbieraj±cy i
normalizuj±cy zdarzenia od rozproszonych czujników.

%package devel
Summary:	Header files for prelude-manager
Summary(pl):	Pliki nag³ówkowe dla prelude-managera
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for prelude-manager.

%description devel -l pl
Pliki nag³ówkowe dla prelude-managera.

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

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

install -d $RPM_BUILD_ROOT%{_sysconfdir}/prelude/profile/%{name}
install -d $RPM_BUILD_ROOT/var/spool/prelude/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add prelude-manager
if [ "$1" = 1 ]; then
	echo "Run \"prelude-adduser add prelude-manager --uid 0 --gid 0\" before"
	echo "starting Prelude Manager for the first time."
fi
%service prelude-manager restart "Prelude Manager"

# TODO:
#
# add this to libpreludedb (as an init script or docs):
#
# For PostgreSQL database you have to create a new database:
#
# 	$ PGPASSWORD=your_password psql -U postgres
# 	postgres=# CREATE database prelude;
# 	postgres=# CREATE USER prelude WITH ENCRYPTED PASSWORD 'prelude' NOCREATEDB NOCREATEUSER;
#	^D
#	$ PGPASSWORD=prelude psql -U prelude -d prelude < /usr/share/libpreludedb/classic/pgsql.sql
#
# Updating database schema:
#
#	$ PGPASSWORD=prelude psql -U prelude -d prelude < /usr/share/libpreludedb/classic/pgsql-update-14-1.sql
#
# add this to prelude-manager (as an init script or docs):
#
# 	 prelude-adduser add prelude-manager --uid 0 --gid 0
#

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
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*.*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(755,root,root) %{_bindir}/%{name}
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/*
%attr(755,root,root) %{_libdir}/%{name}/*/*.so
%dir %{_sysconfdir}/prelude/profile/%{name}
%{_libdir}/%{name}/*/*.la
%{_datadir}/%{name}
%{_var}/run/%{name}
%{_var}/spool/%{name}
%{_var}/spool/prelude/%{name}

%files devel
%defattr(644,root,root,755)
%{_includedir}/%{name}
