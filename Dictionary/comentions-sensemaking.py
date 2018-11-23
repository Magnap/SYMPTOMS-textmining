import csv

class Pair():
    def __init__(self, disease, symptom, strength):
        self.disease = disease
        self.symptom = symptom
        self.strength = float(strength)

pairs = []
with open("output-pairs", newline='') as pair_file:
    pair_reader = csv.reader(pair_file, "excel-tab")
    for row in pair_reader:
        pairs.append(Pair(row[0], row[1], row[2]))

names = {}
with open("combined_dictionary/combined_names.tsv", newline='') as name_file:
    name_reader = csv.reader(name_file, "excel-tab")
    for row in name_reader:
        entity_id = row[0]
        name = row[1]
        if not ':' in name:
            if entity_id in names:
                names[entity_id].add(name)
            else:
                names[entity_id] = set([name])

with open("named-pairs.tsv", 'w', newline='') as f:
    writer = csv.writer(f, "excel-tab")
    for pair in pairs:
        dis_name_short = sorted(names.get(pair.disease, ["Unnamed disease"]), key=len)[0]
        symp_name_short = sorted(names.get(pair.symptom, ["Unnamed symptom"]), key=len)[0]
        dis_name_long = sorted(names.get(pair.disease, ["Unnamed disease"]), key=len, reverse=True)[0]
        symp_name_long = sorted(names.get(pair.symptom, ["Unnamed symptom"]), key=len, reverse=True)[0]
        writer.writerow([dis_name_short, symp_name_short, pair.strength, dis_name_long, symp_name_long, pair.disease, pair.symptom])
