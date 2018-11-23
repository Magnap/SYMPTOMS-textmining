import csv
import random

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

class Mention():
    def __init__(self):
        self.mentions = 0
        self.pubmed_ids = set()
        self.entities = set()
        self.names = set()

    def add_mention(self, pubmed_id, entity_id):
        self.mentions = self.mentions + 1
        self.pubmed_ids.add(pubmed_id)
        self.entities.add(entity_id)
        self.names |= names[entity_id]



mentions = {}
with open("output-mentions", newline='') as mention_file:
    mention_reader = csv.reader(mention_file, "excel-tab")
    for row in mention_reader:
        pubmed_id = row[0]
        term = row[5]
        type_id = row[6]
        entity_id = row[7]
        if type_id == '-37' and entity_id != '1017000371':
            if not term in mentions:
                mentions[term] = Mention()
            mentions[term].add_mention(pubmed_id, entity_id)

with open("blacklist-guide.tsv", "w", newline='') as guide_file:
    guide_writer = csv.writer(guide_file, "excel-tab")
    for (term, mention) in mentions.items():
        if len(mention.pubmed_ids) >= 5:
            for pubmed_id in random.sample(mention.pubmed_ids, 5):
                link = "https://www.ncbi.nlm.nih.gov/pubmed/?term="+pubmed_id
                guide_writer.writerow([mention.mentions, term, link, mention.names, mention.entities])
