pkgname = "libcxx-cross"
pkgver = "13.0.0"
pkgrel = 0
build_style = "cmake"
configure_args = [
    "-DCMAKE_BUILD_TYPE=Release", "-Wno-dev",
    "-DCMAKE_C_COMPILER=/usr/bin/clang",
    "-DCMAKE_CXX_COMPILER=/usr/bin/clang++",
    "-DCMAKE_AR=/usr/bin/llvm-ar",
    "-DCMAKE_NM=/usr/bin/llvm-nm",
    "-DCMAKE_RANLIB=/usr/bin/llvm-ranlib",
    "-DLLVM_CONFIG_PATH=/usr/bin/llvm-config",
    "-DLIBCXX_CXX_ABI=libcxxabi",
    "-DLIBCXX_USE_COMPILER_RT=YES",
    "-DLIBCXX_HAS_MUSL_LIBC=YES",
    "-DLIBCXXABI_USE_LLVM_UNWINDER=YES",
    "-DLIBCXX_ENABLE_STATIC_ABI_LIBRARY=YES",
]
make_cmd = "make"
hostmakedepends = ["cmake", "python"]
makedepends = ["libcxxabi-cross", "linux-headers-cross"]
depends = ["libcxxabi-cross"]
pkgdesc = "LLVM libc++ (cross-compiling)"
maintainer = "q66 <q66@chimera-linux.org>"
license = "Apache-2.0"
url = "https://llvm.org"
source = f"https://github.com/llvm/llvm-project/releases/download/llvmorg-{pkgver}/llvm-project-{pkgver}.src.tar.xz"
sha256 = "6075ad30f1ac0e15f07c1bf062c1e1268c241d674f11bd32cdf0e040c71f2bf3"
# crosstoolchain
options = ["!cross", "!check", "!lto", "foreignelf"]

cmake_dir = "libcxx"

_targets = list(filter(
    lambda p: p != self.profile().arch,
    ["aarch64", "ppc64le", "ppc64", "x86_64", "riscv64"]
))

# not available yet, prevent cmake checks
tool_flags = {
    "CFLAGS": ["-fPIC"],
    "CXXFLAGS": ["-fPIC", "-nostdlib"],
}

def do_configure(self):
    from cbuild.util import cmake

    for an in _targets:
        with self.profile(an) as pf:
            at = pf.triplet
            # configure libcxx
            with self.stamp(f"{an}_configure") as s:
                s.check()
                cmake.configure(self, self.cmake_dir, f"build-{an}", [
                    f"-DCMAKE_SYSROOT=/usr/{at}",
                    f"-DCMAKE_ASM_COMPILER_TARGET={at}",
                    f"-DCMAKE_CXX_COMPILER_TARGET={at}",
                    f"-DCMAKE_C_COMPILER_TARGET={at}",
                    f"-DLIBCXX_CXX_ABI_LIBRARY_PATH=/usr/{at}/usr/lib"
                ], cross_build = False)

def do_build(self):
    for an in _targets:
        with self.profile(an):
            with self.stamp(f"{an}_build") as s:
                s.check()
                self.make.build(wrksrc = f"build-{an}")

def do_install(self):
    for an in _targets:
        with self.profile(an) as pf:
            self.make.install(
                ["DESTDIR=" + str(
                    self.chroot_destdir / "usr" / pf.triplet
                )],
                wrksrc = f"build-{an}", default_args = False
            )

def _gen_crossp(an, at):
    @subpackage(f"libcxx-cross-{an}")
    def _subp(self):
        self.pkgdesc = f"{pkgdesc} ({an} support)"
        self.depends = [f"libcxxabi-cross-{an}"]
        self.options = ["!scanshlibs", "!scanrundeps"]
        return [f"usr/{at}"]
    depends.append(f"libcxx-cross-{an}={pkgver}-r{pkgrel}")

for an in _targets:
    with self.profile(an) as pf:
        _gen_crossp(an, pf.triplet)
