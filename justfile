default:
  just --list

# install (python) dependencies
install:
  poetry install

# check code style
check:
  ruff .

# fix/format code style
fix:
  ruff . --fix

# generate json schema from the data files, and print to stdout
generate-data-schema:
  #!/usr/bin/env bash
  for filename in data/*.json; do
    [ -e "$filename" ] || continue
    echo "Schema for $filename"
    genson $filename | jq --sort-keys .
  done

# Scrape the portfolio company data
scrape-portfolio-companies-data:
  #!/usr/bin/env bash
  cd scretcher && scrapy crawl portfolio_companies -O ../data/scraped_portfolio_companies.jsonl

# enrich the portfolio data with reference data
enrich-portfolio-data:
  python enricher/src/process_data.py