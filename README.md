# Scretcher

A scraper and enricher for portfolio companies of EQT/Motherbrain, built for their code test.

# Installation

This package can optionally use `nix` with flakes to handle system dependencies and `poetry` to handle python dependencies.

## Installing Nix (and direnv)

> :information_source: If you already have NixOS installed, just skip ahead.

The preffered way to install system dependencies is to use Nix. If you are feeling bold, a good way to install NixOS is to us the installer as provided by Determinate Systems, read more [here](https://determinate.systems/posts/determinate-nix-installer)

```bash
curl --proto '=https' --tlsv1.2 -sSf -L https://install.determinate.systems/nix | sh -s -- install
```

For `direnv` the easiest way is probably still to use `brew` and install it using a simple `brew install direnv`. Also add the following to your `~/.zshrc`:

```bash
eval "$(direnv hook zsh)"
```

After this has been done, navigate to the folder, run `direnv allow`. You should see some installation actions happen.

## Using Homebrew

> :information_source: When using this method, make sure to start poetry shell by running `poetry shell` before running the code.

Run the following commands to install system dependencies with brew.

```bash
brew install bash
brew install just
brew install jq
```

Poetry also needs to be installed, see [here](https://python-poetry.org/docs/#installing-with-pipx) for how to do that.

## Installing Python-only dependecies

After your dev-shell has been activated, you can now move on to install any other dependecies not handled via Nix by running `just install`, or fall back to the `poetry install` command which essentially does the same thing. If you went the nix route, hop in and out of the folder once, to make sure the post-hook that activates the python virtual env can run properly.

# Usage

* **Scrape portfolio companies data** (from the public page): `just scrape-portfolio-companies-data`. This will download the scraped data in jsonlines to the `./data` folder in this repo.
* **Process and enrich the company data**: `just enrich-portfolio-data`

## Test

`just test`

**Note** There is one failing test, because I discovered duplicates too late in the process. Hence why you should always test your data!

# Outputs

The resulting dataset is ouput as a gzipped jsonlines file in the `output/` folder in this repo.

# Limitations

* We assume that company names match exactly, which is fragile, but gets the job done
* The way to get unique organizations from the organization data is very fragile, but gets the job done
* Many configuration values are currently hard-coded, but it shouls be an easy task to change them to be read from config
* The scraping way to find the appropriate data is also fragile, due to the higly nested structure of the source data
