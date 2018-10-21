import owlready2 as o
import sys

onto_symps = o.get_ontology("file://symp.owl")
onto_symps.load()

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

# TODO find out the proper pattern for ids
curr_id = 0
for symp in onto_symps.classes():
    if not symp.deprecated: # DISCUSS should we include deprecated symptoms?
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
