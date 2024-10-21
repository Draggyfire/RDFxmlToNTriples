import rdflib
import sys

def convert_rdfxml_to_ntriples(rdfxml_file, ntriples_file):
    # Création du graphe RDF
    graph = rdflib.Graph()

    # Lecture du fichier RDF/XML
    graph.parse(rdfxml_file, format="xml")

    # Filtrer et ne garder que les triples qui ont les attributs spécifiés
    with open(ntriples_file, 'w') as f:
        for subj, pred, obj in graph:
            # Filtrer les attributs spécifiés dans les URI
            subj_str = f"<{subj}>" if isinstance(subj, rdflib.URIRef) else f"_:{subj}"
            pred_str = f"<{pred}>"

            if isinstance(obj, rdflib.URIRef):  # rdf:resource
                obj_str = f"<{obj}>"
            elif isinstance(obj, rdflib.BNode):  # rdf:nodeID
                obj_str = f"_:{obj}"
            elif isinstance(obj, rdflib.Literal):  # rdf:datatype, xml:lang
                lang = f"@{obj.language}" if obj.language else ""
                datatype = f"^^<{obj.datatype}>" if obj.datatype else ""
                obj_str = f"\"{obj}\"{lang}{datatype}"
            else:
                obj_str = f"\"{obj}\""

            # Écrire le triple dans le fichier N-Triples
            f.write(f"{subj_str} {pred_str} {obj_str} .\n")

    print(f"Conversion réussie. Le fichier N-Triples est enregistré sous : {ntriples_file}")

if __name__ == "__main__":
    # Vérifier si le fichier XML a été passé en argument
    if len(sys.argv) < 2:
        print("Usage: python3 test.py <input_rdfxml_file>")
    else:
        rdfxml_file = sys.argv[1]  # Le fichier RDF/XML en entrée
        ntriples_file = 'output.nt'  # Nom de fichier de sortie par défaut
        convert_rdfxml_to_ntriples(rdfxml_file, ntriples_file)
