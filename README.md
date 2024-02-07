# Scretcher

A scraper and enricher for portfolio companies of EQT/Motherbrain, built for their code test.

# Installation

This package uses as mix of `nix` packages and `poetry` to handle development and running dependencies.

## Installing Nix (and direnv)

> :information_source: If you already have NixOS installed, just skip ahead.

The preffered way to install system dependencies is to use Nix. If you are feeling bold, a good way to install NixOS is to us the installer as provided by Determinate Systems, read more [here](https://determinate.systems/posts/determinate-nix-installer)

```bash
curl --proto '=https' --tlsv1.2 -sSf -L https://install.determinate.systems/nix | sh -s -- install
```

For `direnv` the easiest way is probably still to use `brew` and install it using a simple `brew install direnv`. Also add the following to your `~/.zshrc`:

```
eval "$(direnv hook zsh)"
```

After this has been done, navigate to the folder, run `direnv allow`. You should se some installation actions happen, and move on to the python-only installations.

## Using Homebrew

TODO Fill me in

## Installing Python-only dependecies

After your dev-shell has been activated, you can now move on to install any other dependecies not handled via Nix by running `just install`.