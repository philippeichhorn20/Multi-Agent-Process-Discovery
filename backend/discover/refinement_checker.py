import pm4py
from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.petri_net.utils import petri_utils


class Refinement_Checker:
    
    """
    Refinement Operations:

    1. Place Duplication -> Bullshit, should be place addition i think. > Thus implemented like so
    2. Transition Duplication
    3. Local Transition introduction
    4. Place Split

    5. No change, move ahead

    We define a reverse refiner, a reducer, which contains the following methods:
    1. Place Removal -> removes a place if it connects two transitions that are not inter-agent-communicating
    """


class Reducer:

    @staticmethod
    def apply(net):
        pnet, start, end = net
        for place in pnet.places:
            if Reducer.remove_place(pnet, place):
                print("Place removed")
     #   for transition in pnet.transitions:
         #   if Reducer.remove_transition(pnet, transition):
         #       print("Transition removed")
        count = 0

        while(count<15):
            count += 1
            for transition in pnet.transitions.copy():
                if Reducer.remove_local_transition(pnet, transition):
                    break
                break
            break


    @staticmethod
    def remove_place(net, place):
        for other_place in net.places:
            if(set(arc.source for arc in other_place.in_arcs) == set(arc.source for arc in place.in_arcs) and set(arc.target for arc in other_place.out_arcs) == set(arc.target for arc in place.out_arcs) and place != other_place):
                petri_utils.remove_place(net, place)
                return True
        return False

    @staticmethod
    def remove_transition(net, transition):
        #couldnt check it yet really due to lack of cases
        #check if current transition has one in on out arc (might not be sufficient todo check)
        # find a t1 
        for other_transition in net.transitions:
            if (set(arc.source for arc in other_transition.in_arcs) == set(arc.source for arc in transition.in_arcs) and
                set(arc.target for arc in other_transition.out_arcs) == set(arc.target for arc in transition.out_arcs) and
                transition != other_transition):
                petri_utils.remove_transition(net, transition)
                return True
        return False
    

    @staticmethod
    def remove_local_transition(net, transition):
        #todo: dont delet interacting transitions
        if len(transition.in_arcs) == 1 and len(transition.out_arcs) == 1:
            place_before_transition = list(transition.in_arcs)[0].source  # will be removed
            if len(place_before_transition.in_arcs) == 1 and len(place_before_transition.out_arcs) == 1:
                first_transition = list(place_before_transition.in_arcs)[0].source  # will point to last place
                place_after_transition = list(transition.out_arcs)[0].target #gets pointed from first_transition
                if (len(place_after_transition.in_arcs)== 1):
                    petri_utils.add_arc_from_to(first_transition, place_after_transition, net)
                    print("added one arc to: ")
                    print(transition.label)
                    petri_utils.remove_transition(net, transition)
                    petri_utils.remove_place(net, place_before_transition)

                    return True

        return False

    @staticmethod
    def place_merge(net, place):
        for other_place in net.places:
            
            #4th
            if (len((set(arc.source for arc in other_place.in_arcs)).intersection(set(arc.source for arc in place.in_arcs))) == 0):
                #6TH:
                set_of_places_to_t3_1 = {}
                set_of_places_to_t3_2 = {}
                for (x in set(arc.target for arc in place.out_arcs)):
                    set_of_places_to_t3_1.add(x.source)
                for (x in set(arc.target for arc in other_place.out_arcs)):
                    set_of_places_to_t3_2.add(x.source)
                if(set_of_places_to_t3_1.remove(place) == set_of_places_to_t3_2.remove(other_place)):
                    petri_utils.remove_place(net, place)
                    return True
                else:
                    return True
                return False


           

class Refiner:

    @staticmethod
    def place_addtion(net, start_trans, end_trans):
        #checks if 
        if isinstance(start_trans, pm4py.objects.petri_net.obj.PetriNet.Transition):
            if(start_trans.out_arcs.contains(end_trans)):
                t_help = PetriNet.Transition("helper", "helper")
                net.transitions.add(t_help)
                petri_utils.add_arc_from_to(start_trans, t_help, net)
                petri_utils.add_arc_from_to(t_help, end_trans, net)



        


