from unittest.mock import patch

import pandas as pd

from mlb_mcp_server.server import (
    batting_stats_by_year,
    pitching_stats_by_year,
    team_batting_stats_by_year,
    team_pitching_stats_by_year,
)


class TestBattingStats:
    @patch("mlb_mcp_server.server.batting_stats")
    async def test_basic_response(self, mock_batting_stats, batting_stats_fixture):
        mock_batting_stats.return_value = pd.DataFrame(batting_stats_fixture)

        result = await batting_stats_by_year(2023)

        assert result["year"] == 2023
        assert result["total_rows"] == len(batting_stats_fixture)
        assert result["page"] == 1
        assert result["page_size"] == 10
        assert len(result["data"]) == len(batting_stats_fixture)

        assert isinstance(result["data"], list)
        assert len(result["data"]) > 0
        first_player = result["data"][0]
        assert "Name" in first_player
        assert "Team" in first_player
        assert "HR" in first_player
        assert len(first_player) < 40

        mock_batting_stats.assert_called_once_with(2023)

    @patch("mlb_mcp_server.server.batting_stats")
    async def test_empty_data(self, mock_batting_stats):
        mock_batting_stats.return_value = pd.DataFrame()

        result = await batting_stats_by_year(2023)

        assert result["year"] == 2023
        assert result["total_rows"] == 0
        assert result["page"] == 1
        assert result["page_size"] == 10
        assert result["data"] == []
        mock_batting_stats.assert_called_once_with(2023)

    @patch("mlb_mcp_server.server.batting_stats")
    async def test_exception(self, mock_batting_stats):
        mock_batting_stats.side_effect = Exception("Data fetch error")

        result = await batting_stats_by_year(2023)

        assert "error" in result
        assert result["error"] == "Data fetch error"
        mock_batting_stats.assert_called_once_with(2023)

    @patch("mlb_mcp_server.server.batting_stats")
    async def test_no_more_pages(self, mock_batting_stats, batting_stats_fixture):
        mock_batting_stats.return_value = pd.DataFrame(batting_stats_fixture)

        result = await batting_stats_by_year(2023, page=3, page_size=5)

        assert result["year"] == 2023
        assert result["total_rows"] == len(batting_stats_fixture)
        assert result["page"] == 3
        assert result["page_size"] == 5
        assert result["data"] == []
        mock_batting_stats.assert_called_once_with(2023)

    @patch("mlb_mcp_server.server.batting_stats")
    async def test_field_filtering_basic(
        self, mock_batting_stats, batting_stats_fixture
    ):
        mock_batting_stats.return_value = pd.DataFrame(batting_stats_fixture)

        result = await batting_stats_by_year(2023, fields="basic")

        assert len(result["data"]) > 0
        first_player = result["data"][0]

        assert "IDfg" in first_player
        assert "Season" in first_player
        assert "Name" in first_player
        assert "Team" in first_player
        assert "HR" in first_player
        assert "AVG" in first_player
        assert "OPS" in first_player
        assert "RBI" in first_player
        assert len(first_player) < 30

    @patch("mlb_mcp_server.server.batting_stats")
    async def test_field_filtering_advanced(
        self, mock_batting_stats, batting_stats_fixture
    ):
        mock_batting_stats.return_value = pd.DataFrame(batting_stats_fixture)

        result = await batting_stats_by_year(2023, fields="advanced")

        assert len(result["data"]) > 0
        first_player = result["data"][0]

        assert "IDfg" in first_player
        assert "Season" in first_player
        assert "Name" in first_player
        assert "Team" in first_player
        assert "WAR" in first_player
        assert "wOBA" in first_player or "wRC+" in first_player

    @patch("mlb_mcp_server.server.batting_stats")
    async def test_field_filtering_statcast(
        self, mock_batting_stats, batting_stats_fixture
    ):
        mock_batting_stats.return_value = pd.DataFrame(batting_stats_fixture)

        result = await batting_stats_by_year(2023, fields="statcast")

        assert len(result["data"]) > 0
        first_player = result["data"][0]

        assert "IDfg" in first_player
        assert "Season" in first_player
        assert "Name" in first_player
        assert "Team" in first_player

    @patch("mlb_mcp_server.server.batting_stats")
    async def test_field_filtering_custom(
        self, mock_batting_stats, batting_stats_fixture
    ):
        mock_batting_stats.return_value = pd.DataFrame(batting_stats_fixture)

        result = await batting_stats_by_year(2023, fields="Name,Team,HR,AVG,WAR")

        assert len(result["data"]) > 0
        first_player = result["data"][0]

        assert "IDfg" in first_player
        assert "Season" in first_player
        assert "Name" in first_player
        assert "Team" in first_player
        assert "HR" in first_player
        assert len(first_player) <= 7

    @patch("mlb_mcp_server.server.batting_stats")
    async def test_field_filtering_all(self, mock_batting_stats, batting_stats_fixture):
        mock_batting_stats.return_value = pd.DataFrame(batting_stats_fixture)

        result = await batting_stats_by_year(2023, fields="all", page_size=1)

        assert len(result["data"]) > 0
        first_player = result["data"][0]

        assert "Name" in first_player
        assert "Team" in first_player
        assert len(first_player) > 20

    @patch("mlb_mcp_server.server.batting_stats")
    async def test_field_filtering_reduces_payload_size(
        self, mock_batting_stats, batting_stats_fixture
    ):
        mock_batting_stats.return_value = pd.DataFrame(batting_stats_fixture)

        result_all = await batting_stats_by_year(2023, fields="all", page_size=3)
        result_basic = await batting_stats_by_year(2023, fields="basic", page_size=3)
        result_custom = await batting_stats_by_year(
            2023, fields="Name,Team,HR", page_size=3
        )

        assert len(result_all["data"]) == len(result_basic["data"])
        assert len(result_all["data"]) == len(result_custom["data"])

        if len(result_all["data"]) > 0:
            all_fields = len(result_all["data"][0])
            basic_fields = len(result_basic["data"][0])
            custom_fields = len(result_custom["data"][0])

            assert basic_fields < all_fields
            assert custom_fields < basic_fields
            assert custom_fields <= 5


class TestPitchingStats:
    @patch("mlb_mcp_server.server.pitching_stats")
    async def test_basic_response(self, mock_pitching_stats, pitching_stats_fixture):
        mock_pitching_stats.return_value = pd.DataFrame(pitching_stats_fixture)

        result = await pitching_stats_by_year(2023)

        assert result["year"] == 2023
        assert result["total_rows"] == len(pitching_stats_fixture)
        assert result["page"] == 1
        assert result["page_size"] == 10
        assert len(result["data"]) == len(pitching_stats_fixture)

        assert isinstance(result["data"], list)
        assert len(result["data"]) > 0
        first_player = result["data"][0]
        assert "Name" in first_player
        assert "Team" in first_player
        assert "W" in first_player

        mock_pitching_stats.assert_called_once_with(2023)

    @patch("mlb_mcp_server.server.pitching_stats")
    async def test_field_filtering_basic(
        self, mock_pitching_stats, pitching_stats_fixture
    ):
        mock_pitching_stats.return_value = pd.DataFrame(pitching_stats_fixture)

        result = await pitching_stats_by_year(2023, fields="basic")

        assert len(result["data"]) > 0
        first_player = result["data"][0]

        assert "IDfg" in first_player
        assert "Season" in first_player
        assert "Name" in first_player
        assert "Team" in first_player
        assert "ERA" in first_player
        assert "IP" in first_player
        assert "WHIP" in first_player
        assert "SO" in first_player

    @patch("mlb_mcp_server.server.pitching_stats")
    async def test_field_filtering_advanced(
        self, mock_pitching_stats, pitching_stats_fixture
    ):
        mock_pitching_stats.return_value = pd.DataFrame(pitching_stats_fixture)

        result = await pitching_stats_by_year(2023, fields="advanced")

        assert len(result["data"]) > 0
        first_player = result["data"][0]

        assert "IDfg" in first_player
        assert "Season" in first_player
        assert "Name" in first_player
        assert "Team" in first_player
        assert "FIP" in first_player or "xFIP" in first_player
        assert "WAR" in first_player

    @patch("mlb_mcp_server.server.pitching_stats")
    async def test_field_filtering_custom(
        self, mock_pitching_stats, pitching_stats_fixture
    ):
        mock_pitching_stats.return_value = pd.DataFrame(pitching_stats_fixture)

        result = await pitching_stats_by_year(2023, fields="Name,Team,ERA,WHIP")

        assert len(result["data"]) > 0
        first_player = result["data"][0]

        assert "IDfg" in first_player
        assert "Season" in first_player
        assert "Name" in first_player
        assert "Team" in first_player
        assert "ERA" in first_player
        assert "WHIP" in first_player
        assert len(first_player) <= 6


class TestTeamBattingStats:
    @patch("mlb_mcp_server.server.team_batting")
    async def test_basic_response(self, mock_team_batting, team_batting_stats_fixture):
        mock_team_batting.return_value = pd.DataFrame(team_batting_stats_fixture)

        result = await team_batting_stats_by_year(2023)

        assert result["year"] == 2023
        assert result["total_rows"] == len(team_batting_stats_fixture)
        assert result["page"] == 1
        assert result["page_size"] == 10
        assert len(result["data"]) == 10

        assert isinstance(result["data"], list)
        assert len(result["data"]) > 0

        mock_team_batting.assert_called_once_with(2023)

    @patch("mlb_mcp_server.server.team_batting")
    async def test_field_filtering_basic(
        self, mock_team_batting, team_batting_stats_fixture
    ):
        mock_team_batting.return_value = pd.DataFrame(team_batting_stats_fixture)

        result = await team_batting_stats_by_year(2023, fields="basic")

        assert len(result["data"]) > 0
        first_team = result["data"][0]

        assert "teamIDfg" in first_team
        assert "Season" in first_team
        assert "Team" in first_team
        assert "G" in first_team
        assert "AB" in first_team
        assert "H" in first_team
        assert "HR" in first_team
        assert "AVG" in first_team
        assert "OPS" in first_team

        # Should NOT include pitching-only fields
        assert "ERA" not in first_team
        assert "W" not in first_team
        assert "WHIP" not in first_team


class TestTeamPitchingStats:
    @patch("mlb_mcp_server.server.team_pitching")
    async def test_basic_response(
        self, mock_team_pitching, team_pitching_stats_fixture
    ):
        mock_team_pitching.return_value = pd.DataFrame(team_pitching_stats_fixture)

        result = await team_pitching_stats_by_year(2023)

        assert result["year"] == 2023
        assert result["total_rows"] == len(team_pitching_stats_fixture)
        assert result["page"] == 1
        assert result["page_size"] == 10
        assert len(result["data"]) == 10

        assert isinstance(result["data"], list)
        assert len(result["data"]) > 0

        mock_team_pitching.assert_called_once_with(2023)

    @patch("mlb_mcp_server.server.team_pitching")
    async def test_field_filtering_basic(
        self, mock_team_pitching, team_pitching_stats_fixture
    ):
        mock_team_pitching.return_value = pd.DataFrame(team_pitching_stats_fixture)

        result = await team_pitching_stats_by_year(2023, fields="basic")

        assert len(result["data"]) > 0
        first_team = result["data"][0]

        assert "teamIDfg" in first_team
        assert "Season" in first_team
        assert "Team" in first_team
        assert "W" in first_team
        assert "L" in first_team
        assert "ERA" in first_team
        assert "IP" in first_team
        assert "SO" in first_team
        assert "WHIP" in first_team

        # Should NOT include batting-only fields
        assert "AB" not in first_team
        assert "RBI" not in first_team
