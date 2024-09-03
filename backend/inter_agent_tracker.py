

# This class finds the places and transitions between agents and adds them to the net, marked as -ia-
class Inter_Agent_Tracker:
    
    
    @staticmethod
    def track_inter_agent(net, logs):
        for place in net.places:
            in_transitions = [arc.source for arc in place.in_arcs]
            out_transitions = [arc.target for arc in place.out_arcs]
