{ pkgs ? import <nixpkgs> { } }:

pkgs.mkShell
{
    nativeBuildInputs = with pkgs; [
        (python3.withPackages (ps: [
            ps.pyside6
            ps.pillow
        ]))
    ];

    shellHook = ''
        fish
    '';
}
