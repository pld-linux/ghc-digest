#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	digest
Summary:	Various cryptographic hashes for bytestrings; CRC32 and Adler32 for now
Summary(pl.UTF-8):	Różne kryptograficzne skróty łańcuchów bajtów: CRC32 i Adler32
Name:		ghc-%{pkgname}
Version:	0.0.1.2
Release:	3
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/digest
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	83ed3d8c10d24c88d5ddf4f3914507ac
URL:		http://hackage.haskell.org/package/digest
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 2.2
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-bytestring >= 0.9
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof >= 2.2
BuildRequires:	ghc-base-prof < 5
BuildRequires:	ghc-bytestring-prof >= 0.9
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
BuildRequires:	zlib-devel
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-base >= 2.2
Requires:	ghc-base < 5
Requires:	ghc-bytestring >= 0.9
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
This package provides efficient cryptographic hash implementations for
strict and lazy bytestrings. For now, CRC32 and Adler32 are supported;
they are implemented as FFI bindings to efficient code from zlib.

%description -l pl.UTF-8
Ten pakiet dostarcza wydajne implementacje skrótów kryptograficznych
dla łańcuchów bajtów (bytestringów) ścisłych i leniwych. Na razie
obsługiwane są CRC32 i Adler32; są zaimplementowane jako wiązania FFI
do wydajnego kodu z biblioteki zlib.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 2.2
Requires:	ghc-base-prof < 5
Requires:	ghc-bytestring-prof >= 0.9

%description prof
Profiling %{pkgname} library for GHC. Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%package doc
Summary:	HTML documentation for ghc %{pkgname} package
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}
Group:		Documentation

%description doc
HTML documentation for ghc %{pkgname} package.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc LICENSE
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSdigest-%{version}-*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSdigest-%{version}-*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSdigest-%{version}-*_p.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Digest
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Digest/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Digest/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSdigest-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Digest/*.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
