import pm4py
from pm4py.objects.petri_net.obj import PetriNet, Marking
from pm4py.objects.petri_net.utils import petri_utils

class Reducer:
	"""
    Refinement Operations:

    1. Place Duplication ->  should be place addition I think. > Thus implemented like so
    2. Transition Duplication
    3. Local Transition introduction
    4. Place Split

    5. No change, move ahead

    We define a reverse refiner, a reducer, which contains the following methods:
    1. Place Removal -> removes a place if it connects two transitions that are not inter-agent-communicating
    """


	@staticmethod
	def apply_all(nets):
		abstracted_nets = []
		for net in nets:
			net, im, fm = net
			net = net.__deepcopy__()
			abstracted_net = Reducer.apply(net)
			abstracted_nets.append((abstracted_net, Marking(), Marking()))
		return abstracted_nets

	@staticmethod
	def apply(net: PetriNet, print_enabled=False):
		pnet = net
		count = 0
		changes = []  # List to track changes

		while count < 15:
			if print_enabled: print("count: ", count)
			count += 1
			if print_enabled: pm4py.view_petri_net(pnet)
			for transition in pnet.transitions.copy():
				if True or not 'resource' in transition.properties or transition.properties['resource'] not in ['!', '?', 'sync', True]: # disabled with True
					if Reducer.preset_disjoint_simplification(pnet, transition):
						changes.append(('split_place', transition))
						if(print_enabled):
							print("trans pds")
							pm4py.view_petri_net(pnet)
			for transition in pnet.transitions.copy():
				if True or not 'resource' in transition.properties or transition.properties['resource'] not in ['!', '?', 'sync', True]: # disabled with True
					if Reducer.remove_transition(pnet, transition):
						changes.append(('add_transition', transition))
						if(print_enabled):
							print("Transition removed")
							pm4py.view_petri_net(pnet)
			for place in pnet.places.copy():
				if True or not 'resource' in place.properties or place.properties['resource'] not in ['!', '?', 'sync', True]: # disbaled with True
					if Reducer.remove_place(pnet, place):
						changes.append(('add_place', place))
						if(print_enabled):
							print("Place removed")
							pm4py.view_petri_net(pnet)
			for transition in pnet.transitions.copy():
				if not transition.label or ('!' not in transition.label and not '?' in transition.label and not 's' in transition.label):
				#if not 'resource' in transition.properties or transition.properties['resource'] not in ['!', '?', 'sync', True]:
					if Reducer.remove_local_transition(pnet, transition):
						None
						#changes.append(('add_local_transition', transition))
						if(print_enabled):
							print("Local transition removed")
							pm4py.view_petri_net(pnet)


		return pnet  

	@staticmethod
	def remove_local_transition(net, transition, my_way = True): # Local transition elimination
		""""
		This function removes a transition that is has one in arc and one out arc by mergin the place before and after into one.
		According to the paper the place before must not have other outarcs and the place after not any other in arcs. 
		In the my_way version, this rule is disregarded in order to achieve the level of abstraction in the examples.
		"""
		if len(transition.in_arcs) == 1 and len(transition.out_arcs) == 1:
			place_before_transition = list(transition.in_arcs)[0].source
			place_after_transition = list(transition.out_arcs)[0].target  #gets pointed from first_transition
			# changes.append(('add_local_transition', (transition, place_before_transition, place_after_transition) ))
			if(
				# start: extra condition
				(
					my_way or (				
				len(petri_utils.post_set(place_before_transition) )== 1
				and 
				len(petri_utils.pre_set(place_after_transition) )== 1
				and 
				petri_utils.pre_set(place_after_transition) == {transition}
				and
				petri_utils.post_set(place_before_transition) == {transition}
				))
				# end: extra condition
				and
				(len(place_before_transition.out_arcs) == 1)
				or 
				(len(place_after_transition.in_arcs) == 1)
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
				# for t in petri_utils.pre_set(place_before_transition):
				# 	petri_utils.add_arc_from_to(t,place_after_transition, net) 
				# print(transition.label)
				# petri_utils.remove_transition(net, transition)
				# petri_utils.remove_place(net, place_before_transition)
				# return True

				if len(place_before_transition.out_arcs) == 1: # removing place_before_transition + transition
					for t in petri_utils.pre_set(place_before_transition):
						petri_utils.add_arc_from_to(t,place_after_transition, net) 
					# print(transition.label)
					petri_utils.remove_transition(net, transition)
					petri_utils.remove_place(net, place_before_transition)
					return True
				elif len(place_after_transition.in_arcs) == 1: # removing place_before_transition + transition
					for t in petri_utils.post_set(place_after_transition):
						petri_utils.add_arc_from_to(place_before_transition,t , net)
					# print(transition.label)
					petri_utils.remove_transition(net, transition)
					petri_utils.remove_place(net, place_after_transition)
					return True
		return False

	@staticmethod
	def remove_transition(net, transition: PetriNet.Transition, my_way = True): # transition simplififcation
		"""
		The remove_transition method, (a.k.a transition simplifactaion) merges transitions that have the same pre- and postset.
		In theory (in both papaer), the two transitions have to have the same label (h(t)). However in the examples, this appears not to be applied as strictly.
		See reduction_utils.string_match for more details.
		"""
		for other_trans in net.transitions:
			if(
				transition != other_trans
				and 
			(my_way or transition.label == other_trans.label or(transition.label and other_trans.label and transition.label.split("_")[0] == other_trans.label.split("_")[0])) # same labels "h(t1) = h(t2)", perfect match (a_1 == a_2)
				and
				(reduction_utils.string_match(other_trans.label, transition.label) or transition.label == None) # l
				and
				petri_utils.pre_set(transition) == petri_utils.pre_set(other_trans)
				and 
				petri_utils.post_set(transition) == petri_utils.post_set(other_trans)
			
			):
			# print(transition.label, other_trans.label)
			# if(reduction_utils.string_match(transition.label, other_trans.label) and other_trans != transition and petri_utils.pre_set(transition)== petri_utils.pre_set(other_trans)
			# 	and petri_utils.post_set(transition)==petri_utils.post_set(other_trans)):
				petri_utils.remove_transition(net, transition)
				# print("removing transition: ", transition.label, other_trans.label)
				return True
		return False

	@staticmethod
	def remove_place(net, place, my_way = True): # place siplification 
		# no difference between my_way and the paper
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

	# @staticmethod
	# def place_merge(net, place):
	# 	for other_place in net.places:
	# 		#4th no shared transitions before = the sets of transitions prior to p1 and p2 are two disjoint sets

	# 		if (len(place.out_arcs) > 0 and len(other_place.out_arcs) > 0 and other_place != place and len((set(
	# 			arc.source for arc in other_place.in_arcs)).intersection(
	# 			set(arc.source for arc in place.in_arcs))) == 0):
	# 			#6TH:
	# 			print("Length of place.out_arcs:", len(place.out_arcs))
	# 			print("Length of other_place.out_arcs:", len(other_place.out_arcs))
	# 			print("Are place and other_place different?", place != other_place)
	# 			intersection = set(arc.source for arc in other_place.in_arcs).intersection(set(arc.source for arc in place.in_arcs))
	# 			print("Intersection of in_arcs sources:", intersection)
	# 			print("Length of intersection:", len(intersection))
	# 			set_of_places_to_t3_1 = set()
	# 			set_of_places_to_t3_2 = set()
	# 			for x in set(arc.target for arc in place.out_arcs):
	# 				set_of_places_to_t3_1 = set_of_places_to_t3_1.union(
	# 					set(arc.source for arc in x.in_arcs))
	# 			for x in set(arc.target for arc in other_place.out_arcs):
	# 				set_of_places_to_t3_1 = set_of_places_to_t3_1.union(
	# 					set(arc.source for arc in x.in_arcs))

	# 			if set_of_places_to_t3_1 == set_of_places_to_t3_2:  # Compare sets directly
	# 				# print("places are different:", petri_utils.pre_set(place),petri_utils.pre_set(other_place))
	# 				for in_arcs in place.in_arcs:
	# 					petri_utils.add_arc_from_to(in_arcs.source, other_place, net)
	# 				petri_utils.remove_place(net, place)
	# 				print("merging place")
	# 				# print("merging place: ",
	# 				#       [in_arcs.source.label for in_arcs in place.in_arcs],
	# 				#       [out_arcs.target.label for out_arcs in
	# 				#        place.out_arcs], place, other_place)
	# 				return True
	# 	return False


	def postset_empty_place_simplifications(net: PetriNet, place: PetriNet.Place, my_way = True):
		for other_place in net.places.copy():
			if (
				len(petri_utils.post_set(place)) == 0
				and
				len(petri_utils.post_set(place)) == 0
			):
				None
				
	def preset_disjoint_simplification(net: PetriNet, transition: PetriNet.Transition, my_way = True):
		for other_trans in net.transitions:
			if(
				other_trans != transition
				and 
				len(petri_utils.pre_set(transition).intersection(petri_utils.pre_set(other_trans))) == 0
				and 
				len(petri_utils.pre_set(transition)) == len(petri_utils.pre_set(other_trans))
				and 
				petri_utils.post_set(transition) == petri_utils.post_set(other_trans)
				and reduction_utils.string_match(transition.label, other_trans.label)
				and reduction_utils.preset_state_machine_check(transition, other_trans, net)
			):
				print("Checking conditions for transition:", transition.label, "and other_trans:", other_trans.label)
				preset = petri_utils.pre_set(transition)
				other_preset = petri_utils.pre_set(other_trans)

				if len(list(preset)[0].out_arcs)>1 or len(list(other_preset)[0].out_arcs)>1:
					# not specified in paper, but i think it maybe should have been
					print("unfofficial rule in action")
					return False
				
			
				# TODO sequential component???
				for p, other_p in  zip(preset, other_preset.copy()):
					for arc in other_p.in_arcs.copy():
						petri_utils.add_arc_from_to(arc.source, p, net)
					petri_utils.remove_place(net, other_p)
					
				# for in_arcs in other_trans.in_arcs:
				# 	petri_utils.add_arc_from_to(in_arcs.source, transition, net)
				if other_trans.label and '!' in other_trans.label or '?'  in other_trans.label or 's' in other_trans.label:
					transition.label = other_trans.label
				petri_utils.remove_transition(net, other_trans)
				
				return True
		return False
				

class reduction_utils:
	@staticmethod
	def preset_state_machine_check(t1: PetriNet.Transition, t2: PetriNet.Transition, net: PetriNet):
		'''for A5: Preset-disjoint transition simplification we need a check
		 if the presets of the transitions form a sequential component. 
		 This includes, checking, if it the preset-places of t1 and t2: P  build a connected net using •P• and P
		 
		 The resulting net build from •P• and P needs to fulfill the following:
		*	- be a state machine 
		*		- therefore be a connected net
		*		- therefore ∀t ∈ T : |•t| = |t•| = 1
			- has single token in initial marking (TODO)
		-- only conditions with * are implemented so far -- 
		 '''
		# connectedness of graph:
		t1_preset = petri_utils.pre_set(t1)
		t2_preset = petri_utils.pre_set(t2)

		connected_trans_t1 = set()
		for p in t1_preset:
			connected_trans_t1.update(petri_utils.pre_set(p))	

		connected_trans_t2 = set()
		for p in t2_preset:
			connected_trans_t2.update(petri_utils.pre_set(p))
		connected_trans_t1.add(t1)
		connected_trans_t2.add(t2)
		
		# checking  ∀t ∈ T : |•t| = |t•| = 1
		for trans in connected_trans_t1.union(connected_trans_t2):
			if len(trans.in_arcs) != 1 or len(trans.out_arcs) != 1:
				return False
		return True
		# checking connectedness
		for trans in connected_trans_t1:
			if any(p in t2_preset for p in petri_utils.pre_set(trans)) or any(p in t2_preset for p in petri_utils.post_set(trans)):
				print("connectedness proven")
				return True
		for trans in connected_trans_t2:
			if any(p in t1_preset for p in petri_utils.pre_set(trans)) or any(p in t1_preset for p in petri_utils.post_set(trans)):
				print("connectedness proven")
				return True

		
		return False



	@staticmethod
	def string_match(str1: str, str2: str): # if it is a interaction model, it has to be of same interaction object (a!_2==a!_2 but )
		"""
		advanced matching to ensure:
		 - transitions can be merged, as long as no interaction gets lost


		"""
		str1_is_interact = isinstance(str1, str) and ('!' in str1 or '?'  in str1 or 's' == str1.split("_"))
		str2_is_interact = isinstance(str2, str) and ('!' in str2 or '?'  in str2 or 's' == str2.split("_"))
		if(not str1_is_interact and not str2_is_interact): # neither are interactive -> can merge
			return True
		if(str1_is_interact and not str2_is_interact): # one is interactive, one not -> cannot merge
			return False
		if(not str1_is_interact and str2_is_interact):
			return False
		str1 = str1.split('_')[0]
		str2 = str2.split('_')[0]

		return str1 == str2 # both are interactive -> merge, if they have the same label
	
		# min_len = min(len(str1), len(str2)) 
		# for i in range(min_len): # both are interactive -> merge if label matches
		# 	if str1[i] != str2[i] or str1[i] == '_':
		# 		return i == 0 or str1[i] == '_'
		# print(str1, str2, "deuwgh")
		# return False
	
