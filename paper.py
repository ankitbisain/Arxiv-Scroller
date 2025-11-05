import webbrowser
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Paper:
    date: datetime
    title: str
    abstract: str
    authors: str
    link: str
    index: int = 0

    def preview(self, display_fn, date_counts, auth, abs_cut):
        header = (
            self.date.strftime("%m-%d")
            + f" ({self.index}/{date_counts[self.date]})"
            + (" - " + self.authors if auth else "")
        )
        display_fn([header, self.title, self.abs_preview(abs_cut)])

    def abs_preview(self, abs_cut):
        abs_words = self.abstract.split()
        abs_preview = " ".join(abs_words[:abs_cut])
        if len(abs_words) > abs_cut:
            abs_preview += "..."
        return abs_preview

    def yield_abstract(self, display_fn):
        sentences = self.abstract.replace(". ", "...&&&").split("&&&")
        for sentence in sentences:
            display_fn([sentence])
            if input() == "x":
                break

    def open(self):
        webbrowser.open(self.link)
