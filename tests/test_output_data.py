import pandas as pd


def test_name_is_unique():
    output_df = pd.read_json("output/enriched_data.json.gz", orient="records", lines=True,)
    assert len(output_df) == len(output_df["company_name"].unique())
