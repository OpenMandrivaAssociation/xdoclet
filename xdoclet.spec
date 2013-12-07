# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define gcj_support 0

%define section free

# FIXME: JPP 1.7 lacks webwork and xwork, needed for the demo
%define _without_demo 1

# If you do not want to build samples in demo subpackage because of their 
# runtime deps, give rpmbuild option '--without demo'
%define with_demo %{!?_without_demo:1}%{?_without_demo:0}

Name:		xdoclet
Version:	1.2.3
Release:	8.0.9
Epoch:		0
Summary:	XDoclet Attribute Orientated Programming Framework
License:	XDoclet Open Source Licence
Group:		Development/Java
URL:		http://xdoclet.sourceforge.net
Source0:	%{name}-src-%{version}-RHCLEAN.tgz
Source1:	%{name}-modules-objectweb-4.6.tgz
Patch0:		xdoclet-build_xml.patch
Patch1:		xdoclet-XDocletModulesEjbMessages.patch
Patch2:		xdoclet-ant.not-required.patch
Patch3:		xdoclet-WebLogicSubTask.patch
Patch4:		xdoclet-project_xml.patch
Patch5:		xdoclet-AbstractProgramElementTagsHandler.patch
Patch6:		xdoclet-build_docs_xml.patch

%if ! %{gcj_support}
BuildArch:	noarch
%endif
BuildRoot: 	%{_tmppath}/%{name}-root
BuildRequires:  java-devel >= 0:1.4.2
BuildRequires:  java-rpmbuild >= 0:1.6
BuildRequires:  ant >= 0:1.6
BuildRequires:  ant-nodeps >= 0:1.5
BuildRequires:	ant-trax
BuildRequires:  junit
BuildRequires:  javacc
BuildRequires:  jrefactory
BuildRequires:  bsf 
BuildRequires:  jakarta-commons-collections 
BuildRequires:  jakarta-commons-lang 
BuildRequires:  jakarta-commons-logging 
BuildRequires:  log4j
BuildRequires:  struts 
BuildRequires:  velocity 
BuildRequires:  xalan-j2 >= 0:2.7.0
BuildRequires:  xml-commons-apis 
BuildRequires:  xjavadoc >= 0:1.1

Requires:  bsf
Requires:  jakarta-commons-collections
Requires:  jakarta-commons-logging
Requires:  log4j
Requires:  velocity
Requires:  xalan-j2 >= 0:2.7.0
Requires:  xml-commons-apis
Requires:  xjavadoc = 0:1.1

%if %{gcj_support}
BuildRequires:		java-gcj-compat-devel
%endif

%description
This package contains the XDoclet Attribute Orientated Programming Framework

%if %{with_demo}
%package demo
Summary:	XDoclet Sample Projects
Group:		Development/Java
BuildRequires:  servletapi4
BuildRequires:  struts
BuildRequires:  velocity
BuildRequires:  webwork >= 0:2.1
BuildRequires:  xwork
BuildRequires:  geronimo-ejb-2.1-api
BuildRequires:  myfaces
BuildRequires:  geronimo-jms-1.1-api
BuildRequires:  mx4j
Requires:  %{name} = %{version}-%{release}
Requires:  geronimo-ejb-2.1-api
Requires:  myfaces
Requires:  geronimo-jms-1.1-api
Requires:  webwork
Requires:  xwork
Requires:  mx4j
Requires:  struts
Requires:  servletapi4

%description demo
This package contains sample XDoclet projects.
%endif

%package javadoc
Summary:	XDoclet Javadoc
Group:		Development/Java

%description javadoc
This package contains XDoclet javadoc

%package manual
Summary:	XDoclet Sample Manuals and Documentation
Group:		Development/Java

%description manual
This package contains XDoclet documentation.

%prep
%setup -q
find . -name "*.jar" -exec rm {} \;

# Replace JOnAS specific tasks with code blessed by ObjectWeb
pushd modules
mv objectweb objectweb.orig
tar xzf %{SOURCE1}
popd

# Remove mockobjects support.
rm -rf modules/mockobjects

for j in xjavadoc-1.1 jrefactory javacc junit bsf commons-collections commons-logging log4j velocity xalan-j2 xjavadoc xml-commons-apis; do
	ln -s $(build-classpath $j) lib
done

%if %{with_demo}
for j in servletapi4 struts velocity webwork-migration xwork geronimo-ejb-2.1-api myfaces/myfaces-jsf-api geronimo-jms-1.1-api; do
	ln -s $(build-classpath $j) samples/lib
done
for j in mx4j/mx4j-jmx mx4j/mx4j-tools; do
        i=$(build-classpath $j)
	ln -s $(build-classpath $j) samples/lib
done
%endif

%patch0 -p0 -b .sav
%patch1 -p0 -b .sav
%patch2 -p0 
%patch3 -p0 -b .sav
%patch4 -p0 -b .sav
%patch5 -p0 -b .sav
%patch6 -p0 -b .sav

%build
export OPT_JAR_LIST="ant/ant-nodeps jrefactory jaxp_transform_impl ant/ant-trax xalan-j2 xalan-j2-serializer"
%{ant} xjavadoc core modules docs l10n

%if %{with_demo}
%{ant} samples
%endif

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_javadir}/%{name}
install -m 644 target/lib/xdoclet*.jar $RPM_BUILD_ROOT%{_javadir}/%{name}
(cd $RPM_BUILD_ROOT%{_javadir}/%{name} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

%if %{with_demo}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
cp -pr samples/* $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
%endif

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr target/docs/api $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
rm -rf target/docs/api

mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -p LICENSE.txt $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -pr target/docs/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%{gcj_compile}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root, root,0755)
%{_javadir}/%{name}
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
#%doc %{_docdir}/%{name}-%{version}/LICENSE.txt
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-apache-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-bea-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-borland-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-caucho-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-ejb-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-exolab-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-hibernate-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-hp-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-ibm-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-java-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-jboss-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-jdo-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-jmx-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-jsf-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-libelis-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-macromedia-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-mvcsoft-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-mx4j-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-objectweb-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-openejb-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-oracle-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-orion-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-portlet-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-pramati-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-solarmetric-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-spring-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-sun-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-sybase-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-tjdo-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-web-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-webwork-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-wsee-module-1.2.3.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xdoclet-xdoclet-module-1.2.3.jar.*
%endif

%if %{with_demo}
%files demo
%defattr(-, root, root, -)
%{_datadir}/%{name}-%{version}
%endif

%files javadoc
%defattr(-, root, root, -)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

%files manual
%defattr(-, root, root, -)
%doc %{_docdir}/%{name}-%{version}


%changelog
* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.2.3-8.0.5mdv2011.0
+ Revision: 608200
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.2.3-8.0.4mdv2010.1
+ Revision: 524430
- rebuilt for 2010.1

* Tue Sep 01 2009 Christophe Fergeau <cfergeau@mandriva.com> 0:1.2.3-8.0.3mdv2010.0
+ Revision: 423785
- rebuild

  + Nicolas Lécureuil <nlecureuil@mandriva.com>
    - Rediff patch

* Mon Jul 28 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0:1.2.3-8.0.1mdv2009.0
+ Revision: 251702
- fix build

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Anssi Hannula <anssi@mandriva.org>
    - buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 7.3.2mdv2008.0-current
+ Revision: 87268
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Thu Sep 13 2007 David Walluck <walluck@mandriva.org> 0:1.2.3-7.3.1mdv2008.0
+ Revision: 84895
- add xalan-j2 xalan-j2-serializer to OPT_JAR_LIST
- sync with fc to remove mockobjects dep

* Thu Jul 26 2007 Anssi Hannula <anssi@mandriva.org> 0:1.2.3-6mdv2008.0
+ Revision: 55961
- use xml-commons-jaxp-1.3-apis explicitely instead of the generic
  xml-commons-apis which is provided by multiple packages (see bug #31473)


* Sat Dec 16 2006 David Walluck <walluck@mandriva.org> 1.2.3-4mdv2007.0
+ Revision: 98108
- rebuild
- rebuild
- Import xdoclet

* Thu Aug 17 2006 David Walluck <walluck@mandriva.org> 0:1.2.3-3mdv2007.0
- add xalan-j2-serializer to CLASSPATH
- fix macro in changelog

* Sun Jun 04 2006 David Walluck <walluck@mandriva.org> 0:1.2.3-2mdv2007.0
- rebuild for libgcj.so.7

* Wed Nov 02 2005 David Walluck <walluck@mandriva.org> 0:1.2.2-2.2mdk
- BuildRequires: ant-nodeps, ant-trax

* Sun Sep 11 2005 David Walluck <walluck@mandriva.org> 0:1.2.2-2.1mdk
- release

* Thu Jun 16 2005 Gary Benson <gbenson@redhat.com> - 0:1.2.2-2jpp_1fc
- Add missing javadoc %%ghost symlink.
- Build into Fedora.

* Fri Jun 10 2005 Gary Benson <gbenson@redhat.com>
- Remove jarfiles and classfiles from the tarball.

* Wed Jun 08 2005 Gary Benson <gbenson@redhat.com>
- Don't build maven stuff.
- Add missing dependency on ant-trax.

* Thu May 05 2005 Fernando Nasser <fnasser@redhat.com> - 0:1.2.2-2jpp_1rh
- Equivalent to 2jpp upstream

* Fri Apr 29 2005 Fernando Nasser <fnasser@redhat.com> - 0:1.2.2-1jpp_7rh
- Rebuild with the docs as maven is now available
- Fix patch to correct xjavadoc building logic
- Don't try and build twice

* Fri Feb 25 2005 Fernando Nasser <fnasser@redhat.com> - 0:1.2.2-1jpp_4rh
- Remove extra file from objectweb module

* Fri Feb 25 2005 Fernando Nasser <fnasser@redhat.com> - 0:1.2.2-1jpp_3rh
- Do not save copies of the java files when patching.

* Thu Feb 24 2005 Fernando Nasser <fnasser@redhat.com> - 0:1.2.2-1jpp_2rh
- Replace JOnAS specific tasks with code blessed by ObjectWeb

* Wed Feb 16 2005 Fernando Nasser <fnasser@redhat.com> - 0:1.2.2-1jpp_1rh
- Merge with upstream for upgrade
- Add patch to prevent attempt to load DTD from the net, when it comes with
  the source and is locally available
- Temporarely disable documentation and mave plugin building for lack of maven

* Tue Feb 15 2005 Ralph Apel <r.apel at r-apel.de> - 0:1.2.2-1jpp
- Upgrade to 1.2.2
- Add jsf requirement for demo
- Drop jndi requirement for demo
- Drop servletapi and mx4j requirement for main package
- Buildrequire maven and use it to build docs

* Fri Oct 15 2004 Fernando Nasser <fnasser@redhat.com> - 0:1.2.1-2jpp_1rh
* First Red Hat build

* Fri Aug 27 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.2.1-2jpp
- Build with ant-1.6.2

* Sat Jul 03 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.2.1-1jpp
- Upgrade to 1.2.1
- Relax build-time dependencies
- Relax dependency versions
- Make subpackage xdoclet-demo optional

* Fri Mar 05 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.2-1jpp
- First JPackage release.

