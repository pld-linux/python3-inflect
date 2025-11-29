#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	Correctly generate plurals, singular nouns, ordinals, indefinite articles
Summary(pl.UTF-8):	Poprawne generowanie liczby mnogiej i pojedynczej, liczebników, przedimków nieokreślonych
Name:		python3-inflect
Version:	7.5.0
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/inflect/
Source0:	https://files.pythonhosted.org/packages/source/i/inflect/inflect-%{version}.tar.gz
# Source0-md5:	2b4c0c942b110c587d8cc1acfb606882
URL:		https://pypi.org/project/inflect/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.9
BuildRequires:	python3-setuptools >= 1:61.2
BuildRequires:	python3-setuptools_scm >= 3.4.1
%if %{with tests}
BuildRequires:	python3-more_itertools >= 8.5.0
BuildRequires:	python3-pygments
BuildRequires:	python3-pytest >= 6
# lint only
#BuildRequires:	python3-pytest-checkdocs >= 2.4
#BuildRequires:	python3-pytest-cov
#BuildRequires:	python3-pytest-enabler >= 2.2
#BuildRequires:	python3-pytest-flake8
#BuildRequires:	python3-pytest-mypy >= 0.9.1
#BuildRequires:	python3-pytest-ruff >= 0.2.1
BuildRequires:	python3-typeguard >= 4.0.1
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-furo
BuildRequires:	python3-jaraco.packaging >= 9.3
BuildRequires:	python3-jaraco.tidelift >= 1.4
BuildRequires:	python3-rst.linker >= 1.9
#BuildRequires:	python3-sphinx-lint
BuildRequires:	sphinx-pdg-3 >= 3.5
%endif
Requires:	python3-modules >= 1:3.9
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Correctly generate plurals, singular nouns, ordinals, indefinite
articles; convert numbers to words.

%description -l pl.UTF-8
Poprawne generowanie liczby mnogiej i pojedynczej, liczebników,
przedimków nieokreślonych; przekształcanie liczb na słowa.

%package apidocs
Summary:	API documentation for Python inflect module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona inflect
Group:		Documentation

%description apidocs
API documentation for Python inflect module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona inflect.

%prep
%setup -q -n inflect-%{version}

%build
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd) \
%{__python3} -m pytest tests
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
sphinx-build-3 -b html docs docs/build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE NEWS.rst README.rst SECURITY.md
%{py3_sitescriptdir}/inflect
%{py3_sitescriptdir}/inflect-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_static,*.html,*.js}
%endif
