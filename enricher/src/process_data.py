import pandas as pd
from loguru import logger


def list_agg(values):
    return ", ".join(set(filter(None, values)))


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

    # Clean up the messy investors data field
    funding_data_merged["investors"] = funding_data_merged["investor_names"].str.replace(r'"|{|\\|}', '', regex=True).fillna("")
    return funding_data_merged[single_cols + cols_to_coalesce + ["investors"]]


def load_combined_org_data(base_df):
    # Map to harmonize names between base and 2019 data
    name_map_orgs = {
        "name": "company_name",
        "org_uuid": "company_uuid",
        "funding_rounds": "num_funding_rounds",
        "funding_total_usd": "total_funding_usd",
        "uuid": "company_uuid",
    }

    # These cols will be the same in both tables (or only exists in one)
    single_cols = [
        "company_uuid",
        "description",
    ]

    # Columns to coalesce into a common value
    cols_to_coalesce = [
        "company_name",
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
    org_data = load_and_filter_data(base_df, "data/interview-test-org.json.gz", "name", name_map=name_map_orgs,)
    org_data_2019 = load_and_filter_data(base_df, "data/interview-test-org-2019.json.gz", "company_name", name_map=name_map_orgs,)
    org_data_merged = pd.merge(org_data, org_data_2019, how="outer", on="company_uuid", suffixes=["__base", "__2019"])
    for col in cols_to_coalesce:
        org_data_merged[col] = org_data_merged[col + "__base"].combine_first(org_data_merged[col + "__2019"])
    return org_data_merged[single_cols + cols_to_coalesce]


def create_combined_dataset(base_df, funding_df, org_df):
    # Step 1 - aggregate funding data
    funding_data_grouped = funding_df.groupby("company_name")
    agg_funding_data_rename_map = {
        "announced_on_min": "first_funding_data_f",
        "announced_on_max": "last_funding_date_f",
        "investor_count_sum": "num_investors_f",
        "raised_amount_usd_sum": "raised_amount_usd_f",
        "investors_list_agg": "investors_f",
        "investment_type_list_agg": "investment_types_f",
    }
    agg_funding_data = funding_data_grouped.agg({'announced_on': ['min', 'max'], 'investor_count': 'sum', 'raised_amount_usd': 'sum', 'investors': list_agg, 'investment_type': list_agg,})
    agg_funding_data.columns = ["_".join(a) for a in agg_funding_data.columns.to_flat_index()]
    agg_funding_data = agg_funding_data.rename(agg_funding_data_rename_map, axis=1)

    org_data_rename_map = {
        "description": "description_org",
        "city": "city_org",
        "country_code": "country_code_org",
        "employee_count": "employee_count_org",
        "founded_on": "founded_on_org",
        "homepage_url": "homepage_url_org",
        "last_funding_on": "last_funding_on_org",
        "num_funding_rounds": "num_funding_rounds_org",
        "short_description": "short_description_org",
        "total_funding_usd": "total_funding_usd_org",
    }
    org_data_filtered = org_df.sort_values(["company_name", "last_funding_on"], ascending=False).groupby("company_name").first()
    org_data_filtered = org_data_filtered.rename(org_data_rename_map, axis=1)[list(org_data_rename_map.values())]
    return base_df.join(agg_funding_data, on="company_name", how="left").join(org_data_filtered, on="company_name", how="left")


def write_output(df):
    df.to_json("data/enriched_data.json", orient="records", lines = True)


def main():
    logger.info("Starting enricher")
    logger.info("Loading base data (from scraping)")
    base_df = load_base_df()
    logger.info("Loading and merging funding data")
    funding_data = load_combined_funding_data(base_df)
    logger.info("Loading and merging organization data")
    org_data = load_combined_org_data(base_df)
    logger.info("Processing and combing data")
    output_df = create_combined_dataset(base_df, funding_data, org_data)
    logger.info("Writing output data")
    write_output(output_df)


if __name__ == "__main__":
    main()
