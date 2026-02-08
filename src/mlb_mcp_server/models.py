from typing import Optional

from pydantic import BaseModel, Field


class Statcast(BaseModel):
    last_name_first_name: str
    player_id: int
    year: int
    pa: int
    k_percent: float
    bb_percent: float
    woba: str
    xwoba: str
    sweet_spot_percent: float
    barrel_batted_rate: float
    hard_hit_percent: float
    avg_best_speed: float
    avg_hyper_speed: float
    whiff_percent: float
    swing_percent: float


class BRef(BaseModel):
    rk: Optional[int] = Field(alias="Rk")
    player: str = Field(alias="Player")
    age: Optional[int] = Field(alias="Age")
    team: str = Field(alias="Team")
    league: str = Field(alias="Lg")
    war: Optional[float] = Field(alias="WAR")
    games: Optional[int] = Field(alias="G")
    plate_appearances: Optional[int] = Field(alias="PA")
    at_bats: Optional[int] = Field(alias="AB")
    runs: Optional[int] = Field(alias="R")
    hits: Optional[int] = Field(alias="H")
    doubles: Optional[int] = Field(alias="2B")
    triples: Optional[int] = Field(alias="3B")
    home_runs: Optional[int] = Field(alias="HR")
    rbi: Optional[int] = Field(alias="RBI")
    stolen_bases: Optional[int] = Field(alias="SB")
    caught_stealing: Optional[int] = Field(alias="CS")
    walks: Optional[int] = Field(alias="BB")
    strikeouts: Optional[int] = Field(alias="SO")
    batting_avg: Optional[float] = Field(alias="BA")
    on_base_pct: Optional[float] = Field(alias="OBP")
    slugging_pct: Optional[float] = Field(alias="SLG")
    ops: Optional[float] = Field(alias="OPS")
    ops_plus: Optional[float] = Field(alias="OPS+")
    woba_runs: Optional[float] = Field(alias="rOBA")
    rbat_plus: Optional[float] = Field(alias="Rbat+")
    total_bases: Optional[int] = Field(alias="TB")
    gidp: Optional[int] = Field(alias="GIDP")
    hbp: Optional[int] = Field(alias="HBP")
    sacrifice_hits: Optional[int] = Field(alias="SH")
    sacrifice_flies: Optional[int] = Field(alias="SF")
    intentional_walks: Optional[int] = Field(alias="IBB")
    position: Optional[str] = Field(alias="Pos")
    awards: Optional[str] = Field(alias="Awards")
    player_id: str = Field(alias="Player-additional")

    model_config = {"populate_by_name": True}
