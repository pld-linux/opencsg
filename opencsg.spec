Summary:	Library for Constructive Solid Geometry using OpenGL
Name:		opencsg
Version:	1.4.0
Release:	1
# license.txt contains a linking exception for CGAL
License:	GPL v2 with exceptions
Group:		Libraries
Source0:	http://www.opencsg.org/OpenCSG-%{version}.tar.gz
# Source0-md5:	e7fe5fa2bfa1b466f470699da41eb0a2
URL:		http://www.opencsg.org/
Patch0:		%{name}-build.patch
BuildRequires:	dos2unix
BuildRequires:	glew-devel
BuildRequires:	libstdc++-devel
BuildRequires:	qt4-qmake
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenCSG is a library that does image-based CSG rendering using OpenGL.

CSG is short for Constructive Solid Geometry and denotes an approach
to model complex 3D-shapes using simpler ones. I.e., two shapes can be
combined by taking the union of them, by intersecting them, or by
subtracting one shape of the other. The most basic shapes, which are
not result of such a CSG operation, are called primitives. Primitives
must be solid, i.e., they must have a clearly defined interior and
exterior. By construction, a CSG shape is also solid then.

Image-based CSG rendering (also z-buffer CSG rendering) is a term that
denotes algorithms for rendering CSG shapes without an explicit
calculation of the geometric boundary of a CSG shape. Such algorithms
use frame-buffer settings of the graphics hardware, e.g., the depth
and stencil buffer, to compose CSG shapes. OpenCSG implements a
variety of those algorithms, namely the Goldfeather algorithm and the
SCS algorithm, both of them in several variants.

%package devel
Summary:	OpenCSG development files
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development files for OpenCSG.

%prep
%setup -q -n OpenCSG-%{version}
%patch0 -p1

rm src/Makefile RenderTexture/Makefile Makefile example/Makefile
dos2unix license.txt
# New FSF Address
for FILE in src/*.h src/*.cpp include/opencsg.h; do
	sed -i s/"59 Temple Place, Suite 330, Boston, MA 02111-1307 USA"/"51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA"/ $FILE
done

# no bundled glew
rm -rf glew

%build
qmake-qt4
%{__make}

rm lib/libopencsg.so.1.4
chmod g-w lib/*

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}}
cp -pP lib/* $RPM_BUILD_ROOT%{_libdir}
cp -p include/opencsg.h $RPM_BUILD_ROOT%{_includedir}

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc changelog.txt doc license.txt
%attr(755,root,root) %{_libdir}/libopencsg.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopencsg.so.1

%files devel
%defattr(644,root,root,755)
%{_includedir}/opencsg.h
%attr(755,root,root) %{_libdir}/libopencsg.so
