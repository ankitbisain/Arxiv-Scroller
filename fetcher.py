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


def ids_from_url(url):
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    papers = soup.find_all("dt")
    return [
        paper.find("a", title="Abstract")["href"].split("/")[-1] for paper in papers
    ]


def papers_from_url(url):
    client = arxiv.Client()
    search = arxiv.Search(id_list=ids_from_url(url))
    return [result_to_paper(result) for result in client.results(search)]