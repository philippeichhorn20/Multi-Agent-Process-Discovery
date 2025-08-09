from pm4py import PetriNet
from pm4py.objects.petri_net.utils import petri_utils
import networkx as nx
from networkx.algorithms import isomorphism, optimize_graph_edit_distance, graph_edit_distance, simrank_similarity
from services.interface_patterns import interface_patterns

def is_isomorph_with_algorithm(net1: PetriNet, net2: PetriNet): # under construction Todo
	# assumes each net has one starting place (only outgoing arcs)
    
    g1 = petri_net_to_networkx(net1)
    g2 = petri_net_to_networkx(net2)
    matcher = isomorphism.DiGraphMatcher(g1, g2,)
    is_isomorph = matcher.is_isomorphic()
    if(is_isomorph):
        return True
    else:
        return False

def edit_distance_heuristic(net1: PetriNet, net2: PetriNet):
    	# assumes each net has one starting place (only outgoing arcs)
    g1 = petri_net_to_networkx(net1)
    g2 = petri_net_to_networkx(net2)
    generator = optimize_graph_edit_distance(g1,g2)
    
    count  = 0
    for x in generator:
        count += 1
        dist = x
        if(count == 3):
            break
    return dist


def petri_net_to_networkx(petri_net):
    """
    Converts a Petri net into a NetworkX graph.
    """
    G = nx.DiGraph()
    
    # Add places as nodes
    for place in petri_net.places:
        G.add_node(place, node_type='place')
    
    # Add transitions as nodes
    for transition in petri_net.transitions:
        G.add_node(transition, node_type='transition')
    
    # Add arcs as edges
    for arc in petri_net.arcs:
        G.add_edge(arc.source, arc.target, weight=arc.weight)
    
    return G


def find_matching_interaction_pattern(net: PetriNet):
    ips = interface_patterns.get_patterns()
    x = 0
    for ip in ips:
        x = x + 1
        ip, _ , _ = ip
        if is_isomorph_with_algorithm(ip, net):
            return ip.name



