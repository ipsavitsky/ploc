_: {
  projectRootFile = "flake.nix";
  programs.shfmt.enable = true;
  programs.nixfmt.enable = true;
  programs.statix.enable = true;
  programs.deadnix.enable = true;
  programs.taplo.enable = true;
  programs.ruff-format.enable = true;
  programs.ruff-check.enable = true;
}
