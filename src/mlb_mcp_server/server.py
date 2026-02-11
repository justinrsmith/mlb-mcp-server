from typing import Callable, List, Type, TypeVar

import pandas as pd
from mcp.server.fastmcp import FastMCP
from pybaseball import batting_stats, pitching_stats
from pydantic import BaseModel

from mlb_mcp_server.models import BattingStats, PitchingStats

mcp = FastMCP("Statcast")

T = TypeVar("T", bound=BaseModel)


def _fetch_stats_by_year(
    year: int,
    stats_func: Callable[[int], pd.DataFrame],
    model_cls: Type[T],
    page: int = 1,
    page_size: int = 100,
) -> dict:
    """
    Generic function to fetch stats by year and convert to Pydantic models.
    Args:
        year: Season year to retrieve data for.
        stats_func: Function to fetch stats (e.g., batting_stats, pitching_stats).
        model_cls: Pydantic model class to convert data into.
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

    return {
        "year": year,
        "total_rows": total_rows,
        "page": page,
        "page_size": page_size,
        "total_pages": (total_rows + page_size - 1) // page_size,
        "data": [m.model_dump(mode="json", exclude_none=True) for m in models],
    }


@mcp.tool()
def batting_stats_by_year(year: int, page: int = 1, page_size: int = 25) -> dict:
    """
    Retrieve MLB batting statistics for a specific regular season year.

    This tool returns paginated player-level batting statistics sourced from
    pybaseball. Results may include hundreds to thousands of players, so
    pagination parameters should be used to limit response size.

    Parameters:
        year (int):
            Four-digit MLB season year (e.g., 2023).

        page (int, default=1):
            Page number for pagination. Must be >= 1.

        page_size (int, default=100):
            Number of player records per page. Larger values increase response size
            and may impact performance.

    Returns:
        dict with the following structure:

        {
            "year": int,
            "total_rows": int,        # total number of players in dataset
            "page": int,
            "page_size": int,
            "total_pages": int,
            "data": List[BattingStats]  # list of player batting stat records
        }

    Notes:
        - If the requested page exceeds total_pages, an empty "data" list is returned.
        - Only regular season data is included.
        - Use pagination to avoid large payload responses.
    """
    return _fetch_stats_by_year(year, batting_stats, BattingStats, page, page_size)


@mcp.tool()
def pitching_stats_by_year(year: int, page: int = 1, page_size: int = 25) -> dict:
    """
    Retrieve MLB pitching statistics for a specific regular season year.

    This tool returns paginated player-level pitching statistics sourced from
    pybaseball. Results may include hundreds to thousands of players, so
    pagination parameters should be used to limit response size.

    Parameters:
        year (int):
            Four-digit MLB season year (e.g., 2023).

        page (int, default=1):
            Page number for pagination. Must be >= 1.

        page_size (int, default=100):
            Number of player records per page. Larger values increase response size
            and may impact performance.

    Returns:
        dict with the following structure:

        {
            "year": int,
            "total_rows": int,        # total number of players in dataset
            "page": int,
            "page_size": int,
            "total_pages": int,
            "data": List[PitchingStats]  # list of player pitching stat records
        }

    Notes:
        - If the requested page exceeds total_pages, an empty "data" list is returned.
        - Only regular season data is included.
        - Use pagination to avoid large payload responses.
    """
    return _fetch_stats_by_year(year, pitching_stats, PitchingStats, page, page_size)


# Run the server
if __name__ == "__main__":  # pragma: no cover
    mcp.run()
