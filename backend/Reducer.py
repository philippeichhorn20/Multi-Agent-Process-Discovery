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
	def string_match(str1: str, str2: str): # if it is a interaction model, it has to be of same interaction object (a!_2==a!_2 but )
		if not isinstance(str1, str) or not isinstance(str2, str):
			return False
		if '!' not in str1 and '?' not in str1:
			return True
		min_len = min(len(str1), len(str2))
		for i in range(min_len):
			if str1[i] != str2[i] or str1[i] == '_':
				return i == 0 or str1[i] == '_'
		return True
	


	@staticmethod
	def apply(net: PetriNet):
		pnet = net
		count = 0
		changes = []  # List to track changes

		while count < 15:
			# print("count: ", count)
			count += 1
			pm4py.view_petri_net(pnet)
			for place in pnet.places.copy():
				if True or not 'resource' in place.properties or place.properties['resource'] not in ['!', '?', 'sync', True]: # disbaled with True
					if Reducer.remove_place(pnet, place):
						changes.append(('add_place', place))
						print("Place removed")
						pm4py.view_petri_net(pnet)
					if Reducer.preset_disjoint_simplification(pnet, place):
						changes.append(('split_place', place))
						print("Place pds")
						pm4py.view_petri_net(pnet)
			for transition in pnet.transitions.copy():
				if True or not 'resource' in transition.properties or transition.properties['resource'] not in ['!', '?', 'sync', True]: # disabled with True
					if Reducer.remove_transition(pnet, transition):
						changes.append(('add_transition', transition))
						print("Transition removed")
						pm4py.view_petri_net(pnet)
			for transition in pnet.transitions.copy():
				if not 'resource' in transition.properties or transition.properties['resource'] not in ['!', '?', 'sync', True]:
					if Reducer.remove_local_transition(pnet, transition):
						None
						#changes.append(('add_local_transition', transition))
						print("Local transition removed")
						pm4py.view_petri_net(pnet)

		return pnet  

	@staticmethod
	def remove_local_transition(net, transition): # Local transition elimination
		if len(transition.in_arcs) == 1 and len(transition.out_arcs) == 1:
			place_before_transition = list(transition.in_arcs)[0].source
			place_after_transition = list(transition.out_arcs)[0].target  #gets pointed from first_transition
			# changes.append(('add_local_transition', (transition, place_before_transition, place_after_transition) ))
			if(
				len(petri_utils.post_set(place_before_transition) )== 1
				and 
				len(petri_utils.pre_set(place_after_transition) )== 1
				and 
				petri_utils.pre_set(place_after_transition) == {transition}
				and
				petri_utils.post_set(place_before_transition) == {transition}
				and 
				(
					len(petri_utils.pre_set(place_before_transition))>0
					or
					len(petri_utils.post_set(place_after_transition))>0
				)
				and
				len(petri_utils.pre_set(place_before_transition).intersection(
					petri_utils.post_set(place_after_transition)
				))==0
			):
				for t in petri_utils.pre_set(place_before_transition):
					petri_utils.add_arc_from_to(t,place_after_transition, net) 
				# print(transition.label)
				petri_utils.remove_transition(net, transition)
				petri_utils.remove_place(net, place_before_transition)
				return True

			# if len(place_before_transition.out_arcs) == 1: # removing place_before_transition + transition
			# 	for t in petri_utils.pre_set(place_before_transition):
			# 		petri_utils.add_arc_from_to(t,place_after_transition, net) 
			# 	# print(transition.label)
			# 	petri_utils.remove_transition(net, transition)
			# 	petri_utils.remove_place(net, place_before_transition)
			# 	return True
			# elif len(place_after_transition.in_arcs) == 1: # removing place_before_transition + transition
			# 	for t in petri_utils.post_set(place_after_transition):
			# 		petri_utils.add_arc_from_to(place_before_transition,t , net)
			# 	# print(transition.label)
			# 	petri_utils.remove_transition(net, transition)
			# 	petri_utils.remove_place(net, place_after_transition)
			# 	return True
		return False

	@staticmethod
	def remove_transition(net, transition: PetriNet.Transition): # transition simplififcation
		#check if current transition has one in on out arc (might not be sufficient todo check)
		# find a t1
		for other_trans in net.transitions:
			if(
				transition != other_trans
				and 
				Reducer.string_match(transition.label, other_trans.label)
				and
				petri_utils.pre_set(transition) == petri_utils.pre_set(other_trans)
				and 
				petri_utils.post_set(transition) == petri_utils.post_set(other_trans)
			
			):
			# print(transition.label, other_trans.label)
			# if(Reducer.string_match(transition.label, other_trans.label) and other_trans != transition and petri_utils.pre_set(transition)== petri_utils.pre_set(other_trans)
			# 	and petri_utils.post_set(transition)==petri_utils.post_set(other_trans)):
				petri_utils.remove_transition(net, transition)
				# print("removing transition: ", transition.label, other_trans.label)
				return True
		return False

	@staticmethod
	def remove_place(net, place): # place siplification 
		for other_place in net.places:
			if(
				petri_utils.pre_set(place) == petri_utils.pre_set(other_place)
				and
				petri_utils.post_set(place) == petri_utils.post_set(other_place)
				and 
				place != other_place
				):
			# if (set(arc.source for arc in other_place.in_arcs) == set(
			# 	arc.source for arc in place.in_arcs) and set(
			# 	arc.target for arc in other_place.out_arcs) == set(
			# 	arc.target for arc in place.out_arcs) and place != other_place):
				petri_utils.remove_place(net, place)
				# print("remove place: ",
				#       [in_arcs.source.label for in_arcs in place.in_arcs],
				#       [out_arcs.target.label for out_arcs in place.out_arcs])
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

			
				print("Length of place.out_arcs:", len(place.out_arcs))
				print("Length of other_place.out_arcs:", len(other_place.out_arcs))
				print("Are place and other_place different?", place != other_place)
				intersection = set(arc.source for arc in other_place.in_arcs).intersection(set(arc.source for arc in place.in_arcs))
				print("Intersection of in_arcs sources:", intersection)
				print("Length of intersection:", len(intersection))
				set_of_places_to_t3_1 = set()
				set_of_places_to_t3_2 = set()
				for x in set(arc.target for arc in place.out_arcs):
					set_of_places_to_t3_1 = set_of_places_to_t3_1.union(
						set(arc.source for arc in x.in_arcs))
				for x in set(arc.target for arc in other_place.out_arcs):
					set_of_places_to_t3_1 = set_of_places_to_t3_1.union(
						set(arc.source for arc in x.in_arcs))

				if set_of_places_to_t3_1 == set_of_places_to_t3_2:  # Compare sets directly
					# print("places are different:", petri_utils.pre_set(place),petri_utils.pre_set(other_place))
					for in_arcs in place.in_arcs:
						petri_utils.add_arc_from_to(in_arcs.source, other_place, net)
					petri_utils.remove_place(net, place)
					print("merging place")
					# print("merging place: ",
					#       [in_arcs.source.label for in_arcs in place.in_arcs],
					#       [out_arcs.target.label for out_arcs in
					#        place.out_arcs], place, other_place)
					return True
		return False


	def preset_disjoint_simplification(net: PetriNet, transition: PetriNet.Transition):
		for other_trans in net.transitions:
			if(
				other_trans != transition
				and 
				len(petri_utils.pre_set(transition).intersection(petri_utils.pre_set(other_trans))) == 0
				and 
				len(petri_utils.pre_set(transition)) == len(petri_utils.pre_set(other_trans))
				and 
				petri_utils.post_set(transition) == petri_utils.post_set(other_trans)
			):
				t12 = petri_utils.add_transition(net, transition.label)  # Assuming label is the same
				# Set properties for t12
				t12.in_arcs = transition.in_arcs + other_trans.in_arcs
				t12.out_arcs = transition.out_arcs + other_trans.out_arcs
				
				# Update arcs based on the bijection g
				for a in transition.in_arcs:
					for b in other_trans.in_arcs:
						if a != b:  # Ensure a and b are distinct
							# Add arc from a to b
							petri_utils.add_arc_from_to(a.source, b.target, net)
				# Remove old transitions
				petri_utils.remove_transition(net, transition)
				petri_utils.remove_transition(net, other_trans)
				return t12
				

