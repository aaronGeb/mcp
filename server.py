#!/usr/bin/env python3
"""Mcp server"""

import logging
import os
import sys
from datetime import datetime

import requests
from dotenv import load_dotenv
from fastmcp import FastMCP

# Load environment variables from .env file
load_dotenv()
# Set up logging
name = "my-mcp-server"  # This should match the name in pyproject.toml
logging.basicConfig(
    level=logging.INFO,
    format="%(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Create the MCP server
env_port = os.getenv("MCP_PORT")
# Convert the environment value to int
port = (
    int(env_port) if env_port is not None else 3000
)  # Default to 3000 if MCP_PORT is not set
server = FastMCP(name=name, port=port)


@server.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    logger.info("Adding %s and %s", a, b)
    return a + b


@server.tool()
def get_current_time() -> str:
    """Get the current time as a string."""
    current_time = datetime.now().isoformat()
    logger.info("Current time is %s", current_time)
    return current_time


@server.tool()
def get_current_weather(city: str) -> str:
    """Get the current weather in the specified city."""
    logger.info("Tool call: get_current_weather(%s)", city)
    try:
        endpoint = "http://wttr.in"
        response = requests.get(f"{endpoint}/{city}", timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logger.error("Error fetching weather data: %s", e, exc_info=True)
        return f"Could not fetch weather data for {city}."


if __name__ == "__main__":
    logger.info("Starting MCP server on port %s", port)
    try:
        server.run(transport="sse")
    except (RuntimeError, OSError) as e:
        logger.error("Error running MCP server: %s", e, exc_info=True)
        sys.exit(1)
    finally:
        logger.info("MCP server has stopped.")
