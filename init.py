import sys
import datetime
from pathlib import Path
import requests


with open('session.txt', 'r') as f:
    session = f.read().strip()

if len(sys.argv) > 1:
    day = int(sys.argv[1])
else:
    tz = datetime.timezone(datetime.timedelta(hours=-5))  # new puzzles release at 00:00 UTC-5
    day = datetime.datetime.now(tz).day


day_dir = Path(f'day{day}')
day_dir.mkdir(exist_ok=True)

solve_path = day_dir / 'solve.py'
if not solve_path.exists():
    solve_path.write_text('''with open('input.txt', 'r') as f:\n    lines = f.read().splitlines()\n''')


input_path = day_dir / 'input.txt'

res = requests.get(f'https://adventofcode.com/2020/day/{day}/input', cookies={'session': session})
res.raise_for_status()
with input_path.open('wb') as f:
    f.write(res.content)
print(f'[+] Successfully retrieved input for day {day} ({len(res.content)} bytes, {len(res.text.splitlines())} lines)')
