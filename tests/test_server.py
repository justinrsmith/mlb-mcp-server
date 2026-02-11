import json
from pathlib import Path
from unittest.mock import patch

import pandas as pd
import pytest

from mlb_mcp_server.server import (
    batting_stats_by_year,
    pitching_stats_by_year,
)


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


@patch("mlb_mcp_server.server.batting_stats")
def test_batting_stats_by_year(mock_batting_stats, batting_stats_fixture):
    mock_batting_stats.return_value = pd.DataFrame(batting_stats_fixture)

    result = batting_stats_by_year(2023)

    # Assert - Response structure
    assert "year" in result
    assert "total_rows" in result
    assert "page" in result
    assert "page_size" in result
    assert "data" in result

    # Assert - Response values
    assert result["year"] == 2023
    assert result["total_rows"] == len(batting_stats_fixture)
    assert result["page"] == 1
    assert result["page_size"] == 10
    assert len(result["data"]) == len(batting_stats_fixture)

    # Assert - Data content (verify Pydantic worked)
    assert isinstance(result["data"], list)
    assert len(result["data"]) > 0
    first_player = result["data"][0]
    assert "Name" in first_player
    assert "Team" in first_player
    assert "HR" in first_player

    # Assert - Default uses "basic" field filtering
    # Should have fewer fields than if "all" was used
    assert len(first_player) < 40  # Basic has ~23 fields, all would have 100+

    # Assert - Mock was called correctly
    mock_batting_stats.assert_called_once_with(2023)


@patch("mlb_mcp_server.server.pitching_stats")
def test_pitching_stats_by_year(mock_pitching_stats, pitching_stats_fixture):
    mock_pitching_stats.return_value = pd.DataFrame(pitching_stats_fixture)

    result = pitching_stats_by_year(2023)

    # Assert - Response structure
    assert "year" in result
    assert "total_rows" in result
    assert "page" in result
    assert "page_size" in result
    assert "data" in result

    # Assert - Response values
    assert result["year"] == 2023
    assert result["total_rows"] == len(pitching_stats_fixture)
    assert result["page"] == 1
    assert result["page_size"] == 10
    assert len(result["data"]) == len(pitching_stats_fixture)

    # Assert - Data content (verify Pydantic worked)
    assert isinstance(result["data"], list)
    assert len(result["data"]) > 0
    first_player = result["data"][0]
    assert "Name" in first_player
    assert "Team" in first_player
    assert "W" in first_player

    # Assert - Mock was called correctly
    mock_pitching_stats.assert_called_once_with(2023)


@patch("mlb_mcp_server.server.batting_stats")
def test_fetch_stats_by_year_empty_data(mock_batting_stats):
    """Test _fetch_stats_by_year with empty DataFrame"""
    mock_batting_stats.return_value = pd.DataFrame()  # Empty DataFrame

    result = batting_stats_by_year(2023)

    assert result["year"] == 2023
    assert result["total_rows"] == 0
    assert result["page"] == 1
    assert result["page_size"] == 10
    assert result["data"] == []
    mock_batting_stats.assert_called_once_with(2023)


@patch("mlb_mcp_server.server.batting_stats")
def test_fetch_stats_by_year_exception(mock_batting_stats):
    """Test _fetch_stats_by_year when stats_func raises an exception"""
    mock_batting_stats.side_effect = Exception("Data fetch error")

    result = batting_stats_by_year(2023)

    assert "error" in result
    assert result["error"] == "Data fetch error"
    mock_batting_stats.assert_called_once_with(2023)


@patch("mlb_mcp_server.server.batting_stats")
def test_fetch_stats_by_year_no_more_pages(mock_batting_stats, batting_stats_fixture):
    """Test _fetch_stats_by_year when requesting a page beyond available data"""
    mock_batting_stats.return_value = pd.DataFrame(batting_stats_fixture)

    # Assuming fixture has 10 records, page_size=5 means 2 pages total
    result = batting_stats_by_year(2023, page=3, page_size=5)

    assert result["year"] == 2023
    assert result["total_rows"] == len(batting_stats_fixture)
    assert result["page"] == 3
    assert result["page_size"] == 5
    assert result["data"] == []  # No more data on page 3
    mock_batting_stats.assert_called_once_with(2023)


@patch("mlb_mcp_server.server.batting_stats")
def test_batting_stats_field_filtering_basic(mock_batting_stats, batting_stats_fixture):
    """Test field filtering with 'basic' preset"""
    mock_batting_stats.return_value = pd.DataFrame(batting_stats_fixture)

    result = batting_stats_by_year(2023, fields="basic")

    assert len(result["data"]) > 0
    first_player = result["data"][0]

    # Should always include IDfg and Season
    assert "IDfg" in first_player
    assert "Season" in first_player

    # Should include basic fields
    assert "Name" in first_player
    assert "Team" in first_player
    assert "HR" in first_player
    assert "AVG" in first_player
    assert "OPS" in first_player
    assert "RBI" in first_player

    # Should have significantly fewer fields than 'all'
    # Basic preset has ~21 fields + IDfg + Season = ~23 fields
    assert len(first_player) < 30


@patch("mlb_mcp_server.server.batting_stats")
def test_batting_stats_field_filtering_advanced(
    mock_batting_stats, batting_stats_fixture
):
    """Test field filtering with 'advanced' preset"""
    mock_batting_stats.return_value = pd.DataFrame(batting_stats_fixture)

    result = batting_stats_by_year(2023, fields="advanced")

    assert len(result["data"]) > 0
    first_player = result["data"][0]

    # Should always include IDfg and Season
    assert "IDfg" in first_player
    assert "Season" in first_player

    # Should include advanced fields
    assert "Name" in first_player
    assert "Team" in first_player
    assert "WAR" in first_player
    assert (
        "wOBA" in first_player or "wRC+" in first_player
    )  # At least one advanced metric


@patch("mlb_mcp_server.server.batting_stats")
def test_batting_stats_field_filtering_statcast(
    mock_batting_stats, batting_stats_fixture
):
    """Test field filtering with 'statcast' preset"""
    mock_batting_stats.return_value = pd.DataFrame(batting_stats_fixture)

    result = batting_stats_by_year(2023, fields="statcast")

    assert len(result["data"]) > 0
    first_player = result["data"][0]

    # Should always include IDfg and Season
    assert "IDfg" in first_player
    assert "Season" in first_player

    # Should include statcast fields
    assert "Name" in first_player
    assert "Team" in first_player
    # Statcast fields may not all be in fixture, but structure should be there


@patch("mlb_mcp_server.server.batting_stats")
def test_batting_stats_field_filtering_custom(
    mock_batting_stats, batting_stats_fixture
):
    """Test field filtering with custom field list"""
    mock_batting_stats.return_value = pd.DataFrame(batting_stats_fixture)

    result = batting_stats_by_year(2023, fields="Name,Team,HR,AVG,WAR")

    assert len(result["data"]) > 0
    first_player = result["data"][0]

    # Should always include IDfg and Season
    assert "IDfg" in first_player
    assert "Season" in first_player

    # Should include requested fields
    assert "Name" in first_player
    assert "Team" in first_player
    assert "HR" in first_player

    # Should have exactly the requested fields plus IDfg and Season
    # Expected: IDfg, Season, Name, Team, HR, AVG, WAR (if WAR exists in fixture)
    assert len(first_player) <= 7


@patch("mlb_mcp_server.server.batting_stats")
def test_batting_stats_field_filtering_all(mock_batting_stats, batting_stats_fixture):
    """Test field filtering with 'all' to return all fields"""
    mock_batting_stats.return_value = pd.DataFrame(batting_stats_fixture)

    result = batting_stats_by_year(2023, fields="all", page_size=1)

    assert len(result["data"]) > 0
    first_player = result["data"][0]

    # Should include many fields (all non-null fields from fixture)
    assert "Name" in first_player
    assert "Team" in first_player
    # The exact number depends on the fixture, but should be substantial
    # With exclude_none=True, this will vary, but should be more than basic
    assert len(first_player) > 20


@patch("mlb_mcp_server.server.pitching_stats")
def test_pitching_stats_field_filtering_basic(
    mock_pitching_stats, pitching_stats_fixture
):
    """Test field filtering with 'basic' preset for pitching"""
    mock_pitching_stats.return_value = pd.DataFrame(pitching_stats_fixture)

    result = pitching_stats_by_year(2023, fields="basic")

    assert len(result["data"]) > 0
    first_player = result["data"][0]

    # Should always include IDfg and Season
    assert "IDfg" in first_player
    assert "Season" in first_player

    # Should include basic pitching fields
    assert "Name" in first_player
    assert "Team" in first_player
    assert "ERA" in first_player
    assert "IP" in first_player
    assert "WHIP" in first_player
    assert "SO" in first_player


@patch("mlb_mcp_server.server.pitching_stats")
def test_pitching_stats_field_filtering_advanced(
    mock_pitching_stats, pitching_stats_fixture
):
    """Test field filtering with 'advanced' preset for pitching"""
    mock_pitching_stats.return_value = pd.DataFrame(pitching_stats_fixture)

    result = pitching_stats_by_year(2023, fields="advanced")

    assert len(result["data"]) > 0
    first_player = result["data"][0]

    # Should always include IDfg and Season
    assert "IDfg" in first_player
    assert "Season" in first_player

    # Should include advanced pitching fields
    assert "Name" in first_player
    assert "Team" in first_player
    assert (
        "FIP" in first_player or "xFIP" in first_player
    )  # At least one advanced metric
    assert "WAR" in first_player


@patch("mlb_mcp_server.server.pitching_stats")
def test_pitching_stats_field_filtering_custom(
    mock_pitching_stats, pitching_stats_fixture
):
    """Test field filtering with custom fields for pitching"""
    mock_pitching_stats.return_value = pd.DataFrame(pitching_stats_fixture)

    result = pitching_stats_by_year(2023, fields="Name,Team,ERA,WHIP")

    assert len(result["data"]) > 0
    first_player = result["data"][0]

    # Should always include IDfg and Season
    assert "IDfg" in first_player
    assert "Season" in first_player

    # Should include requested fields
    assert "Name" in first_player
    assert "Team" in first_player
    assert "ERA" in first_player
    assert "WHIP" in first_player

    # Should have limited fields
    assert len(first_player) <= 6


@patch("mlb_mcp_server.server.batting_stats")
def test_field_filtering_reduces_payload_size(
    mock_batting_stats, batting_stats_fixture
):
    """Test that field filtering actually reduces payload size"""
    mock_batting_stats.return_value = pd.DataFrame(batting_stats_fixture)

    # Get results with different field settings
    result_all = batting_stats_by_year(2023, fields="all", page_size=3)
    result_basic = batting_stats_by_year(2023, fields="basic", page_size=3)
    result_custom = batting_stats_by_year(2023, fields="Name,Team,HR", page_size=3)

    # All should have the same number of records
    assert len(result_all["data"]) == len(result_basic["data"])
    assert len(result_all["data"]) == len(result_custom["data"])

    # But basic should have fewer fields than all
    if len(result_all["data"]) > 0:
        all_fields = len(result_all["data"][0])
        basic_fields = len(result_basic["data"][0])
        custom_fields = len(result_custom["data"][0])

        assert basic_fields < all_fields
        assert custom_fields < basic_fields
        assert custom_fields <= 5  # Name, Team, HR + IDfg, Season
