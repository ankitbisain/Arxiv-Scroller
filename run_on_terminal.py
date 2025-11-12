import sys
from functools import partial

from fetcher import papers_from_codes
from display_terminal import fit_to_screen

MARGIN = 10
COLOR = "\033[47m\033[30m"
DISPLAY_FN = partial(fit_to_screen, margin=MARGIN, color=COLOR)
ABS_CUT = 20
DEFAULT_AUTH = False
CODES = sys.argv[1:]

papers, date_counts = papers_from_codes(CODES)

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
