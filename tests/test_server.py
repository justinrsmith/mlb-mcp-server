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
    assert result["page_size"] == 25
    assert len(result["data"]) == len(batting_stats_fixture)

    # Assert - Data content (verify Pydantic worked)
    assert isinstance(result["data"], list)
    assert len(result["data"]) > 0
    first_player = result["data"][0]
    assert "Name" in first_player
    assert "Team" in first_player
    assert "HR" in first_player

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
    assert result["page_size"] == 25
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
    assert result["page_size"] == 25
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
