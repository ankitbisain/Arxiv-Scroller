import webbrowser
from datetime import datetime
from dataclasses import dataclass
from pylatexenc.latex2text import LatexNodes2Text


def compile(txt):
    return LatexNodes2Text().latex_to_text(txt)


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
        return display_fn(
            [header, compile(self.title), compile(self.abs_preview(abs_cut))]
        )

    def abs_preview(self, abs_cut):
        abs_words = self.abstract.split()
        abs_preview = " ".join(abs_words[:abs_cut])
        if len(abs_words) > abs_cut:
            abs_preview += "..."
        return abs_preview

    def abs_sentences(self):
        return [
            compile(line)
            for line in self.abstract.replace("et al.", "et al")
            .replace(". ", "...&&&")
            .split("&&&")
        ]

    def yield_abstract(self, display_fn):
        sentences = self.abs_sentences()
        for sentence in sentences:
            display_fn([sentence])
            if input() == "x":
                break

    def open(self):
        webbrowser.open(self.link)
