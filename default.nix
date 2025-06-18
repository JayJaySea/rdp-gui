{ pkgs ? import <nixpkgs> {} }:

pkgs.python3Packages.buildPythonApplication {
  pname = "rdpgui";
  version = "1.0";
  src = ./.;
  format = "setuptools";

  nativeBuildInputs = with pkgs.python3Packages; [
    setuptools
    wheel
  ];

  propagatedBuildInputs = with pkgs.python3Packages; [
    pyside6
  ];
}
