import json
from pathlib import Path

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
