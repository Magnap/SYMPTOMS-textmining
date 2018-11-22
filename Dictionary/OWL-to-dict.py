import owlready2 as o
import sys
import os

onto_symps = o.get_ontology("file://symp.owl")
onto_symps.load()

dict_dir = "./symptoms_dictionary"
if not os.path.exists(dict_dir):
    os.mkdir(dict_dir)
else:
    sys.exit("Disease dictionary directory already exists,\
    aborting to avoid overwriting existing dictionary")
os.chdir(dict_dir)

class Symptom():
    def __init__(self, internal_id, onto_symp):
        self.internal_id = internal_id
        self.symp_id = onto_symp.id[0]
        self.names = onto_symp.label + onto_symp.hasExactSynonym + symp.hasRelatedSynonym
        self.parents = onto_symp.ancestors() - {onto_symp, o.owl.Thing}
        self.other_ids = onto_symp.hasDbXref

symps = {}
symp_internal_ids = {}

# TODO tackle alternative IDs (hasAlternativeId)

curr_id = 1017000001
for symp in onto_symps.classes():
    if not symp.deprecated:
        if not symp.id:
            print("Warning: symptom",symp.name,"is missing a SYMP id, creating one automatically", file=sys.stderr)
            symp.id = ['SYMP:' + symp.name[5:]]
        symps[curr_id] = Symptom(curr_id, symp)

        symp_internal_ids[symp] = curr_id

        curr_id = curr_id + 1

for symp in symps.values():
    symp.parents = {symp_internal_ids[p] for p in symp.parents}

# For convenience while developing
symp_by_name = {}
for symp in symps.values():
    for name in symp.names:
        symp_by_name[name] = symp

with open('symptoms_entities.tsv','a') as entities_file, \
     open('symptoms_groups.tsv','a') as groups_file, \
     open('symptoms_global.tsv','a') as global_file, \
     open('symptoms_names.tsv','a') as names_file:
    for symp in symps.values():
        for name in symp.names:
            if len(name) <= 3:
                # Don't ignore symptom names 3 chars or less
                global_file.write(name + "\t" + "f\n")
        for identifier in symp.names + symp.other_ids + [symp.symp_id]:
            names_file.write(str(symp.internal_id) + "\t" + identifier + "\n")
        for parent in symp.parents:
            groups_file.write(str(symp.internal_id) + "\t" + str(parent) + "\n")
        entities_file.write(
            str(symp.internal_id) + "\t" +
            "-37" + "\t" + # DISCUSS which magic number for symptoms?
            symp.symp_id + "\n") # Canonical ID

