import csv
import os
from typing import Dict, List, Type, TypeVar

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

from mlb_mcp_server.models import BRef, Statcast

mcp = FastMCP("Statcast")


T = TypeVar("T", bound=BaseModel)


def read_csv_to_model(file_path: str, model: Type[T]) -> Dict:
    """Generic CSV reader that returns validated Pydantic models."""
    if not os.path.exists(file_path):
        return {"error": f"{file_path} not found"}

    with open(file_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        data: List[T] = [model.model_validate(row) for row in reader]
    return {"data": data}


@mcp.tool()
def get_statcast_data() -> dict:
    return read_csv_to_model("data/stats.csv", Statcast)


@mcp.tool()
def get_bref_data() -> dict:
    return read_csv_to_model("data/bref.csv", BRef)


# Run the server
if __name__ == "__main__":  # pragma: no cover
    mcp.run()
