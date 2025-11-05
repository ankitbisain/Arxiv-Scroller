import sys
from collections import defaultdict
from functools import partial

from fetcher import papers_from_url
from display import fit_to_screen

MARGIN = 10
COLOR = "\033[47m\033[30m"
DISPLAY_FN = partial(fit_to_screen, margin=MARGIN, color=COLOR)
ABS_CUT = 20
DEFAULT_AUTH = False
URL = f"https://arxiv.org/list/math.{sys.argv[1].upper()}/recent?skip=0&show=2000"

# get recent papers and date counts
papers = papers_from_url(URL)
papers.sort(key=lambda x: x.date, reverse=True)
date_counts = defaultdict(int)
for paper in papers:
    date_counts[paper.date] += 1
    paper.index = date_counts[paper.date]

# scroll papers
i = 0
while True:
    paper = papers[i % len(papers)]
    auth = DEFAULT_AUTH
    while True:
        paper.preview(DISPLAY_FN, date_counts, auth=auth, abs_cut=ABS_CUT)
        match input():
            case "m":
                paper.open()
            case "c":
                paper.yield_abstract(DISPLAY_FN)
            case "a":
                auth = not auth
            case "z":
                i += -1
                break
            case "q":
                sys.exit()
            case _:
                i += 1
                break
