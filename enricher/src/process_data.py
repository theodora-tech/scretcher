import pandas as pd


def load_base_df(path="data/scraped_portfolio_companies.jsonl"):
    """Load the base data, e.g. the output of the scraper"""
    df = pd.read_json(path, orient="records", lines=True)
    df["funds"] =  df["fund"].str.join(", ")
    del df["fund"]

    return df


def load_and_filter_data(base_df, path, col_to_filter="name", name_map=None):
    """Generic functon that loads json from a the reference data and filters out only portfolio companies"""
    name_map = name_map if name_map is not None else {}
    org_df = pd.read_json(path, orient="records", lines=True)

    filtered_org_data = org_df[org_df[col_to_filter].isin(base_df["company_name"])].rename(name_map, axis=1)

    return filtered_org_data


def load_combined_funding_data(base_df):
    """Load both funding data sources and combine them into one cleaner data set"""

    # Map to harmonize names between base and 2019 data
    name_map_funding = {
        "org_name": "company_name",
        "org_uuid": "company_uuid",
        "raised_amount_usd": "raised_amount_usd",
        "uuid": "funding_round_uuid",
    }

    # These cols will be the same in both tables (or only exists in one)
    single_cols = [
        "investor_names",
        "funding_round_uuid",
    ]

    # Cols that exists in both data sources
    cols_to_coalesce = [
        "announced_on",
        "investment_type",
        "investor_count",
        "company_name",
        "company_uuid",
        "raised_amount_usd",
    ]

    funding_data = load_and_filter_data(base_df, "data/interview-test-funding.json.gz", "org_name", name_map=name_map_funding)
    funding_data_2019 = load_and_filter_data(base_df, "data/interview-test-funding-2019.json.gz", "company_name", name_map=name_map_funding)
    funding_data_merged = pd.merge(funding_data, funding_data_2019, how="outer", on="funding_round_uuid", suffixes=["__base", "__2019"])
    for col in cols_to_coalesce:
        funding_data_merged[col] = funding_data_merged[col + "__base"].combine_first(funding_data_merged[col + "__2019"])

    return funding_data_merged[single_cols + cols_to_coalesce]


def load_combined_org_data(base_df):
    # Map to harmonize names between base and 2019 data
    name_map_orgs = {
        "name": "company_name",
        "org_uuid": "company_uuid",
        "funding_rounds": "num_funding_rounds",
        "funding_total_usd": "total_funding_usd",
    }

    # Columns to coalesce into a common value
    cols_to_coalesce = [
        "city",
        "country_code",
        "employee_count",
        "founded_on",
        "homepage_url",
        "last_funding_on",
        "num_funding_rounds",
        "short_description",
        "total_funding_usd",
    ]
    org_data = load_and_filter_data(base_df, f"data/interview-test-org.json.gz", "name", name_map=name_map_orgs)
    org_data_2019 = load_and_filter_data(base_df, f"data/interview-test-org-2019.json.gz", "company_name", name_map=name_map_orgs)
    org_data_merged = pd.merge(org_data, org_data_2019, how="outer", on="uuid", suffixes=["__base", "__2019"])
    for col in cols_to_coalesce:
        org_data_merged[col] = org_data_merged[col + "__base"].combine_first(org_data_merged[col + "__2019"])

    return org_data


def create_combined_dataset():
    pass


def write_output(df):
    pass


def main():
    base_df = load_base_df()
    funding_data = load_combined_funding_data(base_df)
    org_data = load_combined_org_data(base_df)


if __name__ == "__main__":
    main()
