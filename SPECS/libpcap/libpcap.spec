Summary:     C/C++ library for network traffic capture
Name:        libpcap
Version:     1.10.0
Release:     1%{?dist}
License:      BSD
URL:          http://www.tcpdump.org
Source0:      http://www.tcpdump.org/release/%{name}-%{version}.tar.gz
%define sha512 libpcap=007710386ff3435ef97fc99293076eae3c39b424e986141184c712b0285f8589357a1b25085f7eba28730de04312042c724d193934a399797e95a56f5301da7f
Group:        Networking/Libraries
Vendor:       VMware, Inc.
Distribution: Photon

BuildRequires: bison

%description
Libpcap provides a portable framework for low-level network
monitoring.  Libpcap can provide network statistics collection,
security monitoring and network debugging.  Since almost every system
vendor provides a different interface for packet capture, the libpcap
authors created this system-independent API to ease in porting and to
alleviate the need for several system-dependent packet capture modules
in each application.

Install libpcap if you need to do low-level network traffic monitoring
on your network.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1

%build
%configure
make %{?_smp_mflags}

%check
# make doesn't support _smp_mflags
make testprogs
testprogs/opentest
testprogs/findalldevstest

%install
# make doesn't support _smp_mflags
make DESTDIR=%{buildroot} install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_bindir}/*-config
%{_includedir}/*.h
%{_includedir}/pcap
%exclude %{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_mandir}/man7/*

%changelog
* Fri Feb 05 2021 Susant Sahani <ssahani@vmware.com> 1.10.0-1
- Version bump
* Mon Oct 14 2019 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.9.1-1
- Update to 1.9.1
* Mon Nov 26 2018 Ashwin H <ashwinh@vmware.com> 1.9.0-2
- Fix %check
* Sun Sep 30 2018 Bo Gan <ganb@vmware.com> 1.9.0-1
- Update to 1.9.0
- Split devel package
* Tue Apr 11 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.8.1-1
- Updated to version 1.8.1
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.7.4-2
- GA - Bump release of all rpms
* Fri Jan 15 2016 Xiaolin Li <xiaolinl@vmware.com> 1.7.4-1
- Updated to version 1.7.4
* Mon Apr 6 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 1.7.2-1
- Version upgrade to 1.7.2
* Wed Jan 21 2015 Divya Thaluru <dthaluru@vmware.com> 1.6.2-1
- Initial build. First version
