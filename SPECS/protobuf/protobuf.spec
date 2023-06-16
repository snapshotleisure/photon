Summary:        Google's data interchange format
Name:           protobuf
Version:        3.6.1
Release:        4%{?dist}
License:        BSD-3-Clause
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/google/protobuf

Source0:        %{name}-%{version}.tar.gz
%define sha512 %{name}=1bc175d24b49de1b1e41eaf39598194e583afffb924c86c8d2e569d935af21874be76b2cbd4d9655a1d38bac3d4cd811de88bc2c72d81bad79115e69e5b0d839

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  libstdc++
BuildRequires:  curl
BuildRequires:  make
BuildRequires:  unzip
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  chkconfig
BuildRequires:  openjre8 >= 1.8.0.45
BuildRequires:  openjdk8 >= 1.8.0.45
BuildRequires:  apache-maven >= 3.3.3

%description
Protocol Buffers (a.k.a., protobuf) are Google's language-neutral, platform-neutral, extensible mechanism for serializing structured data. You can find protobuf's documentation on the Google Developers site.

%package        devel
Summary:        Development files for protobuf
Group:          Development/Libraries
Requires:       protobuf = %{version}-%{release}

%description    devel
The protobuf-devel package contains libraries and header files for
developing applications that use protobuf.

%package        static
Summary:        protobuf static lib
Group:          Development/Libraries
Requires:       protobuf = %{version}-%{release}

%description    static
The protobuf-static package contains static protobuf libraries.

%package        python
Summary:        protobuf python lib
Group:          Development/Libraries
Requires:       python2
Requires:       python2-libs
Requires:       protobuf = %{version}-%{release}

%description    python
This contains protobuf python libraries.

%package        python3
Summary:        protobuf python3 lib
Group:          Development/Libraries
Requires:       python3
Requires:       python3-libs
Requires:       protobuf = %{version}-%{release}

%description    python3
This contains protobuf python3 libraries.

%package        java
Summary:        protobuf java
Group:          Development/Libraries
Requires:       openjre8 >= 1.8.0.45

%description    java
This contains protobuf java package.

%prep
%autosetup -p1

%build
autoreconf -iv
%configure --disable-silent-rules
make %{?_smp_mflags}

pushd python
python2 setup.py build
python3 setup.py build
popd

pushd java
mvn package
popd

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

pushd python
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd

pushd java
mvn install
install -vdm755 %{buildroot}%{_libdir}/java/protobuf
install -vm644 core/target/protobuf-java-3.6.1.jar %{buildroot}%{_libdir}/java/protobuf
install -vm644 util/target/protobuf-java-util-3.6.1.jar %{buildroot}%{_libdir}/java/protobuf
popd

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/protoc
%{_libdir}/libprotobuf-lite.so.*
%{_libdir}/libprotobuf.so.*
%{_libdir}/libprotoc.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/libprotobuf-lite.so
%{_libdir}/libprotobuf.so
%{_libdir}/libprotoc.so

%files static
%defattr(-,root,root)
%{_libdir}/libprotobuf-lite.a
%{_libdir}/libprotobuf.a
%{_libdir}/libprotoc.a

%files python
%{python_sitelib}/*

%files python3
%{python3_sitelib}/*

%files java
%{_libdir}/java/protobuf/*.jar

%changelog
* Sat Jun 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.6.1-4
- Bump version as a part of openjdk8 upgrade
* Sun Oct 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.6.1-3
- Remove .la files
* Wed May 18 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.6.1-2
- Bump version as a part of apache-maven upgrade
* Tue Sep 18 2018 Tapas Kundu <tkundu@vmware.com> 3.6.1-1
- Update to version 3.6.1
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 3.2.0-6
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.2.0-5
- Use python2 explicitly while building
* Thu May 18 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.2.0-4
- Renamed openjdk to openjdk8
* Fri Apr 28 2017 Siju Maliakkal <smaliakkal@vmware.com> 3.2.0-3
- Update python3 version
* Thu Apr 13 2017 Vinay Kulkarni <kulkarniv@vmware.com> 3.2.0-2
- Build protobuf-java.
* Fri Mar 31 2017 Rongrong Qiu <rqiu@vmware.com> 3.2.0-1
- Upgrade to 3.2.0
* Tue Mar 28 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.6.1-3
- Build protobuf-python.
* Mon Mar 20 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.6.1-2
- Build static lib.
* Fri Mar 03 2017 Xiaolin Li <xiaolinl@vmware.com> 2.6.1-1
- Initial packaging for Photon
