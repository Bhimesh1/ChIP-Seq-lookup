# ChIP-Seq Similarity Lookup

This is a small prototype that compares a user-uploaded BED file to a database of ChIP-Seq peaks (from Monocyte CD14+ samples), and returns the most similar ones using the Jaccard index.

## How to Run

```
pip install -r requirements.txt
python app.py
```

Go to http://127.0.0.1:5000 in the browser.

## How it works
BED files are first compared using overlap in the intervals and

Similarity = Jaccard Index (Intersection / Union)

And then top 3 matches are shown