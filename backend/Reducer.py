import pm4py
from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.petri_net.utils import petri_utils


class Reducer:

	"""
    Refinement Operations:

    1. Place Duplication -> Bullshit, should be place addition I think. > Thus implemented like so
    2. Transition Duplication
    3. Local Transition introduction
    4. Place Split

    5. No change, move ahead

    We define a reverse refiner, a reducer, which contains the following methods:
    1. Place Removal -> removes a place if it connects two transitions that are not inter-agent-communicating
    """

	@staticmethod
	def apply(net: PetriNet):
		pnet = net
		count = 0
		changes = []  # List to track changes

		while count < 15:
			print("count: ", count)
			count += 1
			pm4py.view_petri_net(pnet)
			for place in pnet.places.copy():
				if not 'resource' in place.properties or place.properties['resource'] not in ['!', '?', 'sync', True]:
					if Reducer.remove_place(pnet, place):
						changes.append(('add_place', place))
						print("Place removed")
					if Reducer.place_merge(pnet, place):
						changes.append(('split_place', place))
						print("Place merged")
			for transition in pnet.transitions.copy():
				if not 'resource' in transition.properties or transition.properties['resource'] not in ['!', '?', 'sync', True]:
					if Reducer.remove_transition(pnet, transition):
						changes.append(('add_transition', transition))
						print("Transition removed")
			for transition in pnet.transitions.copy():
				if not 'resource' in transition.properties or transition.properties['resource'] not in ['!', '?', 'sync', True]:
					if Reducer.remove_local_transition(pnet, transition):
						changes.append(('add_local_transition', transition))
						print("Local transition removed")
			

		return pnet, changes  

	@staticmethod
	def remove_local_transition(net, transition):
		if len(transition.in_arcs) == 1 and len(transition.out_arcs) == 1:
			place_before_transition = list(transition.in_arcs)[0].source
			place_after_transition = list(transition.out_arcs)[0].target  #gets pointed from first_transition
			if len(place_before_transition.out_arcs) == 1: # removing place_before_transition + transition
				for t in petri_utils.pre_set(place_before_transition):
					petri_utils.add_arc_from_to(t,place_after_transition, net)
				print(transition.label)
				petri_utils.remove_transition(net, transition)
				petri_utils.remove_place(net, place_before_transition)
				return True
			elif len(place_after_transition.in_arcs) == 1: # removing place_before_transition + transition
				for t in petri_utils.post_set(place_after_transition):
					petri_utils.add_arc_from_to(place_before_transition,t , net)
				print(transition.label)
				petri_utils.remove_transition(net, transition)
				petri_utils.remove_place(net, place_after_transition)
				return True
		return False

	@staticmethod
	def remove_transition(net, transition):
		#check if current transition has one in on out arc (might not be sufficient todo check)
		# find a t1
		for other_trans in net.transitions:
			if(other_trans != transition and petri_utils.pre_set(transition)== petri_utils.pre_set(other_trans)
				and petri_utils.post_set(transition)==petri_utils.post_set(other_trans)):
				petri_utils.remove_transition(net, transition)
				print("removing transition: ", transition.label, other_trans.label)
				return True
		return False

	@staticmethod
	def remove_place(net, place):
		for other_place in net.places:
			if (set(arc.source for arc in other_place.in_arcs) == set(
				arc.source for arc in place.in_arcs) and set(
				arc.target for arc in other_place.out_arcs) == set(
				arc.target for arc in place.out_arcs) and place != other_place):
				petri_utils.remove_place(net, place)
				print("remove place: ",
				      [in_arcs.source.label for in_arcs in place.in_arcs],
				      [out_arcs.target.label for out_arcs in place.out_arcs])
				return True
		return False

	@staticmethod
	def place_merge(net, place):
		for other_place in net.places:
			#4th no shared transitions before = the sets of transitions prior to p1 and p2 are two disjoint sets
			if (len(place.out_arcs) > 0 and len(other_place.out_arcs) > 0 and other_place != place and len((set(
				arc.source for arc in other_place.in_arcs)).intersection(
				set(arc.source for arc in place.in_arcs))) == 0):
				#6TH:
				set_of_places_to_t3_1 = set()
				set_of_places_to_t3_2 = set()
				for x in set(arc.target for arc in place.out_arcs):
					set_of_places_to_t3_1 = set_of_places_to_t3_1.union(
						set(arc.source for arc in x.in_arcs))
				for x in set(arc.target for arc in other_place.out_arcs):
					set_of_places_to_t3_1 = set_of_places_to_t3_1.union(
						set(arc.source for arc in x.in_arcs))

				if set_of_places_to_t3_1 == set_of_places_to_t3_2:  # Compare sets directly
					print("places are different:", petri_utils.pre_set(place),petri_utils.pre_set(other_place))
					for in_arcs in place.in_arcs:
						petri_utils.add_arc_from_to(in_arcs.source, other_place, net)
					petri_utils.remove_place(net, place)
					print("merging place: ",
					      [in_arcs.source.label for in_arcs in place.in_arcs],
					      [out_arcs.target.label for out_arcs in
					       place.out_arcs], place, other_place)
					return True
		return False
