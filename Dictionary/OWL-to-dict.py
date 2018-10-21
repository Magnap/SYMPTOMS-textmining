import owlready2 as o

onto_symps = o.get_ontology("file://symp.owl") # DISCUSS make this a commandline argument?
onto_symps.load()
