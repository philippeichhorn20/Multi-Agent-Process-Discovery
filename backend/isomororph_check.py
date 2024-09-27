from pm4py import PetriNet
import pm4py
from pm4py.objects.petri_net.utils import petri_utils
import networkx as nx
from networkx.algorithms import isomorphism, optimize_graph_edit_distance, graph_edit_distance, simrank_similarity
from interface_patterns import interface_patterns

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


def vf2_petri_net(net1: PetriNet, net2: PetriNet):
    # Check if the number of places and transitions are the same
    if len(net1.places) != len(net2.places) or len(net1.transitions) != len(net2.transitions):
        return False
 
    # Recursive backtracking function to find isomorphism
    def is_isomorphic(mapping, unmatched1, unmatched2):
        # Base case: all nodes are matched
        if not unmatched1 and not unmatched2:
            return True

        # Try to match remaining nodes
        for node1 in unmatched1:
            for node2 in unmatched2:
                if is_feasible(node1, node2, mapping):
                    new_mapping = mapping.copy()
                    new_mapping[node1] = node2
                    
                    # Continue matching remaining nodes
                    new_unmatched1 = unmatched1 - {node1}
                    new_unmatched2 = unmatched2 - {node2}
                    
                    if is_isomorphic(new_mapping, new_unmatched1, new_unmatched2):
                        return True
        
        # No valid mapping found, backtrack
        return False

    # Feasibility check to match node1 (from net1) with node2 (from net2)
    def is_feasible(node1, node2, mapping):
        # Ensure that we are matching places to places and transitions to transitions
        if (node1 in net1.places and node2 not in net2.places) or \
           (node1 in net1.transitions and node2 not in net2.transitions):
            return False
        
        # Check if the sources are in the mapping before accessing
        pre_set_node1 = {mapping[x.source] for x in node1.in_arcs if x.source in mapping}
        pre_set_node2 = {x.source for x in node2.in_arcs}
        post_set_node1 = {mapping[x.target] for x in node1.out_arcs if x.target in mapping}
        post_set_node2 = {x.target for x in node2.out_arcs}  # Changed from x.source to x.target


        return len(pre_set_node1.difference(pre_set_node2)) == 0 and len(post_set_node1.difference(post_set_node2)) == 0

    # Start with no mappings and all nodes unmatched
    return is_isomorphic({}, net1.places | net1.transitions, net2.places | net2.transitions)





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


def matching_ip(net: PetriNet):
    ips = interface_patterns.get_patterns()
    x = 0
    for ip in ips:
        x = x + 1
        ip, _ , _ = ip
        if is_isomorph_with_algorithm(ip, net):
            return ip.name



