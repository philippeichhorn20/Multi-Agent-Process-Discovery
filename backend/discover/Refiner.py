import pm4py
from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.petri_net.utils import petri_utils
from typing import Set

class Refiner:

	@staticmethod
	def place_duplicater(net: PetriNet, place: PetriNet.Place ):
		new_place = petri_utils.add_place(net)
		for in_arc in place.in_arcs:
			petri_utils.add_arc_from_to(in_arc.source, new_place, net)
		for out_arc in place.out_arcs:
			petri_utils.add_arc_from_to(new_place, out_arc.target, net)

	@staticmethod
	def transition_duplicator(net: PetriNet, transition: PetriNet.Transition):
		new_transition = petri_utils.add_transition(net)
		for in_arc in transition.in_arcs:
			petri_utils.add_arc_from_to(in_arc.source, new_transition, net)
		for out_arc in transition.out_arcs:
			petri_utils.add_arc_from_to(new_transition, out_arc.target, net)

	@staticmethod
	def local_transition_adder(net: PetriNet, place: PetriNet.Place):
		new_transition = petri_utils.add_transition(net)
		new_p1 = petri_utils.add_place(net)
		new_p2 = petri_utils.add_place(net)
		for in_arc in place.in_arcs:
			petri_utils.add_arc_from_to(in_arc.source, new_p1, net)
		for out_arc in place.out_arcs:
			petri_utils.add_arc_from_to(new_p2, out_arc.target, net)
		petri_utils.add_arc_from_to(new_p1, new_transition, net)
		petri_utils.add_arc_from_to(new_transition, new_p2, net)
		petri_utils.remove_place(net, place)

	@staticmethod
	def place_splitter(net: PetriNet, place: PetriNet.Place, in_arc_subset: Set):
		# arcs: the set of inarcs of the place that should be split-off the main branch
		print("superset?")
		print(place.in_arcs)
		print(in_arc_subset)
		print("superset?")

		if not place.in_arcs.issuperset(in_arc_subset):
			raise Exception("in_arc_subset are not a subset of the given places in_arcs")
			#return False


		new_place = petri_utils.add_place(net, place.name)
		for arc in in_arc_subset.copy():
			petri_utils.add_arc_from_to(arc.source, new_place, net)
			#net.arcs.remove(arc) # didnt work so i substitiuted the function from the utils class (petri_utils.remover_arc())
			arc.source.out_arcs.remove(arc)
			arc.target.in_arcs.remove(arc)
		for t in petri_utils.post_set(place).copy():
			new_transition = petri_utils.add_transition(net,t.name)
			petri_utils.add_arc_from_to(new_place, new_transition, net)
			for t_post_places in petri_utils.post_set(t):
				petri_utils.add_arc_from_to(new_transition, t_post_places, net)





	@staticmethod
	def create_simple_petri_net():
		# Create a Petri net
		net_pn = PetriNet("Simple Petri Net")

		# Add places to the Petri net
		place1 = petri_utils.add_place(net_pn, 'place1')
		place2 = petri_utils.add_place(net_pn, 'place2')
		place3 = petri_utils.add_place(net_pn, 'place3')

		# Add transitions to the Petri net
		transition1 = petri_utils.add_transition(net_pn, 'transition1')
		transition2 = petri_utils.add_transition(net_pn, 'transition2')

		# Create arcs
		petri_utils.add_arc_from_to(place1, transition1, net_pn)
		petri_utils.add_arc_from_to(transition1, place2, net_pn)
		petri_utils.add_arc_from_to(place2, transition2, net_pn)
		petri_utils.add_arc_from_to(transition2, place3, net_pn)

		# Define the initial and final marking
		initial_marking = pm4py.objects.petri_net.obj.Marking()
		initial_marking[place1] = 1  # Initial token in place1

		final_marking = pm4py.objects.petri_net.obj.Marking()
		final_marking[place3] = 1  # Final token in place3


		return net_pn, place2, transition1, transition2

	@staticmethod
	def create_simple_petri_net2():
		# Create a Petri net
		net_pn = PetriNet("Simple Petri Net")

		# Add places to the Petri net
		place_p = petri_utils.add_place(net_pn, 'p')
		place_final = petri_utils.add_place(net_pn, 'final')

		# Add transitions to the Petri net
		transition_t1 = petri_utils.add_transition(net_pn, 't1')
		transition_t2 = petri_utils.add_transition(net_pn, 't2')
		transition_t3 = petri_utils.add_transition(net_pn, 't3')

		# Create arcs according to the image
		petri_utils.add_arc_from_to(transition_t1, place_p, net_pn)
		petri_utils.add_arc_from_to(transition_t2, place_p, net_pn)
		petri_utils.add_arc_from_to(place_p, transition_t3, net_pn)
		petri_utils.add_arc_from_to(transition_t3, place_final, net_pn)

		# Define the initial and final marking
		initial_marking = pm4py.objects.petri_net.obj.Marking()
		initial_marking[place_p] = 0  # No initial tokens in place p

		final_marking = pm4py.objects.petri_net.obj.Marking()
		# Assuming one token in place 'p' marks the final state
		final_marking[place_p] = 1

		return net_pn, place_p, transition_t1, transition_t2, transition_t3




	net, p, t1,t2,t3  = create_simple_petri_net2()
	pm4py.view_petri_net(net)
	place_splitter(net=net, place=p, in_arc_subset=t1.out_arcs.copy())
	pm4py.view_petri_net(net)


