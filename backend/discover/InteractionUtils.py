# This  class finds transitions that are representing interactions with other agents
#
# Two types of interactions:
# Async: "a!" (message sent), "a?" (message received")

import Transition
import pm4py.objects.petri_net.utils as pnutils
from pm4py.objects.petri_net.obj import PetriNet


class InteractionUtils:

    @staticmethod
    def connect_async_interactions(net: PetriNet):
        pnet, start, end = net
        for trans in net.transitions:
            if trans.label.__contains__('!'):
                search = trans.label.replace('!', '?')
                for trans2 in net.transitions:
                    if trans.label == search:
                        new_place = pnutils.petri_utils.add_place(net, "async")
                        pnutils.petri_utils.add_arc_from_to(trans, new_place,
                                                            net)
                        pnutils.petri_utils.add_arc_from_to(new_place, trans2,
                                                            net)

    @staticmethod
    def merge_two_nets(a, b):
        merged_net = pnutils.petri_utils.merge(a, b)
        InteractionUtils.connect_async_interactions(merged_net)
