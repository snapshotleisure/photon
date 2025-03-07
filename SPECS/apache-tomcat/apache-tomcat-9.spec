%define _use_internal_dependency_generator 0
%define _origname apache-tomcat
%define _prefix /var/opt/%{name}
%define _origprefix /var/opt/%{_origname}
%define _bindir %{_prefix}/bin
%define _confdir %{_prefix}/conf
%define _libdir %{_prefix}/lib
%define _webappsdir %{_prefix}/webapps
%define _logsdir %{_prefix}/logs
%define _tempdir %{_prefix}/temp

Summary:        Apache Tomcat 9
Name:           apache-tomcat-9
Version:        9.0.80
Release:        1%{?dist}
License:        Apache
URL:            http://tomcat.apache.org
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://archive.apache.org/dist/tomcat/tomcat-9/v%{version}/src/%{_origname}-%{version}-src.tar.gz
%define sha512 %{_origname}=a2fb298c1fd2615e1a69371b5f84eb569e897faad3cbe17e3626460f5ce311085c120dd3f62c255fde87e6517915365ab52ada613776d45185b8e53624935114
# base-for-apache-tomcat is a cached -Dbase.path folder
# generate base-for-apache-tomcat code with following steps:
# 1. tar -xvzf Source0 to $HOME
# 2. cd %{_origname}-%{version}-src && ant deploy dist-prepare dist-source
# 3. generated code will be exist to default location $HOME/tomcat-build-libs
# 4. mv tomcat-build-libs base-for-%{_origname}-%{version}
# 5. tar -cvzf base-for-%{_origname}-%{version}.tar.gz base-for-%{_origname}-%{version}
Source1: base-for-%{_origname}-%{version}.tar.gz
%define sha512 base=a9af5a439100d05e0efd9246aaef59824fab9e9f453c513ccfc196a87058510d0d3f9974c16fe2aab81fa9f137f52b913ac4e353a32cbcf01f4e07551553110f

Patch0: apache-tomcat-use-jks-as-inmem-keystore.patch

BuildArch: noarch

BuildRequires: openjdk11
BuildRequires: apache-ant

Requires: jre >= 8.0
Requires: apache-ant
Requires: chkconfig

%description
The Apache Tomcat package contains binaries for the Apache Tomcat servlet container.

%package        webapps
Summary:        Web application for Apache Tomcat
Group:          Applications/System
Requires:       %{name} = %{version}-%{release}

%description    webapps
The web application for Apache Tomcat.

%prep
%autosetup -n %{_origname}-%{version}-src -p1 -b1
# remove pre-built binaries and windows files
find . -type f \( -name "*.bat" -o -name "*.class" -o -name Thumbs.db -o -name "*.gz" -o \
   -name "*.jar" -o -name "*.war" -o -name "*.zip" \) -delete

%build
ant -Dant.build.javac.source=1.8 -Dant.build.javac.target=1.8 \
 -Dbase.path="../base-for-%{_origname}-%{version}" deploy dist-prepare dist-source

%install
install -vdm 755 %{buildroot}%{_prefix}
install -vdm 755 %{buildroot}%{_bindir}
install -vdm 755 %{buildroot}%{_libdir}
install -vdm 755 %{buildroot}%{_confdir}
install -vdm 755 %{buildroot}%{_webappsdir}
install -vdm 755 %{buildroot}%{_logsdir}
install -vdm 755 %{buildroot}%{_tempdir}
cp -r %{_builddir}/%{_origname}-%{version}-src/output/build/bin/* %{buildroot}%{_bindir}
cp -r %{_builddir}/%{_origname}-%{version}-src/output/build/lib/* %{buildroot}%{_libdir}
cp -r %{_builddir}/%{_origname}-%{version}-src/output/build/conf/* %{buildroot}%{_confdir}
cp -r %{_builddir}/%{_origname}-%{version}-src/output/build/webapps/* %{buildroot}%{_webappsdir}

cp %{_builddir}/%{_origname}-%{version}-src/LICENSE %{buildroot}%{_prefix}
cp %{_builddir}/%{_origname}-%{version}-src/NOTICE %{buildroot}%{_prefix}

touch %{buildroot}%{_logsdir}/catalina.out
rm -rf %{buildroot}%{_prefix}/webapps/{examples,docs}

install -vdm 644 %{buildroot}%{_datadir}/java/tomcat9

for jar in %{buildroot}/%{_libdir}/*.jar
do
    jarname=$(basename $jar .jar)
    ln -sfv %{_libdir}/${jarname}.jar %{buildroot}%{_datadir}/java/tomcat9/${jarname}.jar
done

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%dir %{_prefix}
%dir %{_bindir}
%dir %{_libdir}
%dir %{_confdir}
%dir %{_webappsdir}/ROOT
%dir %{_logsdir}
%dir %{_tempdir}
%{_bindir}/*
%config(noreplace) %{_confdir}/catalina.policy
%config(noreplace) %{_confdir}/catalina.properties
%config(noreplace) %{_confdir}/context.xml
%config(noreplace) %{_confdir}/jaspic-providers.xml
%config(noreplace) %{_confdir}/jaspic-providers.xsd
%config(noreplace) %{_confdir}/logging.properties
%config(noreplace) %{_confdir}/server.xml
%config(noreplace) %{_confdir}/tomcat-users.xml
%config(noreplace) %{_confdir}/tomcat-users.xsd
%config(noreplace) %{_confdir}/web.xml
%{_libdir}/*
%{_datadir}/java/tomcat9/*.jar
%{_prefix}/LICENSE
%{_prefix}/NOTICE
%{_logsdir}/catalina.out

%files webapps
%defattr(-,root,root)
%dir %{_webappsdir}/manager
%dir %{_webappsdir}/host-manager
%{_webappsdir}/ROOT/*
%{_webappsdir}/manager/*
%{_webappsdir}/host-manager/*

%post
alternatives --install %{_origprefix} apache-tomcat %{_prefix} 10000 \
  --slave %{_datadir}/java/tomcat tomcat %{_datadir}/java/tomcat9

%postun
# Do alternative remove only in case of uninstall
if [ $1 -eq 0 ]; then
alternatives --remove apache-tomcat %{_prefix}
fi

%changelog
* Mon Sep 04 2023 Vamsi Krishna Brahmajosuyula <vbrahmajosyula@vmware.com> 9.0.80-1
- Upgrade to 9.0.80
* Wed Sep 21 2022 Vamsi Krishna Brahmajosuyula <vbrahmajosyula@vmware.com> 8.5.78-2
- Use openjdk11
* Mon Apr 04 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.5.78-1
- Version Bump to 8.5.78
* Thu Feb 10 2022 Nitesh Kumar <kunitesh@vmware.com> 8.5.72-1
- Upgrade to 8.5.72, Fix CVE-2022-23181
* Tue Jul 20 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.5.68-1
- Version Bump to 8.5.68 to fix CVE-2021-30639
* Wed Mar 31 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.5.64-1
- Version Bump to 8.5.64
* Wed Oct 07 2020 Dweep Advani <dadvani@vmware.com> 8.5.58-1
- Version Bump to 8.5.58
* Wed Aug 05 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.5.57-1
- Version Bump to 8.5.57
* Wed Jul 08 2020 Dweep Advani <dadvani@vmware.com> 8.5.51-3
- Patched for CVE-2020-11996
* Wed May 27 2020 Dweep Advani <dadvani@vmware.com> 8.5.51-2
- Patched for CVE-2020-9484
* Mon Mar 16 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.5.51-1
- Update to version 8.5.51 to fix CVE-2020-1938
* Mon Jan 06 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.5.50-1
- Update to version 8.5.50 to fix CVE-2019-17563
* Tue Jul 16 2019 Dweep Advani <dadvani@vmware.com> 8.5.40-2
- Fix CVE-2019-10072
* Tue Apr 23 2019 Dweep Advani <dadvani@vmware.com> 8.5.40-1
- Upgrading to version 8.5.40
* Thu Jan 10 2019 Dweep Advani <dadvani@vmware.com> 8.5.37-1
- Upgrade to version 8.5.37
* Fri Dec 07 2018 Dweep Advani <dadvani@vmware.com> 8.5.35-1
- Upgrade to version 8.5.35
* Wed Nov 21 2018 Dweep Advani <dadvani@vmware.com> 8.5.31-3
- Fix CVE-2018-8014
* Thu May 17 2018 Xiaolin Li <xiaolinl@vmware.com> 8.5.31-2
- Mark configuration files as config(noreplace)
* Mon May 07 2018 Xiaolin Li <xiaolinl@vmware.com> 8.5.31-1
- Upgraded to version 8.5.31
* Mon Apr 30 2018 Xiaolin Li <xiaolinl@vmware.com> 8.5.30-1
- Upgraded to version 8.5.30
* Tue Mar 20 2018 Xiaolin Li <xiaolinl@vmware.com> 8.5.29-1
- Upgraded to version 8.5.29
* Wed Feb 28 2018 Xiaolin Li <xiaolinl@vmware.com> 8.5.28-1
- Upgraded to version 8.5.28
* Fri Feb 02 2018 Xiaolin Li <xiaolinl@vmware.com> 8.5.27-1
- Upgraded to version 8.5.27
* Thu Dec 21 2017 Anish Swaminathan <anishs@vmware.com> 8.5.24-1
- Upgraded to version 8.5.24
* Mon Oct 16 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 8.5.23-2
- patch to keep using inmem keystore as jks.
* Tue Oct 10 2017 Anish Swaminathan <anishs@vmware.com> 8.5.23-1
- Upgraded to version 8.5.23
* Wed Sep 27 2017 Alexey Makhalov <amakhalov@vmware.com> 8.5.20-3
- Offline build, deactivate javadoc target
* Wed Sep 13 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 8.5.20-2
- Updated the permissions on directories packaged
* Tue Aug 15 2017 Anish Swaminathan <anishs@vmware.com> 8.5.20-1
- Upgraded to version 8.5.20
* Thu Jul 6 2017 Divya Thaluru <dthaluru@vmware.com> 8.5.16-1
- Upgraded to version 8.5.16
* Tue Jun 20 2017 Divya Thaluru <dthaluru@vmware.com> 8.5.15-2
- Removed version from directory path
- Removed dependency on ANT_HOME
* Tue Jun 6 2017 Divya Thaluru <dthaluru@vmware.com> 8.5.15-1
- Upgraded to version 8.5.15
* Thu May 18 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 8.5.13-3
- Renamed openjdk to openjdk8
* Tue Apr 18 2017 Divya Thaluru <dthaluru@vmware.com> 8.5.13-2
- Added logic to package directories
* Mon Apr 10 2017 Divya Thaluru <dthaluru@vmware.com> 8.5.13-1
- Upgraded to version 8.5.13 and also added logic to build binaries from source
* Tue Nov 22 2016 Anish Swaminathan <anishs@vmware.com> 8.5.8-1
- Upgraded to version 8.5.8
* Wed Oct 05 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 8.0.37-1
- Update to version 8.0.37. Change openjre requires to latest
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 8.0.35-2
- GA - Bump release of all rpms
* Fri May 20 2016 Divya Thaluru <dthaluru@vmware.com> 8.0.35-1
- Upgraded to version 8.0.35
* Tue May 03 2016 Anish Swaminathan <anishs@vmware.com> 8.0.33-1
- Upgraded to version 8.0.33
* Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 7.0.68-1
- Upgraded to version 7.0.68
* Mon Nov 16 2015 Sharath George <sharathg@vmware.com> 7.0.63-3
- Change path to /var/opt.
* Wed Sep 16 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 7.0.63-2
- Updated dependency after repackaging openjdk.
* Wed Jul 8 2015 Sriram Nambakam <snambakam@vmware.com> 7.0.63
- Initial build.  First version
