import json
from pathlib import Path

import pandas as pd
import pytest


@pytest.fixture
def batting_stats_fixture():
    """Load batting stats fixture data"""
    fixture_path = Path(__file__).parent / "fixtures" / "batting_stats_fixture.json"
    with open(fixture_path, "r") as f:
        return json.load(f)


@pytest.fixture
def pitching_stats_fixture():
    """Load pitching stats fixture data"""
    fixture_path = Path(__file__).parent / "fixtures" / "pitching_stats_fixture.json"
    with open(fixture_path, "r") as f:
        return json.load(f)


@pytest.fixture
def team_batting_stats_fixture():
    """Load team batting stats fixture data"""
    fixture_path = (
        Path(__file__).parent / "fixtures" / "team_batting_stats_fixture.json"
    )
    with open(fixture_path, "r") as f:
        return json.load(f)


@pytest.fixture
def team_pitching_stats_fixture():
    """Load team pitching stats fixture data"""
    fixture_path = (
        Path(__file__).parent / "fixtures" / "team_pitching_stats_fixture.json"
    )
    with open(fixture_path, "r") as f:
        return json.load(f)


@pytest.fixture
def standings_fixture():
    """Load standings fixture data (list of division DataFrames)"""
    fixture_path = Path(__file__).parent / "fixtures" / "standings_fixture.json"
    with open(fixture_path, "r") as f:
        data = json.load(f)
    # Convert each division's list of dicts into a DataFrame (matches pybaseball output)
    return [pd.DataFrame(division) for division in data]
