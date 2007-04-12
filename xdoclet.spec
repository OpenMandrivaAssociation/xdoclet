%define section free
%define gcj_support 1

# If you do not want to build samples in demo subpackage because of their 
# runtime deps, give rpmbuild option '--without demo'
%define with_demo %{!?_without_demo:1}%{?_without_demo:0}
# We do not ship webwork nor jsf, which are required for the demo
# One can always get the demo subpackage directly from http://jpackage.org
%define with_demo 0

Name:           xdoclet
Version:        1.2.3
Release:        %mkrel 4
Epoch:          0
Summary:        XDoclet Attribute Orientated Programming Framework
License:        BSD-style
Group:          Development/Java
URL:            http://xdoclet.sourceforge.net/xdoclet/index.html
Source0:        http://ovh.dl.sourceforge.net/sourceforge/xdoclet/%{name}-src-%{version}-MDKCLEAN.tar.bz2
Source1:        %{name}-modules-objectweb-4.3.tar.bz2
Patch0:         xdoclet-build_xml.patch
Patch1:         xdoclet-XDocletModulesEjbMessages.patch
Patch2:         xdoclet-ant.not-required.patch
Patch3:         xdoclet-WebLogicSubTask.patch
%if %{gcj_support}
Requires(post): java-gcj-compat
Requires(postun): java-gcj-compat
BuildRequires:  java-gcj-compat-devel
%else
Buildarch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-root
BuildRequires:  java-devel
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  ant >= 0:1.6
# for XMLValidate
BuildRequires:  ant-nodeps >= 0:1.6
# for TraXLiaison
BuildRequires:  ant-trax >= 0:1.6
BuildRequires:  junit
BuildRequires:  javacc
BuildRequires:  jrefactory
BuildRequires:  bsf 
BuildRequires:  jakarta-commons-collections 
BuildRequires:  jakarta-commons-logging 
BuildRequires:  log4j
BuildRequires:  mockobjects 
BuildRequires:  struts 
BuildRequires:  velocity 
BuildRequires:  xalan-j2
BuildRequires:  xml-commons-apis 
BuildRequires:  xjavadoc = 0:1.1
BuildRequires:  ant-trax
Requires:       bsf
Requires:       jakarta-commons-collections
Requires:       jakarta-commons-logging
Requires:       log4j
Requires:       mockobjects
Requires:       velocity
Requires:       xalan-j2
Requires:       xml-commons-apis
Requires:       xjavadoc = 0:1.1

%description
This package contains the XDoclet Attribute Orientated Programming Framework

%if %{with_demo}
%package demo
Summary:        XDoclet Sample Projects
Group:          Development/Java
BuildRequires:  servletapi4
BuildRequires:  struts
BuildRequires:  velocity
BuildRequires:  webwork
BuildRequires:  ejb
BuildRequires:  jsf
BuildRequires:  jms
BuildRequires:  mx4j
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       ejb
Requires:       jsf
Requires:       jms
Requires:       webwork
Requires:       mx4j
Requires:       struts
Requires:       servletapi4

%description demo
This package contains sample XDoclet projects.
%endif

%package javadoc
Summary:        XDoclet Javadoc
Group:          Development/Java

%description javadoc
This package contains XDoclet javadoc

%package manual
Summary:        XDoclet Sample Manuals and Documentation
Group:          Development/Java

%description manual
This package contains XDoclet documentation.

%prep
%setup -q

# Replace JOnAS specific tasks with code blessed by ObjectWeb
pushd modules
mv objectweb objectweb.orig
tar xjf %{SOURCE1}
popd

for j in xjavadoc-1.1 jrefactory javacc junit bsf commons-collections commons-logging log4j velocity xalan-j2 xalan-j2-serializer xjavadoc xml-commons-apis mockobjects-core; do
        ln -s $(build-classpath $j) lib/$j.jar
done

%if %{with_demo}
for j in servletapi4 struts velocity webwork ejb jsf-api jms; do
        ln -s $(build-classpath $j) samples/lib/$j.jar
done
for j in mx4j/mx4j-jmx mx4j/mx4j-tools; do
        i=$(build-classpath $j)
        ln -s $i samples/lib/$(basename $i)
done
%endif

%patch0 -b .sav
%patch1 -b .sav
%patch2
%patch3 -b .sav

%build
export OPT_JAR_LIST="ant/ant-nodeps ant/ant-trax"
# Apparently, symlinking isn't enough to override the default
export CLASSPATH=$(build-classpath xalan-j2 xalan-j2-serializer)
%ant xjavadoc core modules docs l10n

%if %{with_demo}
%ant samples
%endif

%install
%{__rm} -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT%{_javadir}/%{name}
install -m 644 target/lib/xdoclet*.jar $RPM_BUILD_ROOT%{_javadir}/%{name}
(cd $RPM_BUILD_ROOT%{_javadir}/%{name} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

%if %{with_demo}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
cp -pr samples/* $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
%endif

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
# FIXME: javadocs do not build
#cp -pr target/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
rm -rf target/docs/api

mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -p LICENSE.txt $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -pr target/docs/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
    rm -f %{_javadocdir}/%{name}
fi

%files
%defattr(-, root, root, -)
%{_javadir}/%{name}
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif
#%doc %{_docdir}/%{name}-%{version}/LICENSE.txt

%if %{with_demo}
%files demo
%defattr(-, root, root, -)
%{_datadir}/%{name}-%{version}
%endif

%files javadoc
%defattr(-, root, root, -)
%doc %{_javadocdir}/%{name}-%{version}
%ghost %doc %{_javadocdir}/%{name}

%files manual
%defattr(-, root, root, -)
%doc %{_docdir}/%{name}-%{version}


