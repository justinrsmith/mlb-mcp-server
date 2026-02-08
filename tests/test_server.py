from unittest.mock import mock_open, patch

from mlb_mcp_server.models import BRef, Statcast
from mlb_mcp_server.server import get_bref_data, get_statcast_data

# Sample CSV contents
STATCAST_CSV = """last_name_first_name,player_id,year,pa,k_percent,bb_percent,woba,xwoba,sweet_spot_percent,barrel_batted_rate,hard_hit_percent,avg_best_speed,avg_hyper_speed,whiff_percent,swing_percent
Doe,123,2025,400,25.0,10.0,.350,.360,30.0,5.0,40.0,90.0,100.0,20.0,60.0
"""
BREF_CSV = """Rk,Player,Age,Team,Lg,WAR,G,PA,AB,R,H,2B,3B,HR,RBI,SB,CS,BB,SO,BA,OBP,SLG,OPS,OPS+,rOBA,Rbat+,TB,GIDP,HBP,SH,SF,IBB,Pos,Awards,Player-additional
1,John Doe,28,NYY,AL,5.0,150,600,500,120,150,30,2,25,90,5,2,70,100,.300,.380,.500,.880,120,40,110,250,5,3,2,1,1,RF,All-Star,JD123
"""


@patch("builtins.open", new_callable=mock_open, read_data=STATCAST_CSV)
@patch("os.path.exists", return_value=True)
def test_get_statcast_data_success(mock_exists, mock_file):
    """Get statcast data tool should return a list of Statcast models when the CSV is valid."""
    result = get_statcast_data()
    assert "data" in result
    assert len(result["data"]) == 1
    row = result["data"][0]
    assert isinstance(row, Statcast)
    assert row.last_name_first_name == "Doe"
    assert row.player_id == 123


@patch("os.path.exists", return_value=False)
def test_get_statcast_data_file_missing(mock_exists):
    """Get statcast data tool should return an error when the CSV file is missing."""
    result = get_statcast_data()
    assert "error" in result
    assert "not found" in result["error"]


@patch("builtins.open", new_callable=mock_open, read_data=BREF_CSV)
def test_get_bref_data_success(mock_file):
    """Get bref data tool should return a list of BRef models when the CSV is valid."""
    result = get_bref_data()
    assert "data" in result
    assert len(result["data"]) == 1
    row = result["data"][0]
    assert isinstance(row, BRef)
    assert row.player == "John Doe"
    assert row.team == "NYY"
    assert row.player_id == "JD123"


@patch("os.path.exists", return_value=False)
def test_get_bref_data_file_not_found(mock_exists):
    """Get bref data tool should return an error when the CSV file is missing."""
    result = get_bref_data()
    assert "error" in result
    assert "not found" in result["error"]
