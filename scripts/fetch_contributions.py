#!/usr/bin/env python3
"""Fetch GitHub contribution data without API token.

Scrapes the public contribution calendar from:
https://github.com/users/<username>/contributions

Outputs data/contributions.json with:
- Raw daily contributions
- Current streak
- Longest streak
- Best day
- Monthly totals
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

import requests
from bs4 import BeautifulSoup

# Configuration - EDIT THIS
USERNAME = "basitali08"


def fetch_contributions(username: str) -> list[dict]:
    """Fetch contribution data from GitHub."""
    url = f"https://github.com/users/{username}/contributions"
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; ContributionGraph/1.0)"
    }

    print(f"Fetching contributions from {url}...")
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    contributions = []
    # Find all day cells in the contribution graph
    day_cells = soup.find_all("td", class_="ContributionCalendar-day")

    for cell in day_cells:
        date_str = cell.get("data-date")
        level = cell.get("data-level", "0")
        count_text = cell.get("aria-label", "")

        if date_str:
            # Parse count from aria-label like "3 contributions on January 1, 2024"
            try:
                count = int(count_text.split()[0]) if count_text.split()[0].isdigit() else 0
            except (IndexError, ValueError):
                count = 0

            contributions.append({
                "date": date_str,
                "count": count,
                "level": int(level),
            })

    return contributions


def calculate_stats(contributions: list[dict]) -> dict:
    """Calculate contribution statistics."""
    if not contributions:
        return {
            "total": 0,
            "current_streak": 0,
            "longest_streak": 0,
            "best_day": {"date": "", "count": 0},
            "monthly_totals": {},
        }

    # Sort by date
    contributions.sort(key=lambda x: x["date"])

    total = sum(c["count"] for c in contributions)

    # Calculate streaks
    current_streak = 0
    longest_streak = 0
    temp_streak = 0
    best_day = {"date": "", "count": 0}

    today = datetime.now().date()
    yesterday = today - timedelta(days=1)

    # Check if today or yesterday has contributions for current streak
    dates_with_contributions = {c["date"] for c in contributions if c["count"] > 0}

    # Current streak (from today backwards)
    check_date = today
    while check_date.isoformat() in dates_with_contributions:
        current_streak += 1
        check_date -= timedelta(days=1)

    # If today has no contributions, check from yesterday
    if current_streak == 0:
        check_date = yesterday
        while check_date.isoformat() in dates_with_contributions:
            current_streak += 1
            check_date -= timedelta(days=1)

    # Longest streak and best day
    for contrib in contributions:
        if contrib["count"] > 0:
            temp_streak += 1
            longest_streak = max(longest_streak, temp_streak)
        else:
            temp_streak = 0

        if contrib["count"] > best_day["count"]:
            best_day = {"date": contrib["date"], "count": contrib["count"]}

    # Monthly totals
    monthly_totals = {}
    for contrib in contributions:
        month_key = contrib["date"][:7]  # YYYY-MM
        monthly_totals[month_key] = monthly_totals.get(month_key, 0) + contrib["count"]

    return {
        "total": total,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": best_day,
        "monthly_totals": monthly_totals,
    }


def main():
    username = USERNAME

    contributions = fetch_contributions(username)
    stats = calculate_stats(contributions)

    output_data = {
        "username": username,
        "fetched_at": datetime.now().isoformat(),
        "stats": stats,
        "contributions": contributions,
    }

    # Ensure data directory exists
    Path("data").mkdir(exist_ok=True)

    output_path = "data/contributions.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)

    print(f"Saved {len(contributions)} days of contribution data to {output_path}")
    print(f"Total contributions: {stats['total']}")
    print(f"Current streak: {stats['current_streak']} days")
    print(f"Longest streak: {stats['longest_streak']} days")


if __name__ == "__main__":
    main()
