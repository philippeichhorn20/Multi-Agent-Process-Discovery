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
        
        for transition in pnet.transitions:
            if Reducer.remove_local_transition(pnet, transition):
                print("Local Transition removed")


    @staticmethod
    def remove_place(net, place):
        if len(place.in_arcs) == 1 and len(place.out_arcs) == 1:
            in_t = list(place.in_arcs)[0].source
            out_t = list(place.out_arcs)[0].target
            other_ins = in_t.out_arcs.remove(list(place.in_arcs)[0])    # t1 to px archs
            if(other_ins and len(other_ins)> 0):
                other_outs = list(other_ins)[0].target.out_arcs    # px to t2 archs
                if( other_outs > 0 and list(other_outs)[0].target == list(place.out_arcs)[0].target):
                    petri_utils.remove_arc(arc=list(place.in_arcs)[0], net=net)
                    petri_utils.remove_arc(arc=list(place.out_arcs)[0],net=net)
                    #petri_utils.remove_place(place=place, net=net)
                    return True
        return False

    @staticmethod
    def remove_transition(net, transition):
        if len(transition.in_arcs) == 1 and len(transition.out_arcs) == 1:
            in_p = list(transition.in_arcs)[0].source
            out_p = list(transition.out_arcs)[0].target
            if in_p.label != out_p.label:
                petri_utils.remove_arc(arc=list(transition.in_arcs)[0], net=net)
                petri_utils.remove_arc(arc=list(transition.out_arcs)[0], net=net)
                #petri_utils.remove_transition(trans=transition, net=net)
                petri_utils.add_arc_from_to(in_p, out_p, net)
                return True        
        return False
    

    @staticmethod
    def remove_local_transition(net,transition):
        place_before_transition = list(transition.in_arcs)[0].source
      #  first_transition = list(place_bef)

    @staticmethod
    def remove_local_transition_old(net, transition):
        print(transition.label)
        if (len(transition.in_arcs) > 0 and len(transition.out_arcs)>0):
            print("step 1")
            p1 = list(transition.in_arcs)[0].source
            p2 = list(transition.out_arcs)[0].target

            if  (len(p1.in_arcs)> 0 and len(p2.out_arcs)> 0 ):
                print("step 2")

                t1 = list(p1.in_arcs)[0].source
                if(p1 and p2 and t1):
                    print("step 3")

                    if len(transition.in_arcs) == 1 and len(transition.out_arcs) == 1 and len(p1.in_arcs) == 1:
                        print("step 4")
                        petri_utils.remove_arc(arc = list(p1.in_arcs)[0], net = net)

                        petri_utils.add_arc_from_to(t1, p2, net)

                        petri_utils.remove_arc(arc = list(p1.out_arcs)[0], net =net)
                        petri_utils.remove_arc(arc = list(transition.out_arcs)[0], net = net)
                        #petri_utils.remove_arc(arc = list(p1.in_arcs)[0], net = net)
                        #petri_utils.remove_transition(trans = transition, net = net)
                        #petri_utils.remove_place(place = p2, net = net)
                        return True

    @staticmethod
    def place_merge(net, place):
        if len(place.out_arcs) == 2:
            t1 = list(place.out_arcs)[0].target
            t2 = list(place.out_arcs)[1].target
            if t1.label == t2.label:
                petri_utils.remove_arc(list(place.out_arcs)[0], net)
                petri_utils.remove_arc(list(place.out_arcs)[1], net)
                petri_utils.remove_place(place, net)
                petri_utils.add_arc_from_to(t1, t2, net)
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



        


