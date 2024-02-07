{
  description = "A basic flake with a shell";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShells.default = pkgs.mkShell {
          packages = [
            pkgs.bashInteractive
            pkgs.poetry
            pkgs.just
            pkgs.python311
            pkgs.ruff
            pkgs.python311Packages.scrapy
            pkgs.python311Packages.google-cloud-storage
            pkgs.python311Packages.jsonlines
          ];
        };
      });
}
