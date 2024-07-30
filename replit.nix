{pkgs}: {
  deps = [
    pkgs.rustc
    pkgs.libiconv
    pkgs.cargo
    pkgs.gettext
    pkgs.glibcLocales
  ];
}
