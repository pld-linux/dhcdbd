#
# TODO:
# - move header file to -devel
# - split an -init
#
Summary:	DHCP D-BUS daemon (dhcdbd) controls dhclient sessions with D-BUS, stores and presents DHCP options
Summary(pl):	Demon DHCP D-BUS (dhcdbd) - sterowanie sesjami dhclient przy u¿yciu D-BUS, przechowywanie opcji DHCP
Name:		dhcdbd
Version:	1.12
Release:	0.1
License:	GPL
Group:		Networking/Daemons
Source0:	http://people.redhat.com/~jvdias/dhcdbd/%{name}-%{version}.tar.gz
# Source0-md5:	f84f00d10643193fb5e6ee08ccfc0b09
Source1:	%{name}.init
URL:		http://people.redhat.com/~jvdias/dhcdbd/
BuildRequires:	dbus-devel >= 0.33
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	dbus >= 0.33
Requires:	dhcp-client >= 3:3.0.3-3
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
DHCP D-BUS daemon (dhcdbd) controls dhclient sessions with D-BUS,
stores and presents DHCP options.

%description -l pl
Demon DHCP D-BUS (dhcdbd) steruje sesjami dhclient przy u¿yciu D-BUS,
a tak¿e przechowuje i przedstawia opcje DHCP.

%prep
%setup -q

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/dhcdbd

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add dhcdbd
%service dhcdbd restart "DHCP D-BUS daemon"
if [ -f /var/lock/subsys/dhcdbd ]; then
	echo "You will probably also need \"/sbin/service messagebus restart\""
	echo "to reload the *.service database."
fi

%preun
if [ "$1" = "0" ]; then
	%service dhcdbd stop
	/sbin/chkconfig --del dhcdbd
fi

%files
%defattr(644,root,root,755)
%doc README LICENSE dhcp_options.h dhcdbd.h dbus_service.h
%attr(755,root,root) %{_sbindir}/dhcdbd
%attr(754,root,root) /etc/rc.d/init.d/dhcdbd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dbus-1/system.d/dhcdbd.conf
%{_datadir}/dbus-1/services/dhcdbd.service
