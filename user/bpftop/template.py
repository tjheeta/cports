pkgname = "bpftop"
pkgver = "0.5.1"
pkgrel = 0
build_style = "cargo"
hostmakedepends = [
    "cargo",
    "pkgconf",
]
makedepends = [
    "libbpf-devel",
    "rust-std",
]
pkgdesc = "TUI view for running BPF programs"
maintainer = "psykose <alice@ayaya.dev>"
license = "Apache-2.0"
url = "https://github.com/Netflix/bpftop"
source = f"{url}/archive/refs/tags/v{pkgver}.tar.gz"
sha256 = "8457caf5ededba38aad01ed6317bd737a8079bbb26ca9a79cfdca5848a8c80f6"


def do_prepare(self):
    # we patch the lockfile so vendor after patch
    pass


def post_patch(self):
    from cbuild.util import cargo

    self.cargo.vendor()
    cargo.setup_vendor(self)


def do_install(self):
    self.install_bin(f"target/{self.profile().triplet}/release/bpftop")
