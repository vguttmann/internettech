with import <nixpkgs> {};

stdenv.mkDerivation {
  name = "node";
  buildInputs = [
    nodejs_22
    yarn-berry
    python311
  ];
  shellHook = ''
    export PATH="$PWD/node_modules/.bin/:$PATH"
  '';
}
