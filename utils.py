from datetime import datetime, timezone, timedelta
import time
import os
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional


class AocInput:
    def __init__(self, session_token: Optional[str] = None):
        self.session_token = session_token or os.getenv("AOC_SESSION")
        if not self.session_token:
            raise ValueError("Session token must be provided either through AOC_SESSION environment variable or constructor")

        self.base_dir = Path.cwd()

    def get_input(self, year: int, day: int) -> str:
        filepath = self._get_file_path(year, day)

        if filepath.exists():
            print(f"Using cached input from {filepath}.")
            return filepath.read_text()

        input_text = self._download(year, day)
        self._save(filepath, input_text)
        print(f"Input for {year} day {day} downloaded and saved to {filepath}.")
        return input_text

    def get_input_lines(self, year: int, day: int) -> list[str]:
        return [line.strip() for line in self.get_input(year, day).splitlines()]

    def get_input_ints(self, year: int, day: int) -> list[int]:
        return [int(line) for line in self.get_input_lines(year, day)]

    def _download(self, year: int, day: int) -> str:
        url = f"https://adventofcode.com/{year}/day/{day}/input"
        headers = {"Cookie": f"session={self.session_token}"}

        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req) as response:
                return response.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"Failed to download input: HTTP {e.code}") from e
        except urllib.error.URLError as e:
            raise RuntimeError(f"Failed to download input: {e.reason}") from e

    def _get_file_path(self, year: int, day: int) -> Path:
        return self.base_dir / f"day{day:02d}.txt"

    def _save(self, filepath: Path, content: str) -> None:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content)


if __name__ == "__main__":
    aoc = AocInput()
    utc = datetime.now(timezone.utc)
    # Use time.localtime() to properly detect DST for Eastern Time
    is_dst = time.localtime().tm_isdst > 0
    # Adjust offset based on DST
    offset = -4 if is_dst else -5
    # Convert UTC to Eastern with correct offset
    now = utc.astimezone(timezone(timedelta(hours=offset)))
    print("Now", now)
    input_text = aoc.get_input(now.year, now.day)  # assuming we are running it in December
    print(input_text)
