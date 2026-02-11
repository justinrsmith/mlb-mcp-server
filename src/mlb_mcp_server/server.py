from typing import Callable, List, Type, TypeVar

import pandas as pd
from mcp.server.fastmcp import FastMCP
from pybaseball import batting_stats, pitching_stats
from pydantic import BaseModel

from mlb_mcp_server.constants import BATTING_PRESETS, PITCHING_PRESETS
from mlb_mcp_server.models import BattingStats, PitchingStats

mcp = FastMCP("Statcast")

T = TypeVar("T", bound=BaseModel)


def _fetch_stats_by_year(
    year: int,
    stats_func: Callable[[int], pd.DataFrame],
    model_cls: Type[T],
    page: int = 1,
    page_size: int = 10,
    fields: str = "all",
) -> dict:
    """
    Generic function to fetch stats by year and convert to Pydantic models.
    Args:
        year: Season year to retrieve data for.
        stats_func: Function to fetch stats (e.g., batting_stats, pitching_stats).
        model_cls: Pydantic model class to convert data into.
        page: Page number for pagination.
        page_size: Number of records per page.
        fields: Which fields to return. Options:
            - "all": All available fields (may be large)
            - "basic": Core stats only (Name, Team, G, AB, H, HR, RBI, AVG, etc.)
            - "advanced": Advanced metrics (wOBA, wRC+, WAR, etc.)
            - "statcast": Statcast data (EV, LA, Barrels, xwOBA, etc.)
            - Comma-separated field names for custom selection
    Returns:
        Dictionary containing stats for the specified year.
    """
    # Get data from pybaseball
    try:
        df = stats_func(year)
    except Exception as e:
        return {"error": str(e)}

    if df.empty:
        return {
            "year": year,
            "total_rows": 0,
            "page": page,
            "page_size": page_size,
            "data": [],
        }

    total_rows = len(df)

    # Pagination math
    start = (page - 1) * page_size
    end = start + page_size

    if start >= total_rows:
        return {
            "year": year,
            "total_rows": total_rows,
            "page": page,
            "page_size": page_size,
            "data": [],
        }

    # Slice BEFORE converting to Pydantic
    page_df = df.iloc[start:end]

    records = page_df.to_dict("records")

    # Only validate page subset
    models: List[T] = [model_cls.model_validate(row) for row in records]

    # Convert to dicts
    data = [m.model_dump(mode="json", exclude_none=True) for m in models]

    # Apply field filtering if requested
    if fields != "all":
        data = _filter_fields(data, fields, model_cls.__name__)

    return {
        "year": year,
        "total_rows": total_rows,
        "page": page,
        "page_size": page_size,
        "total_pages": (total_rows + page_size - 1) // page_size,
        "data": data,
    }


def _filter_fields(data: List[dict], fields: str, model_name: str) -> List[dict]:
    """
    Filter data to only include specified fields.

    Args:
        data: List of dictionaries to filter
        fields: Field specification (preset or comma-separated list)
        model_name: Name of the model ("BattingStats" or "PitchingStats")

    Returns:
        Filtered list of dictionaries
    """
    presets = BATTING_PRESETS if model_name == "BattingStats" else PITCHING_PRESETS

    # Determine which fields to keep
    if fields in presets:
        keep_fields = set(presets[fields])
    else:
        # Treat as comma-separated list of field names
        keep_fields = set(f.strip() for f in fields.split(","))

    # Always include IDfg and Season for identification
    keep_fields.update(["IDfg", "Season"])

    # Filter each record
    filtered_data = []
    for record in data:
        filtered_record = {k: v for k, v in record.items() if k in keep_fields}
        filtered_data.append(filtered_record)

    return filtered_data


@mcp.tool()
def batting_stats_by_year(
    year: int, page: int = 1, page_size: int = 10, fields: str = "basic"
) -> dict:
    """
    Retrieve MLB batting statistics for a specific regular season year.

    This tool returns paginated player-level batting statistics sourced from
    pybaseball. Results may include hundreds to thousands of players, so
    pagination and field filtering should be used to limit response size.

    Parameters:
        year (int):
            Four-digit MLB season year (e.g., 2023).

        page (int, default=1):
            Page number for pagination. Must be >= 1.

        page_size (int, default=10):
            Number of player records per page. Recommended: 5-10 for "all" fields,
            10-25 for preset groups, up to 50 for custom minimal field sets.

        fields (str, default="basic"):
            Which fields to return. Options:
            - "basic": Core stats (Name, Team, G, AB, H, HR, RBI, AVG, OPS, etc.)
            - "advanced": Advanced metrics (wOBA, wRC+, WAR, ISO, BABIP, etc.)
            - "statcast": Statcast data (EV, LA, Barrels, xwOBA, etc.)
            - "all": All available fields (WARNING: large payload, use small page_size)
            - Custom: Comma-separated field names (e.g., "Name,Team,HR,AVG,WAR")

    Returns:
        dict with the following structure:

        {
            "year": int,
            "total_rows": int,        # total number of players in dataset
            "page": int,
            "page_size": int,
            "total_pages": int,
            "data": List[dict]         # list of player batting stat records
        }

    Notes:
        - If the requested page exceeds total_pages, an empty "data" list is returned.
        - Only regular season data is included.
        - Use field filtering to avoid large payloads that may cause errors in Claude Desktop.
        - IDfg and Season are always included for player identification.
    """
    return _fetch_stats_by_year(
        year, batting_stats, BattingStats, page, page_size, fields
    )


@mcp.tool()
def pitching_stats_by_year(
    year: int, page: int = 1, page_size: int = 10, fields: str = "basic"
) -> dict:
    """
    Retrieve MLB pitching statistics for a specific regular season year.

    This tool returns paginated player-level pitching statistics sourced from
    pybaseball. Results may include hundreds to thousands of players, so
    pagination and field filtering should be used to limit response size.

    Parameters:
        year (int):
            Four-digit MLB season year (e.g., 2023).

        page (int, default=1):
            Page number for pagination. Must be >= 1.

        page_size (int, default=10):
            Number of player records per page. Recommended: 5-10 for "all" fields,
            10-25 for preset groups, up to 50 for custom minimal field sets.

        fields (str, default="basic"):
            Which fields to return. Options:
            - "basic": Core stats (Name, Team, W, L, ERA, IP, SO, WHIP, etc.)
            - "advanced": Advanced metrics (FIP, xFIP, SIERA, K%, WAR, etc.)
            - "statcast": Statcast data (EV, LA, Barrel%, xwOBA, xERA, etc.)
            - "all": All available fields (WARNING: large payload, use small page_size)
            - Custom: Comma-separated field names (e.g., "Name,Team,ERA,WHIP,WAR")

    Returns:
        dict with the following structure:

        {
            "year": int,
            "total_rows": int,        # total number of players in dataset
            "page": int,
            "page_size": int,
            "total_pages": int,
            "data": List[dict]         # list of player pitching stat records
        }

    Notes:
        - If the requested page exceeds total_pages, an empty "data" list is returned.
        - Only regular season data is included.
        - Use field filtering to avoid large payloads that may cause errors in Claude Desktop.
        - IDfg and Season are always included for player identification.
    """
    return _fetch_stats_by_year(
        year, pitching_stats, PitchingStats, page, page_size, fields
    )


# Run the server
if __name__ == "__main__":  # pragma: no cover
    mcp.run()
