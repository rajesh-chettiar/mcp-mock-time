from mcp.server.fastmcp import FastMCP
import argparse
import datetime
import pytz
from typing import Optional


def get_timezone_name(location: str) -> Optional[str]:
    """Maps common location names to timezone names.

    Args:
        location: A string representing a location (city, country, etc.)

    Returns:
        str: The corresponding timezone name, or None if not found
    """
    # Dictionary mapping common locations to timezone names
    location_to_timezone = {
        # North America
        "new york": "America/New_York",
        "los angeles": "America/Los_Angeles",
        "chicago": "America/Chicago",
        "toronto": "America/Toronto",
        "mexico city": "America/Mexico_City",
        "vancouver": "America/Vancouver",
        
        # Europe
        "london": "Europe/London",
        "paris": "Europe/Paris",
        "berlin": "Europe/Berlin",
        "rome": "Europe/Rome",
        "madrid": "Europe/Madrid",
        "amsterdam": "Europe/Amsterdam",
        
        # Asia
        "tokyo": "Asia/Tokyo",
        "beijing": "Asia/Shanghai",
        "hong kong": "Asia/Hong_Kong",
        "singapore": "Asia/Singapore",
        "dubai": "Asia/Dubai",
        "mumbai": "Asia/Kolkata",
        
        # Australia & Oceania
        "sydney": "Australia/Sydney",
        "melbourne": "Australia/Melbourne",
        "auckland": "Pacific/Auckland",
        
        # South America
        "sao paulo": "America/Sao_Paulo",
        "buenos aires": "America/Argentina/Buenos_Aires",
        
        # Africa
        "cairo": "Africa/Cairo",
        "johannesburg": "Africa/Johannesburg",
        
        # Common country names
        "usa": "America/New_York",
        "uk": "Europe/London",
        "india": "Asia/Kolkata",
        "japan": "Asia/Tokyo",
        "china": "Asia/Shanghai",
        "australia": "Australia/Sydney",
        "germany": "Europe/Berlin",
        "france": "Europe/Paris",
        "italy": "Europe/Rome",
        "spain": "Europe/Madrid",
    }
    
    return location_to_timezone.get(location.lower())


mcp = FastMCP("TimeService", port=3001)


@mcp.tool()
def get_current_time(location: str):
    """Gets the current time for a specified location.

    Args:
        location: The name of the location (city or country) to get the time for.

    Returns:
        dict: Current time information for the specified location.

    Raises:
        ValueError: If the location is not recognized or has an invalid timezone.
    """
    # Get timezone for the location
    timezone_name = get_timezone_name(location)
    
    if not timezone_name:
        return {
            "error": f"Location '{location}' not recognized. Please try a major city or country name.",
            "status": "error"
        }
    
    try:
        # Get the timezone object
        timezone = pytz.timezone(timezone_name)
        
        # Get current time in the specified timezone
        current_time = datetime.datetime.now(timezone)
        
        # Format the time information
        return {
            "location": location,
            "timezone": timezone_name,
            "current_time": current_time.strftime("%Y-%m-%d %H:%M:%S"),
            "date": current_time.strftime("%Y-%m-%d"),
            "time": current_time.strftime("%H:%M:%S"),
            "day_of_week": current_time.strftime("%A"),
            "utc_offset": current_time.strftime("%z"),
            "status": "success"
        }
    except pytz.exceptions.UnknownTimeZoneError:
        return {
            "error": f"Unknown timezone '{timezone_name}' for location '{location}'.",
            "status": "error"
        }
    except Exception as e:
        return {
            "error": f"Error retrieving time: {str(e)}",
            "status": "error"
        }


if __name__ == "__main__":
    # Start the server
    print("🚀Starting time server... ")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--server_type", type=str, default="sse", choices=["sse", "stdio"]
    )
    args = parser.parse_args()
    
    print("Server type:", args.server_type)
    print("Launching on Port:", 3001)
    print('Check "http://localhost:3001/sse" for the server status')
    
    mcp.run(args.server_type)