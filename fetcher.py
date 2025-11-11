import arxiv
import requests
from bs4 import BeautifulSoup

from paper import Paper


def result_to_paper(result):
    return Paper(
        date=max(result.updated, result.published).date(),
        title=str(result.title),
        abstract=str(result.summary).replace("\n", " "),
        authors=str(", ".join(person.name for person in result.authors)),
        link=str(result.entry_id).replace("abs", "pdf"),
    )


def url_from_code(code):
    return f"https://arxiv.org/list/math.{code}/recent?skip=0&show=2000"


def ids_from_url(url):
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    papers = soup.find_all("dt")
    return [
        paper.find("a", title="Abstract")["href"].split("/")[-1] for paper in papers
    ]


def ids_from_codes(codes):
    all_ids = []
    for code in codes:
        all_ids.extend(ids_from_url(url_from_code(code)))
    return list(set(all_ids))


def papers_from_codes(codes):
    client = arxiv.Client()
    search = arxiv.Search(id_list=ids_from_codes(codes))
    return [result_to_paper(result) for result in client.results(search)]
