import rdflib
# from utils import syntax_to_owl
from utils import convert_list_queries_to_df


prefix = """
        PREFIX ns: <http://www.semanticweb.org/tinou/ontologies/2022/2/untitled-ontology-20#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX tg: <http://www.turnguard.com/functions#>
    """


def start_queries(ontology: str):
    g = rdflib.graph.ConjunctiveGraph()
    g.parse(ontology)
    return g


def query_get_all_nature(path: str):
    graph = start_queries(path)
    nature_query = """
        SELECT DISTINCT ?subsub
        WHERE {
            ?sub rdfs:subClassOf ns:Object .
            ?subsub rdfs:subClassOf ?sub . 
        }
    """
    res = graph.query(prefix + '\n' + nature_query)
    l_elt = [row.subsub.split('#')[1] for row in res]
    return l_elt


def query_get_all_type(path: str):
    graph = start_queries(path)
    type_query = """
            SELECT DISTINCT ?sub
            WHERE {
                ?sub rdfs:subClassOf ns:Object .
            }
        """
    res = graph.query(prefix + '\n' + type_query)
    l_elt = [row.sub.split('#')[1] for row in res]
    return l_elt


def query_get_nature_objects_found_group_by_train_station(path: str):
    graph = start_queries(path)
    condition_query = """
        SELECT DISTINCT ?nature ?name
        WHERE{
            ?type rdfs:subClassOf ns:Object .
            ?nature rdfs:subClassOf ?type . 
            ?obj rdf:type ?nature .
            ?obj ns:foundDate ?fDate .
            ?obj ns:hasBeenFoundHere ?place .
            ?place ns:name ?name .
        }
        GROUP BY ?name
        """
    res = graph.query(prefix + '\n' + condition_query)
    l_elt = [[row.nature.split('#')[1], row.name.value] for row in res]
    return l_elt


def query_get_group_by_train_station_having_more_than_3_object(path: str):
    graph = start_queries(path)
    condition_query = """
        SELECT ?name ?fDate (COUNT(?obj) as ?countObj)
        WHERE{
            ?type rdfs:subClassOf ns:Object .
            ?nature rdfs:subClassOf ?type . 
            ?obj rdf:type ?nature .
            ?obj ns:foundDate ?fDate .
            ?obj ns:hasBeenFoundHere ?place .
            ?place ns:name ?name .
            OPTIONAL {?obj ns:recoveredDate ?rDate}
        }
        GROUP BY ?name
        HAVING (?countObj > 3)
    """
    res = graph.query(prefix + '\n' + condition_query)
    l_elt = [[row.name.value, row.fDate.value, row.countObj] for row in res]
    return l_elt


def query_get_instances(path: str):
    graph = start_queries(path)
    condition_query = """
            SELECT ?type ?nature ?fDate ?rDate ?uic ?lat ?long
            WHERE {
                ?type rdfs:subClassOf ns:Object .
                ?nature rdfs:subClassOf ?type .
                ?obj rdf:type ?nature .
                ?obj ns:foundDate ?fDate .
                ?obj ns:recoveredDate ?rDate . 
                ?obj ns:hasBeenFoundHere ?place .
                ?place ns:name ?name .
                ?place ns:codeUIC ?uic .
                ?place ns:latitude ?lat .
                ?place ns:longitude ?long .
            }
    """
    res = graph.query(prefix + '\n' + condition_query)
    l_elt = [[row.type.split('#')[1], row.nature.split('#')[1], row.fDate.value, row.rDate.value, row.uic.value,
              float(row.lat.value), float(row.long.value)] for row in res]
    return l_elt


def query_condition_rdate_not_nan(path: str, nature: str, place: str):
    graph = start_queries(path)
    condition_query1 = """
        SELECT ?obj ?fDate ?rDate
        WHERE{
    """
    condition_query2 = f"""
            ?obj rdf:type ns:{nature}.
            ?obj ns:foundDate ?fDate. 
            ?obj ns:recoveredDate ?rDate. 
            ?obj ns:hasBeenFoundHere ns:{place}.
            FILTER(?rDate != "nan")
    """
    condition_query3 = """
    }
    """
    res = graph.query(prefix + '\n' + condition_query1 + condition_query2 + condition_query3)
    l_elt = [[row.obj('#')[1], row.fDate.value, row.rDate.value] for row in res]
    return l_elt


def query_condition_rdate_nan(path: str, nature: str, place: str):
    graph = start_queries(path)
    condition_query1 = """
        SELECT ?obj ?fDate ?rDate
        WHERE{
    """
    condition_query2 = f"""
            ?obj rdf:type ?{nature}.
            ?obj ns:foundDate ?fDate. 
            ?obj ns:recoveredDate ?rDate. 
            ?obj ns:hasBeenFoundHere ns:{place}.
            FILTER(?rDate = "nan")
    """
    condition_query3 = """
    }
    """
    res = graph.query(prefix + '\n' + condition_query1 + condition_query2 + condition_query3)
    l_elt = [[row.obj.split('#')[1], row.fDate.value, row.rDate.value] for row in res]
    return l_elt


def query_get_train_station_by_zipcode(path: str, zipcode: str):
    graph = start_queries(path)
    condition_query1 = """
        SELECT DISTINCT ?place ?zipcode
        WHERE{
    """
    condition_query2 = f"""
            ?type rdfs:subClassOf ns:Object .
            ?nature rdfs:subClassOf ?type .
            ?obj rdf:type ?nature .
            ?obj ns:hasBeenFoundHere ?place.
            ?place ns:zipcode ?zipcode.
            FILTER(?zipcode = "{zipcode}")
    """
    condition_query3 = """
    }
    """
    res = graph.query(prefix + '\n' + condition_query1 + condition_query2 + condition_query3)
    elt = [row.place.split('#')[1] for row in res]
    return ''.join(elt)


def query_get_last_date_of_lost_objects(path: str):
    graph = start_queries(path)
    condition_query = """
        SELECT ?fDate ?name
        WHERE{
            ?type rdfs:subClassOf ns:Object .
            ?nature rdfs:subClassOf ?type . 
            ?obj rdf:type ?nature .
            ?obj ns:foundDate ?fDate.
            ?obj ns:hasBeenFoundHere ?place.
            ?place ns:name ?name.
    }
    ORDER BY DESC(?fDate)
    """
    res = graph.query(prefix + '\n' + condition_query)
    l_elt = [[row.fDate.value, row.name.value] for row in res][0]
    return l_elt


def query_get_lost_object_with_conditions(path: str, nature: str, zipcode: str, hasRecoveredDate: str):
    graph = start_queries(path)
    condition_query1 = """
    SELECT ?type ?fDate ?rDate ?zipcode ?lat ?long ?city
    WHERE {
    """
    if nature == 'nature':
        condition_query2 = f"""
            ?nature rdfs:subClassOf ?type . 
            ?obj rdf:type ?nature.
            ?obj ns:foundDate ?fDate.
            ?obj ns:recoveredDate ?rDate.
        """
    else:
        condition_query2 = f"""
            ns:{nature} rdfs:subClassOf ?type . 
            ?obj rdf:type ns:{nature}.
            ?obj ns:foundDate ?fDate.
            ?obj ns:recoveredDate ?rDate.
        """

    if hasRecoveredDate == "Oui":
        condition_query_optional = f"""
            FILTER(?rDate != "nan")
            ?obj ns:hasBeenFoundHere ?place.
            ?place ns:zipcode ?zipcode.
        """
    else:
        condition_query_optional = f"""
            FILTER(?rDate = "nan")
            ?obj ns:hasBeenFoundHere ?place.
            ?place ns:zipcode ?zipcode.
        """

    if zipcode != 'zipcode':
        condition_query_optional2 = f'    FILTER(?zipcode = "{zipcode}")\n'
    else:
        condition_query_optional2 = ''

    condition_query3 = f"""
        ?place ns:latitude ?lat.
        ?place ns:longitude ?long.
        ?place ns:city ?city.
    """
    condition_query4 = """
    }
    ORDER BY DESC(?fDate)
    """
    res = graph.query(prefix + '\n' + condition_query1 + condition_query2 + condition_query_optional + condition_query_optional2 + condition_query3 + condition_query4)
    # print(prefix + '\n' + condition_query1 + condition_query2 + condition_query_optional + condition_query_optional2 + condition_query3 + condition_query4)
    l_elt = [[row.type.split('#')[1], row.fDate.value, row.rDate.value, row.zipcode.value, row.lat.value, row.long.value, row.city.value] for row in res]
    df = convert_list_queries_to_df(l_queries=l_elt,
                                    l_cols=['Type of the Object', 'Found Date', 'Reovered Date',
                                            'Zipcode of the Station', 'Latitude', 'longitude', 'City of the Station'])
    return df


if __name__ == "__main__":
    path_owl_file = './data/output_context.owl'

    q = query_get_lost_object_with_conditions(path_owl_file, 'AirPod_casque_audio_ecouteurs', 'zipcode', 'Oui')
    print(q)
