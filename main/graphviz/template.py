pkgname = "graphviz"
pkgver = "6.0.1"
pkgrel = 0
build_style = "gnu_configure"
configure_args = [
    "--disable-lefty"
]
make_cmd = "gmake"
# otherwise y.tab.h is not located
make_dir = "."
make_install_args = ["-j1"]
hostmakedepends = [
    "gmake", "pkgconf", "automake", "libtool", "libltdl-devel", "flex",
    "bison", "perl", "python"
]
makedepends = [
    "libpng-devel", "libjpeg-turbo-devel", "libwebp-devel", "libgd-devel",
    "zlib-devel", "libexpat-devel", "fontconfig-devel", "cairo-devel",
    "pango-devel", "freetype-devel",
]
checkdepends = ["fonts-liberation-otf"]
depends = ["fonts-liberation"]
triggers = ["/usr/lib/graphviz"]
pkgdesc = "Graph visualization software"
maintainer = "q66 <q66@chimera-linux.org>"
license = "EPL-1.0"
url = "https://graphviz.org"
source = f"https://gitlab.com/{pkgname}/{pkgname}/-/archive/{pkgver}/{pkgname}-{pkgver}.tar.gz"
sha256 = "92a5cabb71c2610ffb713f0da7ee595fa143f3fae5eaff172927dd27355d9775"
# expects already installed graphviz
# testing is via pytest
options = ["!check"]

def init_configure(self):
    self.make_build_args += ["HOSTCC=" + self.get_tool("CC")]

def pre_configure(self):
    self.do(self.chroot_cwd / "autogen.sh")

def post_install(self):
    self.install_license("epl-v10.txt")
    # useless
    self.rm(self.destdir / "usr/bin/dot_builtins")

@subpackage("graphviz-libs")
def _libs(self):
    return self.default_libs()

@subpackage("graphviz-devel")
def _devel(self):
    return self.default_devel()
