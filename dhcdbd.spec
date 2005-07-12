#
# TODO:
# - move header file to -devel
# - split an -init
#
Summary:	DHCP D-BUS daemon (dhcdbd) controls dhclient sessions with D-BUS, stores and presents DHCP options.
#Summary(pl):
Name:		dhcdbd
Version:	1.6
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	http://people.redhat.com/~jvdias/dhcdbd/%{name}-%{version}.tar.gz
# Source0-md5:	e46269dcfceca8fb678e48a42450db0b
Source1:	%{name}.init
URL:		http://people.redhat.com/~jvdias/dhcdbd
BuildRequires:	dbus-devel >= 0.33
Requires:	dbus >= 0.33
Requires:	dhcp-client >= 3.0.2
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DHCP D-BUS daemon (dhcdbd) controls dhclient sessions with D-BUS,
stores and presents DHCP options.

#description -l pl

%prep
%setup -q

%build
%{__make} \
	CFLAGS="%{rpmcflags}"
	LDFALGS="%{rpmldflags}"
	CC="%{__gcc}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -c %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/dhcdbd

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add dhcdbd
if [ -f /var/lock/subsys/dhcdbd ]; then
	/etc/rc.d/init.d/dhcdbd restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/dhcdbd start\" to start DHCP D-BUS daemon."
	echo "You will probably also need \"/etc/rc.d/init.d/messagebus restart\""
	echo "to reload the *.service database."
fi


%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/dhcdbd ]; then
		/etc/rc.d/init.d/dhcdbd stop 1>&2
	fi
	[ ! -x /sbin/chkconfig ] || /sbin/chkconfig --fel dhcdbd
fi

%files
%defattr(644,root,root,755)
%doc README LICENSE dhcp_options.h dhcdbd.h dbus_service.h
%attr(755,root,root) /sbin/dhcdbd
%attr(754,root,root) /etc/rc.d/init.d/dhcdbd
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/dhcdbd.conf
%{_datadir}/dbus-1/services/dhcdbd.service
