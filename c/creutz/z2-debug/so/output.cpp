// basic file operations
#include <iostream>
#include <fstream>
using namespace std;

int main () {
  ofstream myfile;
  myfile.open ("example.txt");
  myfile << "Writing this to a file.\n";
  myfile.close();
  return 0;
}

// https://cplusplus.com/doc/tutorial/files/

// dantopa@Quaxolotl.local:so $ date
// Fri Oct 20 20:22:10 MDT 2023

// dantopa@Quaxolotl.local:so $ pwd
// /Volumes/T7-Touch/repos/github/jop/c/creutz/z2-debug/so

// dantopa@Quaxolotl.local:so $ gcc -v
// Using built-in specs.
// COLLECT_GCC=gcc
// COLLECT_LTO_WRAPPER=/opt/local/libexec/gcc/x86_64-apple-darwin23/13.2.0/lto-wrapper
// Target: x86_64-apple-darwin23
// Configured with: /opt/local/var/macports/build/_opt_local_var_macports_sources_rsync.macports.org_macports_release_tarballs_ports_lang_gcc13/gcc13/work/gcc-13.2.0/configure --prefix=/opt/local --build=x86_64-apple-darwin23 --enable-languages=c,c++,objc,obj-c++,lto,fortran,jit --libdir=/opt/local/lib/gcc13 --includedir=/opt/local/include/gcc13 --infodir=/opt/local/share/info --mandir=/opt/local/share/man --datarootdir=/opt/local/share/gcc-13 --with-local-prefix=/opt/local --with-system-zlib --disable-nls --program-suffix=-mp-13 --with-gxx-include-dir=/opt/local/include/gcc13/c++/ --with-gmp=/opt/local --with-mpfr=/opt/local --with-mpc=/opt/local --with-isl=/opt/local --with-zstd=/opt/local --enable-checking=release --disable-multilib --enable-lto --enable-libstdcxx-time --with-build-config=bootstrap-debug --with-as=/opt/local/bin/as --with-ld=/opt/local/bin/ld-classic --with-ar=/opt/local/bin/ar --with-bugurl=https://trac.macports.org/newticket --enable-host-shared --with-darwin-extra-rpath=/opt/local/lib/libgcc --with-libiconv-prefix=/opt/local --disable-tls --with-gxx-libcxx-include-dir=/opt/local/libexec/gcc13/libc++/include/c++/v1 --with-pkgversion='MacPorts gcc13 13.2.0_3+stdlib_flag' --with-sysroot=/Library/Developer/CommandLineTools/SDKs/MacOSX14.sdk
// Thread model: posix
// Supported LTO compression algorithms: zlib zstd
// gcc version 13.2.0 (MacPorts gcc13 13.2.0_3+stdlib_flag) 

// dantopa@Quaxolotl.local:so $ gcc output.cpp -lstdc++

// dantopa@Quaxolotl.local:so $ ./a.out 
