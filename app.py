from flask import Flask, request, render_template
import os

app = Flask(__name__)

# this is a function to read a BED file and return the intervals as tuples
def read_bed(file_path):
    intervals = []
    with open(file_path) as f:
        for line in f:
            if line.startswith('#') or line.strip() == '':
                continue
            parts = line.strip().split('\t')
            if len(parts) >= 3:
                chrom, start, end = parts[0], int(parts[1]), int(parts[2])
                intervals.append((chrom, start, end))
    return intervals

# this function calculates the Jaccard index between the two lists of intervals
def jaccard_index(set1, set2):
    intersect = 0
    union = 0
    for i in set1:
        for j in set2:
            if i[0] != j[0]:  # chromosomes must match
                continue
            start = max(i[1], j[1])
            end = min(i[2], j[2])
            if start < end:
                intersect += end - start
            union += (i[2] - i[1]) + (j[2] - j[1])
    union = union - intersect  # removes overlapping part once
    if union == 0:
        return 0
    return intersect / union

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file:
            # Reads uploaded BED
            user_intervals = read_bed(uploaded_file)

            # Reads each database BED and compares
            db_dir = 'static'
            scores = []
            for filename in os.listdir(db_dir):
                if filename.endswith('.bed'):
                    db_path = os.path.join(db_dir, filename)
                    db_intervals = read_bed(db_path)
                    score = jaccard_index(user_intervals, db_intervals)
                    scores.append((filename, score))

            # Sorts by Jaccard score
            scores.sort(key=lambda x: x[1], reverse=True)
            results = scores[:3]  # top 3 matches

    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
