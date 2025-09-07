import pandas as pd
import numpy as np
import pytest
from finance_tracker_app.core.transactions import Transactions


@pytest.fixture
def sample_df():
    """Creates a simple DataFrame with different currencies and sectors."""
    data = {
        "Currency": ["EUR", "CHF", "CHF", "EUR", "CHF"],
        "Debit":    [100.0, 50.0,  np.nan, 20.0, np.nan],
        "Credit":   [np.nan, np.nan, 30.0, np.nan, np.nan],
        "Amount":   [np.nan, np.nan, np.nan, np.nan, 10.0],
        "Booking text": [
            "NOVAE RESTAURATION",
            "Amazon Purchase",
            "Random Store",
            "Hotel Reservation",
            "Pending Transaction",
        ],
        "Sector": [
            "Restaurants",
            "Department stores",
            "Random Store",
            "Hotels",
            "Airlines",
        ],
    }
    return pd.DataFrame(data)


def test_total_expenses_initialization(sample_df):
    t = Transactions(sample_df, exchange_rate=1.1)
    # Rent always adds 1050
    assert t.total_expenses > 1050


def test_calculate_total_expenses(sample_df):
    chf_rate = 1.06
    expected = (
        sample_df[sample_df["Currency"] == "EUR"]["Debit"].sum()
        + sample_df[sample_df["Currency"] == "CHF"]["Debit"].sum() * chf_rate
    )
    result = Transactions.calculate_total_expenses(sample_df, chf_rate)
    assert pytest.approx(result, rel=1e-2) == expected


def test_analyze_categorizes_expenses(sample_df):
    t = Transactions(sample_df, exchange_rate=1.06)
    t.analyze()

    # Check that known booking texts/sectors are categorized correctly
    assert t.EXP_CATEGORIES["Food at work"] > 0
    assert t.EXP_CATEGORIES["Shopping"] > 0
    assert t.EXP_CATEGORIES["Hotels"] <= 0
    assert t.EXP_CATEGORIES["Transportation"] >= 0
    # Unclassified list should not be empty (Random Store)
    assert len(t.UNCLASSIFIED_EXPENSES) >= 1


def test_check_for_reimbursements(sample_df):
    t = Transactions(sample_df, exchange_rate=1.06)
    row = sample_df.iloc[2].copy()  # NaN Debit, valid Credit
    t.check_for_reimbursements(row)

    assert row["Debit"] == -30.0
    assert t.reimbursements == 30.0


def test_check_pending_transactions(sample_df):
    t = Transactions(sample_df, exchange_rate=1.06)
    row = sample_df.iloc[4].copy()  # NaN Debit and Credit
    t.check_pending_transactions(row)

    assert row["Debit"] == 10.0
    assert t.total_expenses >= 10.0


def test_convert_chf_to_eur(sample_df):
    t = Transactions(sample_df, exchange_rate=1.06)
    row = sample_df.iloc[1].copy()  # CHF row
    original_value = row["Debit"]
    t.convert_chf_to_eur(row)

    assert row["Debit"] == original_value * 1.06


def test_with_dummy_csv(tmp_path):
    """Optional: if you have dummy_data.csv in your project."""
    csv_path = tmp_path / "dummy_data.csv"
    # Minimal CSV for testing
    df = pd.DataFrame({
        "Currency": ["EUR", "CHF"],
        "Debit": [100.0, 50.0],
        "Credit": [np.nan, np.nan],
        "Amount": [np.nan, np.nan],
        "Booking text": ["CERN Restaurant no 1", "Random"],
        "Sector": ["Restaurants", "Pharmacies"],
    })
    df.to_csv(csv_path, index=False)

    df_loaded = pd.read_csv(csv_path)
    t = Transactions(df_loaded, exchange_rate=1.06)
    t.analyze()

    assert "Food at work" in t.EXP_CATEGORIES
    assert isinstance(t.EXP_CATEGORIES["Food at work"], (int, float))
