# This  class finds transitions that are representing interactions with other agents
#
# Two types of interactions:
# Async: "a!" (message sent), "a?" (message received")

from pm4py.objects.petri_net.utils import petri_utils
import pm4py
import pm4py.objects.petri_net.utils as pnutils
from pm4py.objects.petri_net.obj import PetriNet, Marking
from itertools import chain
import re

class InteractionUtils:

	@staticmethod
	def connect_async_interactions(net: PetriNet):
		for trans in net.transitions:
			if trans.label and '!' in trans.label:
				trans.properties.update({"resource": '!'})
				for trans2 in net.transitions:
					if trans.label and trans2.label and "__" in trans.label and "__" in trans2.label:
						matches = InteractionUtils.match_messages(trans.label,trans2.label)
						if matches and len(matches)>0:
							for match in matches:
								trans2.properties.update({"resource": '?'})
								new_place = None
								for place in net.places:
									if place.name == match:
										new_place = place
								if not new_place:
									new_place = pnutils.petri_utils.add_place(net, match,)
								new_place.properties.update({"resource":"X"})
								if(new_place not in pnutils.petri_utils.post_set(trans)):
									pnutils.petri_utils.add_arc_from_to(trans, new_place,net)
								if(new_place not in pnutils.petri_utils.pre_set(trans2)):
									pnutils.petri_utils.add_arc_from_to(new_place, trans2, net)

					elif (trans2.label and trans.label and trans2.label.split("_")[0] == trans.label.replace('!', '?').split("_")[0]):
						trans2.properties.update({"resource": '?'})
						trans2.properties.update({"resource": '?'})
						new_place = None
						for place in net.places:
							if place.name == trans.label.split("!")[0]:
								new_place = place
						if not new_place:
							new_place = pnutils.petri_utils.add_place(net, trans.label.split("!")[0],)
						new_place.properties.update({"resource":"X"})
						if(new_place not in pnutils.petri_utils.post_set(trans)):
							pnutils.petri_utils.add_arc_from_to(trans, new_place,net)
						if(new_place not in pnutils.petri_utils.pre_set(trans2)):
							pnutils.petri_utils.add_arc_from_to(new_place, trans2, net)

	@staticmethod
	def connect_sync_interactions(net:PetriNet):
		for trans in net.transitions.copy():
			for trans2 in net.transitions.copy():
				if net.transitions.__contains__(trans2) and net.transitions.__contains__(trans):
					if trans2.label and trans.label and trans.label.split("_")[0] == trans2.label.split("_")[0] and trans != trans2 and trans2.label.split("_")[0]=="s":
						print("trans", trans, trans2)
						
						for arc in trans2.in_arcs.copy():
							if not arc.source in petri_utils.pre_set(trans):
								petri_utils.add_arc_from_to(arc.source, trans, net)
						for arc in trans2.out_arcs.copy():
							if not trans in petri_utils.pre_set(arc.target):
								petri_utils.add_arc_from_to(trans, arc.target , net)
						trans.properties['resource'] = "sync"
						petri_utils.remove_transition(net, trans2)
	@staticmethod
	def merge_markings(markings):
		if not markings:
			return Marking() 
		merged_marking = markings[0]  
		for marking in markings[1:]:
			merged_marking += marking  
		return merged_marking

	@staticmethod
	def merge_two_nets(nets):

		merged_net = pnutils.petri_utils.merge(nets=[net[0] for net in nets])
		im = InteractionUtils.merge_markings([net[1] for net in nets])
		fm = InteractionUtils.merge_markings([net[2] for net in nets])
		InteractionUtils.connect_async_interactions(merged_net)
		InteractionUtils.connect_sync_interactions(merged_net)
		print("connecting done")
		return merged_net, im, fm




	@staticmethod
	def encode_name(place_or_transition):
		if not place_or_transition:
			return ""
		string = ""
		if "resource" in place_or_transition.properties and place_or_transition.properties["resource"]:
			string += place_or_transition.properties["resource"]
		else:
			string += "undefined"
		string += ":"
		if isinstance(place_or_transition, PetriNet.Place) and place_or_transition.name:
			string += place_or_transition.name
		else:
			string += (place_or_transition.label if place_or_transition.label != None else (place_or_transition.name if place_or_transition.name else ""))
		return string
	@staticmethod
	def encode_names_for_transfer(net: PetriNet):
		for x in net.places:
			x.name = InteractionUtils.encode_name(x)

		for x in net.transitions:
			x.name = InteractionUtils.encode_name(x)
			x.label = InteractionUtils.encode_name(x)

	@staticmethod
	def extract_messages(trans_label):		
	
		trans_label = trans_label.split("__")[1]
		if(trans_label ==""):
			return set(),set()
		if("!" in trans_label):
			sent_part, received_part = trans_label.split('!')
		else:
			received_part = trans_label
			sent_part = ""
		if("?" in received_part):
			received_part = received_part.split('?')[0]
				
		# Split the sent and received parts into individual messages
		sent_messages = set(re.findall(r'\w+\d*', sent_part))  # Match words (alphanumeric strings) followed by numbers
		received_messages = set(re.findall(r'\w+\d*', received_part))
		
		return sent_messages, received_messages

	@staticmethod
	def match_messages(trans1_label, trans2_label):
		sent1, received1 = InteractionUtils.extract_messages(trans1_label)
	
		sent2, received2 = InteractionUtils.extract_messages(trans2_label)

		# Find matches: sent in one and received in the other
		matched_messages = (sent1 & received2)
		
		return matched_messages

