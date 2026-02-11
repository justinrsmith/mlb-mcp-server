from typing import Optional, Union

from pydantic import BaseModel, ConfigDict, Field


class BattingStats(BaseModel):
    """
    Comprehensive batting statistics model optimized for Claude Desktop.
    Removes pitch-tracking columns while keeping Statcast and FanGraphs data.
    """

    # ========== IDENTITY ==========
    IDfg: int = Field(..., description="FanGraphs Player ID")
    Season: int
    Name: str
    Team: str
    Age: Optional[int] = None
    Pos: Optional[Union[str, float]] = Field(None, description="Position")
    Age_Rng: Optional[str] = Field(None, alias="Age Rng", description="Age Range")

    # ========== BASIC COUNTING STATS ==========
    G: int = Field(..., description="Games")
    AB: int = Field(..., description="At Bats")
    PA: int = Field(..., description="Plate Appearances")
    H: int = Field(..., description="Hits")
    single: Optional[int] = Field(None, alias="1B", description="Singles")
    double: Optional[int] = Field(None, alias="2B", description="Doubles")
    triple: Optional[int] = Field(None, alias="3B", description="Triples")
    HR: int = Field(..., description="Home Runs")
    R: int = Field(..., description="Runs")
    RBI: int = Field(..., description="Runs Batted In")
    BB: int = Field(..., description="Walks")
    IBB: Optional[int] = Field(None, description="Intentional Walks")
    SO: int = Field(..., description="Strikeouts")
    HBP: Optional[int] = Field(None, description="Hit By Pitch")
    SF: Optional[int] = Field(None, description="Sacrifice Flies")
    SH: Optional[int] = Field(None, description="Sacrifice Hits/Bunts")
    GDP: Optional[int] = Field(None, description="Grounded into Double Play")
    SB: Optional[int] = Field(None, description="Stolen Bases")
    CS: Optional[int] = Field(None, description="Caught Stealing")

    # ========== TRADITIONAL RATE STATS ==========
    AVG: float = Field(..., description="Batting Average")
    OBP: float = Field(..., description="On Base Percentage")
    SLG: float = Field(..., description="Slugging Percentage")
    OPS: float = Field(..., description="On Base Plus Slugging")
    ISO: Optional[float] = Field(None, description="Isolated Power")
    BABIP: Optional[float] = Field(None, description="Batting Average on Balls in Play")

    # ========== PLATE DISCIPLINE ==========
    BB_pct: Optional[float] = Field(None, alias="BB%", description="Walk Percentage")
    K_pct: Optional[float] = Field(None, alias="K%", description="Strikeout Percentage")
    BB_K: Optional[float] = Field(
        None, alias="BB/K", description="Walk to Strikeout Ratio"
    )

    # Swing metrics (not pitch-tracking, these are general plate discipline)
    O_Swing_pct: Optional[float] = Field(
        None, alias="O-Swing%", description="Outside Swing %"
    )
    Z_Swing_pct: Optional[float] = Field(
        None, alias="Z-Swing%", description="Zone Swing %"
    )
    Swing_pct: Optional[float] = Field(
        None, alias="Swing%", description="Overall Swing %"
    )
    O_Contact_pct: Optional[float] = Field(
        None, alias="O-Contact%", description="Outside Contact %"
    )
    Z_Contact_pct: Optional[float] = Field(
        None, alias="Z-Contact%", description="Zone Contact %"
    )
    Contact_pct: Optional[float] = Field(
        None, alias="Contact%", description="Overall Contact %"
    )
    Zone_pct: Optional[float] = Field(None, alias="Zone%", description="Zone %")
    F_Strike_pct: Optional[float] = Field(
        None, alias="F-Strike%", description="First Strike %"
    )
    SwStr_pct: Optional[float] = Field(
        None, alias="SwStr%", description="Swinging Strike %"
    )
    CStr_pct: Optional[float] = Field(
        None, alias="CStr%", description="Called Strike %"
    )
    CSW_pct: Optional[float] = Field(
        None, alias="CSW%", description="Called + Swinging Strike %"
    )

    # ========== BATTED BALL DATA ==========
    GB: Optional[int] = Field(None, description="Ground Balls")
    FB: Optional[int] = Field(None, description="Fly Balls")
    LD: Optional[int] = Field(None, description="Line Drives")
    IFFB: Optional[int] = Field(None, description="Infield Fly Balls")

    GB_FB: Optional[float] = Field(
        None, alias="GB/FB", description="Ground Ball to Fly Ball Ratio"
    )
    LD_pct: Optional[float] = Field(None, alias="LD%", description="Line Drive %")
    GB_pct: Optional[float] = Field(None, alias="GB%", description="Ground Ball %")
    FB_pct: Optional[float] = Field(None, alias="FB%", description="Fly Ball %")
    IFFB_pct: Optional[float] = Field(
        None, alias="IFFB%", description="Infield Fly Ball %"
    )
    HR_FB: Optional[float] = Field(
        None, alias="HR/FB", description="Home Run per Fly Ball"
    )

    Pull_pct: Optional[float] = Field(None, alias="Pull%", description="Pull %")
    Cent_pct: Optional[float] = Field(None, alias="Cent%", description="Center %")
    Oppo_pct: Optional[float] = Field(
        None, alias="Oppo%", description="Opposite Field %"
    )

    Soft_pct: Optional[float] = Field(None, alias="Soft%", description="Soft Contact %")
    Med_pct: Optional[float] = Field(None, alias="Med%", description="Medium Contact %")
    Hard_pct: Optional[float] = Field(None, alias="Hard%", description="Hard Contact %")

    # ========== ADVANCED FANGRAPHS METRICS ==========
    wOBA: Optional[float] = Field(None, description="Weighted On Base Average")
    wRAA: Optional[float] = Field(None, description="Weighted Runs Above Average")
    wRC: Optional[float] = Field(None, description="Weighted Runs Created")
    wRC_plus: Optional[int] = Field(
        None, alias="wRC+", description="Weighted Runs Created Plus"
    )

    # ========== VALUE METRICS ==========
    Bat: Optional[float] = Field(None, description="Batting Runs")
    Fld: Optional[float] = Field(None, description="Fielding Runs")
    Rep: Optional[float] = Field(None, description="Replacement Runs")
    PositionalAdjustment: Optional[float] = Field(
        None, description="Positional Adjustment"
    )
    RAR: Optional[float] = Field(None, description="Runs Above Replacement")
    WAR: Optional[float] = Field(None, description="Wins Above Replacement")
    Off: Optional[float] = Field(None, description="Offensive Runs")
    Def: Optional[float] = Field(None, description="Defensive Runs")

    # ========== BASERUNNING ==========
    BsR: Optional[float] = Field(None, description="Base Running Runs")
    wSB: Optional[float] = Field(None, description="Weighted Stolen Base Runs")
    UBR: Optional[float] = Field(None, description="Ultimate Base Running")
    wGDP: Optional[float] = Field(None, description="Weighted GDP Runs")
    Spd: Optional[float] = Field(None, description="Speed Score")

    # ========== WIN PROBABILITY ==========
    WPA: Optional[float] = Field(None, description="Win Probability Added")
    minus_WPA: Optional[float] = Field(
        None, alias="-WPA", description="Loss Advancement"
    )
    plus_WPA: Optional[float] = Field(None, alias="+WPA", description="Win Advancement")
    RE24: Optional[float] = Field(None, description="Run Expectancy 24 Base-Out States")
    REW: Optional[float] = Field(None, description="Run Expectancy Wins")
    pLI: Optional[float] = Field(None, description="Average Leverage Index")
    phLI: Optional[float] = Field(
        None, description="Average Leverage Index as Pinch Hitter"
    )
    PH: Optional[int] = Field(None, description="Pinch Hit Appearances")
    WPA_LI: Optional[float] = Field(None, alias="WPA/LI", description="WPA per LI")
    Clutch: Optional[float] = Field(None, description="Clutch Score")

    # ========== STATCAST DATA ==========
    EV: Optional[float] = Field(None, description="Exit Velocity (mph)")
    LA: Optional[float] = Field(None, description="Launch Angle (degrees)")
    Barrels: Optional[int] = Field(None, description="Barrel Count")
    Barrel_pct: Optional[float] = Field(None, alias="Barrel%", description="Barrel %")
    maxEV: Optional[float] = Field(None, description="Max Exit Velocity")
    HardHit: Optional[int] = Field(None, description="Hard Hit Count")
    HardHit_pct: Optional[float] = Field(
        None, alias="HardHit%", description="Hard Hit %"
    )
    Events: Optional[int] = Field(None, description="Batted Ball Events")

    # Statcast Expected Stats
    xBA: Optional[float] = Field(None, description="Expected Batting Average")
    xSLG: Optional[float] = Field(None, description="Expected Slugging")
    xwOBA: Optional[float] = Field(None, description="Expected wOBA")

    # ========== MISCELLANEOUS ==========
    Pitches: Optional[int] = Field(None, description="Pitches Seen")
    Balls: Optional[int] = Field(None, description="Balls Seen")
    Strikes: Optional[int] = Field(None, description="Strikes Seen")
    IFH: Optional[int] = Field(None, description="Infield Hits")
    IFH_pct: Optional[float] = Field(None, alias="IFH%", description="Infield Hit %")
    BU: Optional[int] = Field(None, description="Bunts")
    BUH: Optional[int] = Field(None, description="Bunt Hits")
    BUH_pct: Optional[float] = Field(None, alias="BUH%", description="Bunt Hit %")
    TTO_pct: Optional[float] = Field(
        None, alias="TTO%", description="Three True Outcomes %"
    )
    Pace: Optional[float] = Field(None, description="Pace of Play")
    FRM: Optional[float] = Field(None, description="Framing Runs (catchers)")

    # ========== LEAGUE-ADJUSTED STATS (Plus Stats) ==========
    AVG_plus: Optional[int] = Field(None, alias="AVG+", description="AVG+")
    BB_pct_plus: Optional[int] = Field(None, alias="BB%+", description="BB%+")
    K_pct_plus: Optional[int] = Field(None, alias="K%+", description="K%+")
    OBP_plus: Optional[int] = Field(None, alias="OBP+", description="OBP+")
    SLG_plus: Optional[int] = Field(None, alias="SLG+", description="SLG+")
    ISO_plus: Optional[int] = Field(None, alias="ISO+", description="ISO+")
    BABIP_plus: Optional[int] = Field(None, alias="BABIP+", description="BABIP+")
    LD_pct_plus: Optional[float] = Field(None, alias="LD+%", description="LD%+")
    GB_pct_plus: Optional[int] = Field(None, alias="GB%+", description="GB%+")
    FB_pct_plus: Optional[int] = Field(None, alias="FB%+", description="FB%+")
    HR_FB_pct_plus: Optional[int] = Field(None, alias="HR/FB%+", description="HR/FB%+")
    Pull_pct_plus: Optional[int] = Field(None, alias="Pull%+", description="Pull%+")
    Cent_pct_plus: Optional[int] = Field(None, alias="Cent%+", description="Cent%+")
    Oppo_pct_plus: Optional[int] = Field(None, alias="Oppo%+", description="Oppo%+")
    Soft_pct_plus: Optional[int] = Field(None, alias="Soft%+", description="Soft%+")
    Med_pct_plus: Optional[int] = Field(None, alias="Med%+", description="Med%+")
    Hard_pct_plus: Optional[int] = Field(None, alias="Hard%+", description="Hard%+")

    # Alternative WAR calculation
    L_WAR: Optional[float] = Field(None, alias="L-WAR", description="Alternative WAR")

    model_config = ConfigDict(
        populate_by_name=True
    )  # Allows using both alias and field name


class PitchingStats(BaseModel):
    """
    Comprehensive pitching statistics model optimized for MCP tools.
    Removes pitch-tracking columns while keeping Statcast and FanGraphs data.
    """

    # ========== IDENTITY ==========
    IDfg: int = Field(..., description="FanGraphs Player ID")
    Season: int
    Name: str
    Team: str
    Age: Optional[int] = None
    Pos: Optional[str] = Field(None, description="Position (SP/RP)")
    Age_Rng: Optional[str] = Field(None, alias="Age Rng", description="Age Range")
    Lg: Optional[str] = Field(None, description="League")

    # ========== BASIC COUNTING STATS ==========
    W: int = Field(..., description="Wins")
    L: int = Field(..., description="Losses")
    ERA: float = Field(..., description="Earned Run Average")
    G: int = Field(..., description="Games")
    GS: int = Field(..., description="Games Started")
    CG: Optional[int] = Field(None, description="Complete Games")
    ShO: Optional[int] = Field(None, description="Shutouts")
    SV: Optional[int] = Field(None, description="Saves")
    BS: Optional[int] = Field(None, description="Blown Saves")
    HLD: Optional[int] = Field(None, description="Holds")
    IP: float = Field(..., description="Innings Pitched")
    TBF: int = Field(..., description="Total Batters Faced")
    H: int = Field(..., description="Hits Allowed")
    R: int = Field(..., description="Runs Allowed")
    ER: int = Field(..., description="Earned Runs")
    HR: int = Field(..., description="Home Runs Allowed")
    BB: int = Field(..., description="Walks")
    IBB: Optional[int] = Field(None, description="Intentional Walks")
    HBP: Optional[int] = Field(None, description="Hit By Pitch")
    WP: Optional[int] = Field(None, description="Wild Pitches")
    BK: Optional[int] = Field(None, description="Balks")
    SO: int = Field(..., description="Strikeouts")

    # ========== TRADITIONAL RATE STATS ==========
    K_9: Optional[float] = Field(
        None, alias="K/9", description="Strikeouts per 9 innings"
    )
    BB_9: Optional[float] = Field(None, alias="BB/9", description="Walks per 9 innings")
    K_BB: Optional[float] = Field(
        None, alias="K/BB", description="Strikeout to Walk Ratio"
    )
    H_9: Optional[float] = Field(None, alias="H/9", description="Hits per 9 innings")
    HR_9: Optional[float] = Field(
        None, alias="HR/9", description="Home Runs per 9 innings"
    )
    AVG: Optional[float] = Field(None, description="Batting Average Against")
    WHIP: Optional[float] = Field(None, description="Walks + Hits per Inning Pitched")
    BABIP: Optional[float] = Field(None, description="Batting Average on Balls in Play")
    LOB_pct: Optional[float] = Field(
        None, alias="LOB%", description="Left on Base Percentage"
    )

    # ========== ADVANCED METRICS ==========
    FIP: Optional[float] = Field(None, description="Fielding Independent Pitching")
    xFIP: Optional[float] = Field(None, description="Expected FIP")
    SIERA: Optional[float] = Field(None, description="Skill-Interactive ERA")
    tERA: Optional[float] = Field(None, description="True ERA")
    xERA: Optional[float] = Field(None, description="Expected ERA")

    # ========== PLATE DISCIPLINE ==========
    K_pct: Optional[float] = Field(None, alias="K%", description="Strikeout Percentage")
    BB_pct: Optional[float] = Field(None, alias="BB%", description="Walk Percentage")
    K_BB_pct: Optional[float] = Field(None, alias="K-BB%", description="K% - BB%")

    # Swing metrics
    O_Swing_pct: Optional[float] = Field(
        None, alias="O-Swing%", description="Outside Swing %"
    )
    Z_Swing_pct: Optional[float] = Field(
        None, alias="Z-Swing%", description="Zone Swing %"
    )
    Swing_pct: Optional[float] = Field(
        None, alias="Swing%", description="Overall Swing %"
    )
    O_Contact_pct: Optional[float] = Field(
        None, alias="O-Contact%", description="Outside Contact %"
    )
    Z_Contact_pct: Optional[float] = Field(
        None, alias="Z-Contact%", description="Zone Contact %"
    )
    Contact_pct: Optional[float] = Field(
        None, alias="Contact%", description="Overall Contact %"
    )
    Zone_pct: Optional[float] = Field(None, alias="Zone%", description="Zone %")
    F_Strike_pct: Optional[float] = Field(
        None, alias="F-Strike%", description="First Strike %"
    )
    SwStr_pct: Optional[float] = Field(
        None, alias="SwStr%", description="Swinging Strike %"
    )
    CStr_pct: Optional[float] = Field(
        None, alias="CStr%", description="Called Strike %"
    )
    CSW_pct: Optional[float] = Field(
        None, alias="CSW%", description="Called + Swinging Strike %"
    )

    # ========== BATTED BALL DATA ==========
    GB: Optional[int] = Field(None, description="Ground Balls")
    FB: Optional[int] = Field(None, description="Fly Balls")
    LD: Optional[int] = Field(None, description="Line Drives")
    IFFB: Optional[int] = Field(None, description="Infield Fly Balls")

    GB_pct: Optional[float] = Field(None, alias="GB%", description="Ground Ball %")
    FB_pct: Optional[float] = Field(None, alias="FB%", description="Fly Ball %")
    LD_pct: Optional[float] = Field(None, alias="LD%", description="Line Drive %")
    IFFB_pct: Optional[float] = Field(
        None, alias="IFFB%", description="Infield Fly Ball %"
    )
    HR_FB: Optional[float] = Field(
        None, alias="HR/FB", description="Home Run per Fly Ball"
    )

    Pull_pct: Optional[float] = Field(None, alias="Pull%", description="Pull %")
    Cent_pct: Optional[float] = Field(None, alias="Cent%", description="Center %")
    Oppo_pct: Optional[float] = Field(
        None, alias="Oppo%", description="Opposite Field %"
    )

    Soft_pct: Optional[float] = Field(None, alias="Soft%", description="Soft Contact %")
    Med_pct: Optional[float] = Field(None, alias="Med%", description="Medium Contact %")
    Hard_pct: Optional[float] = Field(None, alias="Hard%", description="Hard Contact %")

    # ========== VALUE METRICS ==========
    WAR: Optional[float] = Field(None, description="Wins Above Replacement")
    RA9_WAR: Optional[float] = Field(
        None, alias="RA9-WAR", description="RA9 Wins Above Replacement"
    )
    RAR: Optional[float] = Field(None, description="Runs Above Replacement")
    # Dollars: Optional[float] = Field(None, description="Dollar Value")

    # ========== WIN PROBABILITY ==========
    WPA: Optional[float] = Field(None, description="Win Probability Added")
    minus_WPA: Optional[float] = Field(
        None, alias="-WPA", description="Loss Advancement"
    )
    plus_WPA: Optional[float] = Field(None, alias="+WPA", description="Win Advancement")
    RE24: Optional[float] = Field(None, description="Run Expectancy 24 Base-Out States")
    REW: Optional[float] = Field(None, description="Run Expectancy Wins")
    pLI: Optional[float] = Field(None, description="Average Leverage Index")
    inLI: Optional[float] = Field(None, description="Leverage Index at Start of Inning")
    gmLI: Optional[float] = Field(None, description="Leverage Index at Start of Game")
    exLI: Optional[float] = Field(None, description="Leverage Index at Exit")
    Pulls: Optional[int] = Field(None, description="Times Pulled from Game")
    WPA_LI: Optional[float] = Field(None, alias="WPA/LI", description="WPA per LI")
    Clutch: Optional[float] = Field(None, description="Clutch Score")

    # ========== STATCAST DATA ==========
    EV: Optional[float] = Field(None, description="Exit Velocity (mph)")
    LA: Optional[float] = Field(None, description="Launch Angle (degrees)")
    Barrel_pct: Optional[float] = Field(None, alias="Barrel%", description="Barrel %")
    HardHit_pct: Optional[float] = Field(
        None, alias="HardHit%", description="Hard Hit %"
    )
    maxEV: Optional[float] = Field(None, description="Max Exit Velocity")
    Events: Optional[int] = Field(None, description="Batted Ball Events")

    # Statcast Expected Stats
    xBA: Optional[float] = Field(None, description="Expected Batting Average Against")
    xSLG: Optional[float] = Field(None, description="Expected Slugging Against")
    xwOBA: Optional[float] = Field(None, description="Expected wOBA Against")

    # ========== MISCELLANEOUS ==========
    Pitches: Optional[int] = Field(None, description="Total Pitches Thrown")
    Balls: Optional[int] = Field(None, description="Balls Thrown")
    Strikes: Optional[int] = Field(None, description="Strikes Thrown")
    IFH: Optional[int] = Field(None, description="Infield Hits Allowed")
    IFH_pct: Optional[float] = Field(None, alias="IFH%", description="Infield Hit %")
    BU: Optional[int] = Field(None, description="Bunts Against")
    BUH: Optional[int] = Field(None, description="Bunt Hits Allowed")
    BUH_pct: Optional[float] = Field(None, alias="BUH%", description="Bunt Hit %")
    Pace: Optional[float] = Field(None, description="Pace of Play")

    # # ========== STARTER/RELIEVER SPLITS ==========
    Start_IP: Optional[float] = Field(
        None, alias="Start-IP", description="Innings as Starter"
    )
    Relief_IP: Optional[float] = Field(
        None, alias="Relief-IP", description="Innings in Relief"
    )

    # ========== LEAGUE-ADJUSTED STATS (Plus Stats) ==========
    K_9_plus: Optional[int] = Field(None, alias="K/9+", description="K/9+")
    BB_9_plus: Optional[int] = Field(None, alias="BB/9+", description="BB/9+")
    K_BB_plus: Optional[int] = Field(None, alias="K/BB+", description="K/BB+")
    H_9_plus: Optional[int] = Field(None, alias="H/9+", description="H/9+")
    HR_9_plus: Optional[int] = Field(None, alias="HR/9+", description="HR/9+")
    AVG_plus: Optional[int] = Field(None, alias="AVG+", description="AVG+")
    WHIP_plus: Optional[int] = Field(None, alias="WHIP+", description="WHIP+")
    BABIP_plus: Optional[int] = Field(None, alias="BABIP+", description="BABIP+")
    LOB_pct_plus: Optional[int] = Field(None, alias="LOB%+", description="LOB%+")
    K_pct_plus: Optional[int] = Field(None, alias="K%+", description="K%+")
    BB_pct_plus: Optional[int] = Field(None, alias="BB%+", description="BB%+")
    LD_pct_plus: Optional[int] = Field(None, alias="LD%+", description="LD%+")
    GB_pct_plus: Optional[int] = Field(None, alias="GB%+", description="GB%+")
    FB_pct_plus: Optional[int] = Field(None, alias="FB%+", description="FB%+")
    HR_FB_pct_plus: Optional[int] = Field(None, alias="HR/FB%+", description="HR/FB%+")
    Pull_pct_plus: Optional[int] = Field(None, alias="Pull%+", description="Pull%+")
    Cent_pct_plus: Optional[int] = Field(None, alias="Cent%+", description="Cent%+")
    Oppo_pct_plus: Optional[int] = Field(None, alias="Oppo%+", description="Oppo%+")
    Soft_pct_plus: Optional[int] = Field(None, alias="Soft%+", description="Soft%+")
    Med_pct_plus: Optional[int] = Field(None, alias="Med%+", description="Med%+")
    Hard_pct_plus: Optional[int] = Field(None, alias="Hard%+", description="Hard%+")
    ERA_plus: Optional[int] = Field(None, alias="ERA+", description="ERA+")
    FIP_plus: Optional[int] = Field(None, alias="FIP+", description="FIP+")
    xFIP_plus: Optional[int] = Field(None, alias="xFIP+", description="xFIP+")

    model_config = ConfigDict(
        populate_by_name=True
    )  # Allows using both alias and field name


class TeamPitchingStats(BaseModel):
    """
    Comprehensive team pitching statistics model optimized for MCP tools.
    Structured identically to PitchingStats but for team-level aggregates.
    """

    # ========== IDENTITY ==========
    teamIDfg: int = Field(..., description="FanGraphs Team ID")
    Season: int
    Team: str
    Age: Optional[int] = Field(None, description="Average Team Age")

    # ========== BASIC COUNTING STATS ==========
    W: int = Field(..., description="Wins")
    L: int = Field(..., description="Losses")
    ERA: float = Field(..., description="Earned Run Average")
    G: int = Field(..., description="Games")
    GS: int = Field(..., description="Games Started")
    CG: Optional[int] = Field(None, description="Complete Games")
    ShO: Optional[int] = Field(None, description="Shutouts")
    SV: Optional[int] = Field(None, description="Saves")

    IP: float = Field(..., description="Innings Pitched")
    H: int = Field(..., description="Hits Allowed")
    R: int = Field(..., description="Runs Allowed")
    ER: int = Field(..., description="Earned Runs")
    HR: int = Field(..., description="Home Runs Allowed")
    BB: int = Field(..., description="Walks")
    IBB: Optional[int] = Field(None, description="Intentional Walks")
    SO: int = Field(..., description="Strikeouts")
    HBP: Optional[int] = Field(None, description="Hit By Pitch")
    WP: Optional[int] = Field(None, description="Wild Pitches")
    BK: Optional[int] = Field(None, description="Balks")

    TBF: Optional[int] = Field(None, description="Total Batters Faced")
    Pitches: Optional[int] = Field(None, description="Total Pitches Thrown")
    Balls: Optional[int] = Field(None, description="Balls Thrown")
    Strikes: Optional[int] = Field(None, description="Strikes Thrown")

    # ========== TRADITIONAL RATE STATS ==========
    WHIP: Optional[float] = Field(None, description="Walks + Hits per Inning Pitched")
    BABIP: Optional[float] = Field(None, description="Batting Average on Balls in Play")
    LOB_pct: Optional[float] = Field(
        None, alias="LOB%", description="Left on Base Percentage"
    )

    K_9: Optional[float] = Field(None, alias="K/9", description="Strikeouts per 9")
    BB_9: Optional[float] = Field(None, alias="BB/9", description="Walks per 9")
    HR_9: Optional[float] = Field(None, alias="HR/9", description="Home Runs per 9")
    K_BB: Optional[float] = Field(None, alias="K/BB", description="K/BB Ratio")

    # ========== ADVANCED METRICS ==========
    FIP: Optional[float] = Field(None, description="Fielding Independent Pitching")
    xFIP: Optional[float] = Field(None, description="Expected FIP")
    SIERA: Optional[float] = Field(None, description="Skill-Interactive ERA")
    xERA: Optional[float] = Field(None, description="Expected ERA")

    # ========== BATTED BALL DATA ==========
    GB: Optional[int] = Field(None, description="Ground Balls")
    FB: Optional[int] = Field(None, description="Fly Balls")
    LD: Optional[int] = Field(None, description="Line Drives")
    IFFB: Optional[int] = Field(None, description="Infield Fly Balls")

    GB_pct: Optional[float] = Field(None, alias="GB%", description="Ground Ball %")
    FB_pct: Optional[float] = Field(None, alias="FB%", description="Fly Ball %")
    LD_pct: Optional[float] = Field(None, alias="LD%", description="Line Drive %")
    IFFB_pct: Optional[float] = Field(None, alias="IFFB%", description="IFFB %")
    HR_FB: Optional[float] = Field(None, alias="HR/FB", description="HR per Fly Ball")

    # ========== VALUE METRICS ==========
    WAR: Optional[float] = Field(None, description="Wins Above Replacement")
    RA9_WAR: Optional[float] = Field(
        None, alias="RA9-WAR", description="RA9 Wins Above Replacement"
    )

    # ========== LEAGUE-ADJUSTED STATS (Plus Stats) ==========
    ERA_plus: Optional[int] = Field(None, alias="ERA+", description="ERA+")
    FIP_plus: Optional[int] = Field(None, alias="FIP+", description="FIP+")
    BABIP_plus: Optional[int] = Field(None, alias="BABIP+", description="BABIP+")
    LOB_pct_plus: Optional[int] = Field(None, alias="LOB%+", description="LOB%+")
    K_pct_plus: Optional[int] = Field(None, alias="K%+", description="K%+")
    BB_pct_plus: Optional[int] = Field(None, alias="BB%+", description="BB%+")
    GB_pct_plus: Optional[int] = Field(None, alias="GB%+", description="GB%+")
    FB_pct_plus: Optional[int] = Field(None, alias="FB%+", description="FB%+")
    LD_pct_plus: Optional[int] = Field(None, alias="LD%+", description="LD%+")
    HR_FB_pct_plus: Optional[int] = Field(None, alias="HR/FB%+", description="HR/FB%+")

    # ========== PITCH QUALITY METRICS ==========
    Stuff_plus: Optional[int] = Field(None, alias="Stuff+", description="Stuff+")
    Location_plus: Optional[int] = Field(
        None, alias="Location+", description="Location+"
    )
    Pitching_plus: Optional[int] = Field(
        None, alias="Pitching+", description="Pitching+"
    )

    model_config = ConfigDict(populate_by_name=True)


class TeamBattingStats(BaseModel):
    """
    Comprehensive team batting statistics model optimized for MCP tools.
    Structured identically to BattingStats but for team-level aggregates.
    """

    # ========== IDENTITY ==========
    teamIDfg: int = Field(..., description="FanGraphs Team ID")
    Season: int
    Team: str
    Age: Optional[int] = Field(None, description="Average Team Age")

    # ========== BASIC COUNTING STATS ==========
    G: int = Field(..., description="Games")
    AB: int = Field(..., description="At Bats")
    PA: int = Field(..., description="Plate Appearances")
    H: int = Field(..., description="Hits")
    R: int = Field(..., description="Runs")
    RBI: int = Field(..., description="Runs Batted In")

    BB: int = Field(..., description="Walks")
    IBB: Optional[int] = Field(None, description="Intentional Walks")
    SO: int = Field(..., description="Strikeouts")
    HBP: Optional[int] = Field(None, description="Hit By Pitch")
    SF: Optional[int] = Field(None, description="Sacrifice Flies")
    SH: Optional[int] = Field(None, description="Sacrifice Hits/Bunts")
    GDP: Optional[int] = Field(None, description="Grounded into Double Play")

    SB: Optional[int] = Field(None, description="Stolen Bases")
    CS: Optional[int] = Field(None, description="Caught Stealing")

    # ========== TRADITIONAL RATE STATS ==========
    AVG: float = Field(..., description="Batting Average")
    OBP: float = Field(..., description="On Base Percentage")
    SLG: float = Field(..., description="Slugging Percentage")
    OPS: float = Field(..., description="On Base Plus Slugging")
    ISO: Optional[float] = Field(None, description="Isolated Power")
    BABIP: Optional[float] = Field(None, description="Batting Average on Balls in Play")

    BB_pct: Optional[float] = Field(None, alias="BB%", description="Walk Percentage")
    K_pct: Optional[float] = Field(None, alias="K%", description="Strikeout Percentage")
    BB_K: Optional[float] = Field(
        None, alias="BB/K", description="Walk to Strikeout Ratio"
    )

    # ========== ADVANCED METRICS ==========
    wOBA: Optional[float] = Field(None, description="Weighted On Base Average")
    wRAA: Optional[float] = Field(None, description="Weighted Runs Above Average")
    wRC: Optional[int] = Field(None, description="Weighted Runs Created")
    wRC_plus: Optional[int] = Field(
        None, alias="wRC+", description="Weighted Runs Created Plus"
    )

    # ========== BATTED BALL DATA ==========
    GB: Optional[int] = Field(None, description="Ground Balls")
    FB: Optional[int] = Field(None, description="Fly Balls")
    LD: Optional[int] = Field(None, description="Line Drives")
    IFFB: Optional[int] = Field(None, description="Infield Fly Balls")

    GB_FB: Optional[float] = Field(
        None, alias="GB/FB", description="Ground Ball to Fly Ball Ratio"
    )
    LD_pct: Optional[float] = Field(
        None, alias="LD%", description="Line Drive Percentage"
    )
    GB_pct: Optional[float] = Field(
        None, alias="GB%", description="Ground Ball Percentage"
    )
    FB_pct: Optional[float] = Field(
        None, alias="FB%", description="Fly Ball Percentage"
    )
    HR_FB: Optional[float] = Field(
        None, alias="HR/FB", description="Home Run per Fly Ball"
    )

    # ========== VALUE METRICS ==========
    WAR: Optional[float] = Field(None, description="Wins Above Replacement")
    RAR: Optional[float] = Field(None, description="Runs Above Replacement")

    Bat: Optional[float] = Field(None, description="Batting Runs")
    Fld: Optional[float] = Field(None, description="Fielding Runs")
    Rep: Optional[float] = Field(None, description="Replacement Runs")
    Pos: Optional[float] = Field(None, description="Positional Adjustment")

    # ========== WIN PROBABILITY ==========
    WPA: Optional[float] = Field(None, description="Win Probability Added")
    WPA_LI: Optional[float] = Field(None, alias="WPA/LI", description="WPA per LI")
    RE24: Optional[float] = Field(None, description="Run Expectancy 24 Base-Out States")

    # ========== BASERUNNING ==========
    Spd: Optional[float] = Field(None, description="Speed Score")

    model_config = ConfigDict(populate_by_name=True)
