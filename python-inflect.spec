#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Correctly generate plurals, singular nouns, ordinals, indefinite articles
Summary(pl.UTF-8):	Poprawne generowanie liczby mnogiej i pojedynczej, liczebników, przedimków nieokreślonych
Name:		python-inflect
# keep 3.x here for python2 support
Version:	3.0.2
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/inflect/
Source0:	https://files.pythonhosted.org/packages/source/i/inflect/inflect-%{version}.tar.gz
# Source0-md5:	29c60edf9917762e24c3b9aef63701c5
URL:		https://pypi.org/project/inflect/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools >= 1:31.0.1
BuildRequires:	python-setuptools_scm >= 1.15.0
%if %{with tests}
BuildRequires:	python-importlib_metadata
BuildRequires:	python-nose
BuildRequires:	python-pytest >= 3.5
BuildRequires:	python-pytest-black-multipy
#BuildRequires:	python-pytest-checkdocs >= 1.2.3
BuildRequires:	python-pytest-cov
BuildRequires:	python-pytest-flake8
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools >= 1:31.0.1
BuildRequires:	python3-setuptools_scm >= 1.15.0
%if %{with tests}
BuildRequires:	python3-importlib_metadata
BuildRequires:	python3-nose
BuildRequires:	python3-pytest >= 3.5
BuildRequires:	python3-pytest-black-multipy
#BuildRequires:	python3-pytest-checkdocs >= 1.2.3
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-pytest-flake8
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python-jaraco.packaging >= 3.2
BuildRequires:	python-rst.linker >= 1.9
BuildRequires:	sphinx-pdg-2
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Correctly generate plurals, singular nouns, ordinals, indefinite
articles; convert numbers to words.

%description -l pl.UTF-8
Poprawne generowanie liczby mnogiej i pojedynczej, liczebników,
przedimków nieokreślonych; przekształcanie liczb na słowa.

%package -n python3-inflect
Summary:	Correctly generate plurals, singular nouns, ordinals, indefinite articles
Summary(pl.UTF-8):	Poprawne generowanie liczby mnogiej i pojedynczej, liczebników, przedimków nieokreślonych
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-inflect
Correctly generate plurals, singular nouns, ordinals, indefinite
articles; convert numbers to words.

%description -n python3-inflect -l pl.UTF-8
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
%if %{with python2}
%py_build

%if %{with tests}
ln -snf ../tests build-2/tests
cd build-2
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_black_multipy,pytest_flake8,pytest_cov.plugin \
PYTHONPATH=$(echo $(pwd)/lib) \
%{__python} -m pytest tests
cd ..
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
ln -snf ../tests build-2/tests
cd build-3
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_black_multipy,pytest_flake8,pytest_cov.plugin \
PYTHONPATH=$(echo $(pwd)/lib) \
%{__python3} -m pytest tests
cd ..
%endif
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
sphinx-build-2 -b html docs docs/build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE README.rst
%{py_sitescriptdir}/inflect.py[co]
%{py_sitescriptdir}/inflect-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-inflect
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE README.rst
%{py3_sitescriptdir}/inflect.py
%{py3_sitescriptdir}/__pycache__/inflect.cpython-*.py[co]
%{py3_sitescriptdir}/inflect-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_static,*.html,*.js}
%endif
