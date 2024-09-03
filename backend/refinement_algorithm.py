import pm4py
from pm4py import PetriNet
from itertools import permutations
from typing import Dict
from Refiner import Refiner

from collections import deque
from itertools import combinations

def is_refinement_via_search(net_A: PetriNet, net_B: PetriNet) -> bool:
	"""
	This function attempts to determine if net_B can be refined to match net_A
	using the transformations defined in the Refiner class.
	"""
	# Queue for BFS, storing pairs (current_net, applied_operations)
	queue = deque([(net_B, [])])
	visited = set()  # To keep track of visited operations

	step_count = 0  # Counter to keep track of steps

	while queue:
		step_count += 1  # Increment step counter
		current_net, applied_operations = queue.popleft()

		# Print current step and applied operations
		print(f"\nStep {step_count}: Current applied operations: {applied_operations}")

		# Check if the current net is isomorphic to net_A
		if are_petri_nets_isomorphic(current_net, net_A):
			print("Refinement successful with operations:", applied_operations)
			return True

		# Generate possible transformations
		possible_transformations = []

		# Apply all possible place duplications
		for place in current_net.places:
			possible_transformations.append(('place_duplicater', place))

		# Apply all possible transition duplications
		for transition in current_net.transitions:
			possible_transformations.append(('transition_duplicator', transition))

		# Apply all possible local transition additions
		for place in current_net.places:
			possible_transformations.append(('local_transition_adder', place))

		# Apply all possible place splits
		for place in current_net.places:
			in_arc_combinations = get_in_arc_subsets(place)  # Function to generate subsets of in-arcs
			for subset in in_arc_combinations:
				possible_transformations.append(('place_splitter', place, subset))

		# Print the number of possible transformations
		print(f"Number of possible transformations: {len(possible_transformations)}")

		# Explore transformations
		for transformation in possible_transformations:
			# Create a deep copy of the net to apply transformation
			new_net = current_net.__deepcopy__()
			# pm4py.view_petri_net(new_net, )

			# Print which transformation is being applied
			# print(f"Applying transformation: {transformation}")

			# Apply transformation based on the type
			if transformation[0] == 'place_duplicater':
				Refiner.place_duplicater(new_net, transformation[1])
			elif transformation[0] == 'transition_duplicator':
				Refiner.transition_duplicator(new_net, transformation[1])
			elif transformation[0] == 'local_transition_adder':
				Refiner.local_transition_adder(new_net, transformation[1])
			elif transformation[0] == 'place_splitter':
				Refiner.place_splitter(new_net, transformation[1], transformation[2])

			# Generate a unique identifier for the new state based on the applied operations
			new_operations = applied_operations + [transformation]
			new_state_id = get_state_identifier(new_net, new_operations)

			# Print the state identifier of the new net
			# print(f"New state identifier: {new_state_id}")

			# Check if this state has been visited
			if new_state_id not in visited:
				# print(f"New state not visited. Adding to queue.")
				visited.add(new_state_id)
				queue.append((new_net, new_operations))
			# else:
			# 	print(f"State already visited: {new_state_id}")

	# print("No refinement found.")
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
	if len(net1.places) != len(net2.places):
		print("Different number of places:", len(net1.places), "vs", len(net2.places))
		return False
	if len(net1.transitions) != len(net2.transitions):
		print("Different number of transitions:", len(net1.transitions), "vs", len(net2.transitions))
		return False
	if len(net1.arcs) != len(net2.arcs):
		print("Different number of arcs:", len(net1.arcs), "vs", len(net2.arcs))
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
