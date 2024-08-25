# This  class finds transitions that are representing interactions with other agents
#
# Two types of interactions:
# Async: "a!" (message sent), "a?" (message received")
from pm4py.objects.petri_net.utils import petri_utils

import pm4py.objects.petri_net.utils as pnutils
from pm4py.objects.petri_net.obj import PetriNet


class InteractionUtils:

	@staticmethod
	def connect_async_interactions(net: PetriNet):
		for trans in net.transitions:
			if trans.name and '!' in trans.name:
				trans.properties.update({"sync": '!'})
				search = trans.name.replace('!', '?')
				for trans2 in net.transitions:
					trans2.properties.update({"sync": '?'})
					if trans.label == search:
						new_place = pnutils.petri_utils.add_place(net, "async", )
						new_place.properties.update({"sync":True})
						pnutils.petri_utils.add_arc_from_to(trans, new_place,net)
						pnutils.petri_utils.add_arc_from_to(new_place, trans2, net)

	@staticmethod
	def connect_sync_interactions(net:PetriNet):
		for trans in net.transitions.copy():
			for trans2 in net.transitions.copy():
				if net.transitions.__contains__(trans2):
					if trans.name == trans2.name:
						for arc in trans2.in_arcs.copy():
							petri_utils.add_arc_from_to(arc.source, trans, net)
						for arc in trans2.out_arcs.copy():
							petri_utils.add_arc_from_to(trans, arc.target , net)
						trans.properties.update({"sync":"s"})
						petri_utils.remove_transition(net, trans2)


	@staticmethod
	def merge_two_nets(a, b):
		merged_net = pnutils.petri_utils.merge(nets=[a, b])
		InteractionUtils.connect_async_interactions(merged_net)
		#InteractionUtils.connect_sync_interactions(merged_net)
		return merged_net
