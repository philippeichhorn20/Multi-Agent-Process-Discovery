import pm4py
from pm4py import PetriNet
from itertools import permutations
from typing import Dict
from Refiner import Refiner

from collections import deque
from itertools import combinations
from isomororph_check import vf2_petri_net, is_isomorph_with_algorithm, edit_distance_heuristic

# class PetriNet(PN):
#     def __lt__(self, other):
#         diff_self = len(self.transitions) + len(self.places) + len(self.arcs)
#         diff_other = len(other.transitions) + len(other.places) + len(other.arcs)
#         return diff_self < diff_other


def is_refinement_via_astar(goal_net: PetriNet, net_B: PetriNet) -> bool:
    """
    This function attempts to determine if net_B can be refined to match net_A
    using the transformations defined in the Refiner class, using the A* algorithm.
    """
    from queue import PriorityQueue
    def count_arcs(elements):
        in_arc_counts = {}
        out_arc_counts = {}
        for e in elements:
            in_count = len(e.in_arcs)
            out_count = len(e.out_arcs)
            in_arc_counts[in_count] = in_arc_counts.get(in_count, 0) + 1
            out_arc_counts[out_count] = out_arc_counts.get(out_count, 0) + 1
        return in_arc_counts, out_arc_counts

    def calculate_arc_diff(net_counts, goal_counts):
        arc_diff = 0
        for count in set(net_counts.keys()) | set(goal_counts.keys()):
            arc_diff += abs(net_counts.get(count, 0) - goal_counts.get(count, 0))
        return arc_diff
    def heuristic(net, goal_net):
        heur = edit_distance_heuristic(net, goal_net)
        diff = 0.0 + abs(len(goal_net.transitions) - len(net.transitions)) + abs(len(goal_net.places) - len(net.places)) + abs(len(goal_net.arcs) - len(net.arcs))
        return diff + heur 

        # Compare transitions by number of in_arcs and out_arcs
        net_t_in_counts, net_t_out_counts = count_arcs(net.transitions)
        goal_t_in_counts, goal_t_out_counts = count_arcs(goal_net.transitions)
        
        
        # Compare places by number of in_arcs and out_arcs
        net_p_in_counts, net_p_out_counts = count_arcs(net.places)
        goal_p_in_counts, goal_p_out_counts = count_arcs(goal_net.places)

        return   diff + 1

    start_state = (net_B, [])
    goal_state = goal_net

    frontier = PriorityQueue()
    start_state_id = get_state_identifier(net_B, [])
    frontier.put((0, start_state_id))
    
    came_from = {}
    cost_so_far = {start_state_id: 0}
    state_map = {start_state_id: start_state}

    step_count = 0

    while not frontier.empty():
        step_count += 1
        current_priority, current_state_id = frontier.get()
        current_net, applied_operations = state_map[current_state_id]

        # print(f"\nStep {step_count}: Current applied operations: {applied_operations}")
        pm4py.view_petri_net(current_net)

        if are_petri_nets_isomorphic(current_net, goal_state):
            print("Refinement successful with operations:", applied_operations)
            pm4py.view_petri_net(current_net)
            return True

        possible_transformations = []

        for place in current_net.places:
            possible_transformations.append(('place_duplicater', place))
            possible_transformations.append(('local_transition_adder', place))
            in_arc_combinations = get_in_arc_subsets(place)
            for subset in in_arc_combinations:
                possible_transformations.append(('place_splitter', place, subset))

        for transition in current_net.transitions:
            possible_transformations.append(('transition_duplicator', transition))

        print(f"Number of possible transformations: {len(possible_transformations)}")

        for transformation in possible_transformations:
            new_net = current_net.__deepcopy__()
            if transformation[0] == 'place_duplicater':
                Refiner.place_duplicater(new_net, transformation[1])
            elif transformation[0] == 'transition_duplicator':
                Refiner.transition_duplicator(new_net, transformation[1])
            elif transformation[0] == 'local_transition_adder':
                Refiner.local_transition_adder(new_net, transformation[1])
            elif transformation[0] == 'place_splitter':
                Refiner.place_splitter(new_net, transformation[1], transformation[2])

            new_operations = applied_operations + [transformation]
            new_state_id = get_state_identifier(new_net, new_operations)

            new_cost = cost_so_far[current_state_id] + 1
            if new_state_id not in cost_so_far or new_cost < cost_so_far[new_state_id]:
                cost_so_far[new_state_id] = new_cost
                priority = new_cost + heuristic(new_net, goal_state)
                frontier.put((priority, new_state_id))
                came_from[new_state_id] = current_state_id
                state_map[new_state_id] = (new_net, new_operations)

    print("No refinement found.")
    return False


def get_in_arc_subsets(place: PetriNet.Place):
	"""
	Helper function to generate all non-empty subsets of in-arcs of a given place.
	"""
	in_arcs = list(place.in_arcs)
	subsets = []
	for r in range(1, len(in_arcs) + 1):
		subsets.extend(combinations(in_arcs, r))
	return [set(subset) for subset in subsets]

def get_state_identifier(net: PetriNet, operations: list):
	"""
	Generates a unique identifier for a given state based on the net and applied operations.
	This helps in checking if a state has already been visited.
	"""
	# Example: concatenate a sorted list of operation strings
	operation_strings = [f"{op[0]}-{op[1].name}" if len(op) == 2 else f"{op[0]}-{op[1].name}-{len(op[2])}" for op in operations]
	return f"Net({len(net.places)}, {len(net.transitions)}, {len(net.arcs)})_" + "_".join(sorted(operation_strings))



def are_petri_nets_isomorphic(net1: PetriNet, net2: PetriNet) -> bool:
	# Check if the number of places, transitions, and arcs are the same
	
	print("Proper isomorphism check starting!!")
	return is_isomorph_with_algorithm(net1, net2)
	
	if len(net1.places) != len(net2.places):
		# print("Different number of places:", len(net1.places), "vs", len(net2.places))
		return False
	if len(net1.transitions) != len(net2.transitions):
		# print("Different number of transitions:", len(net1.transitions), "vs", len(net2.transitions))
		return False
	if len(net1.arcs) != len(net2.arcs):
		# print("Different number of arcs:", len(net1.arcs), "vs", len(net2.arcs))
		return False

	# Convert sets to lists for permutation generation
	places1 = list(net1.places)
	places2 = list(net2.places)
	transitions1 = list(net1.transitions)
	transitions2 = list(net2.transitions)

	# Generate all permutations of places and transitions of net2
	for place_perm in permutations(places2):
		for trans_perm in permutations(transitions2):
			# Create a mapping based on current permutation
			place_map: Dict[PetriNet.Place, PetriNet.Place] = {p1: p2 for p1, p2 in zip(places1, place_perm)}
			trans_map: Dict[PetriNet.Transition, PetriNet.Transition] = {t1: t2 for t1, t2 in zip(transitions1, trans_perm)}

			# print("\nTrying permutation:")
			# print("Place mapping:", {p.name: place_map[p].name for p in place_map})
			# print("Transition mapping:", {t.name: trans_map[t].name for t in trans_map})

			# Verify if the arc structures are preserved under the current mappings
			if check_arc_structure(net1, net2, place_map, trans_map):
				print("Isomorphic mapping found.")
				return True
			# else:
			# 	# print("Mapping did not preserve arc structure.")

	print("No isomorphic mapping found.")
	return False

def check_arc_structure(
	net1: PetriNet,
	net2: PetriNet,
	place_map: Dict[PetriNet.Place, PetriNet.Place],
	trans_map: Dict[PetriNet.Transition, PetriNet.Transition]
) -> bool:
	# Create a set of mapped arcs from net1 to compare with arcs in net2
	mapped_arcs = set()

	for arc in net1.arcs:
		mapped_source = place_map.get(arc.source, trans_map.get(arc.source, None))
		mapped_target = place_map.get(arc.target, trans_map.get(arc.target, None))

		if mapped_source is None or mapped_target is None:
			print("Arc source/target mapping not found for arc:", arc)
			return False

		mapped_arc = PetriNet.Arc(mapped_source, mapped_target, weight=arc.weight)
		mapped_arcs.add(mapped_arc)

	# Compare the mapped arcs with the actual arcs in net2 manually
	for mapped_arc in mapped_arcs:
		found_match = False
		for net2_arc in net2.arcs:
			if (
				mapped_arc.source == net2_arc.source and
				mapped_arc.target == net2_arc.target and
				mapped_arc.weight == net2_arc.weight
			):
				found_match = True
				break

		if not found_match:
			# print(f"Mapped arc {mapped_arc} does not match any arc in net2.")
			return False

	# Ensure every arc in net2 also has a corresponding mapped arc
	for net2_arc in net2.arcs:
		found_match = False
		for mapped_arc in mapped_arcs:
			if (
				mapped_arc.source == net2_arc.source and
				mapped_arc.target == net2_arc.target and
				mapped_arc.weight == net2_arc.weight
			):
				found_match = True
				break

		if not found_match:
			# print(f"Net2 arc {net2_arc} does not match any mapped arc.")
			return False
	return True



# Helper functions
def rho1(net: PetriNet):
	# Implement transformation ρ1 (serial place refinement)
	Refiner.local_transition_adder(net)
	return net

def rho2(net):
	# Implement transformation ρ2 (parallel place refinement)
	pass

def rho3(net):
	# Implement transformation ρ3 (optional loop addition)
	pass

def rho4(net):
	# Implement transformation ρ4 (transition refinement)
	pass

# # Create net1
# p1 = PetriNet.Place('p1')
# p2 = PetriNet.Place('p2')
# t1 = PetriNet.Transition('t1')

# arc1_net1 = PetriNet.Arc(p1, t1)
# arc2_net1 = PetriNet.Arc(t1, p2)

# net1 = PetriNet(
# 	name="net1",
# 	places={p1, p2},
# 	transitions={t1},
# 	arcs={arc1_net1, arc2_net1}
# )

# # Create net2
# a = PetriNet.Place('a')
# b = PetriNet.Place('b')
# x = PetriNet.Transition('x')

# arc1_net2 = PetriNet.Arc(a, x)
# arc2_net2 = PetriNet.Arc(x, b)

# net2 = PetriNet(
# 	name="net2",
# 	places={a, b},
# 	transitions={x},
# 	arcs={arc1_net2, arc2_net2}
# )

# # Check if the two nets are isomorphic
# isomorphic = are_petri_nets_isomorphic(net1, net2)
# if isomorphic:
# 	print("The two Petri nets are isomorphic.")
# else:
# 	print("The two Petri nets are not isomorphic.")



