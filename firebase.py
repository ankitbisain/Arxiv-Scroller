import json

from fetcher import papers_from_codes
from db import clear_collection, db_add

with open("subjects.json") as f:
    codes_from_subject = json.load(f)

subjects = codes_from_subject.keys()


def db_entry_from_paper(paper, index, date_counts):
    header, title, abstract_preview = paper.preview(lambda x: x, date_counts, True, 20)
    preview = (
        header
        + f"<br><br><a href='{paper.link}' target='_blank'><b><big>"
        + title
        + "</big></b></a><br><br>"
        + abstract_preview
    )
    return {
        "id": index,
        "slides": [preview] + paper.abs_sentences(),
    }


for subject in subjects:
    collection_name = f"{subject}-papers"
    papers, date_counts = papers_from_codes(codes_from_subject[subject])
    clear_collection(collection_name)
    for index, paper in enumerate(papers):
        entry = db_entry_from_paper(paper, index + 1, date_counts)
        db_add(entry, collection_name)
    print(f"{collection_name} updated")
