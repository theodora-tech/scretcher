from enricher.src.process_data import list_agg
import numpy as np


def test_list_agg_with_nulls():
    assert list_agg(["candy", "coffee", "junk", None, ""]) == "candy, coffee, junk"


def test_list_agg_not_sorted():
    assert list_agg(["coffee", "candy", "junk", None, ""]) == "candy, coffee, junk"
