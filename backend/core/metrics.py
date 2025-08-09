from pm4py.objects.petri_net.obj import PetriNet, Marking
import subprocess
import services.log_store as log_store
import os
from pm4py.write import write_pnml
from pm4py import precision_alignments, fitness_alignments

def alignment_fitness(net: PetriNet, logs, initial: Marking, final: Marking):
    fitness = fitness_alignments(logs, petri_net=net, initial_marking=initial, final_marking=final)
    return fitness

def alignment_precision(net: PetriNet, logs, initial: Marking, final: Marking):
    precision = precision_alignments(logs, petri_net=net, initial_marking=initial, final_marking=final)
    return precision

def entropy_based_precision(log_storage: log_store.LogStore, net: PetriNet, initial: Marking, final: Marking):
    try:
        xes_path = './entropy_temp_log.xes'
        pnml_path = './entropy_temp_net.pnml'

        write_pnml(petri_net=net, initial_marking=initial, final_marking=final,file_path=pnml_path)

        cmd = ["java", "-jar", f"codebase-master/jbpt-pm/entropia/jbpt-pm-entropia-1.7.jar", "-empr","-s", f"-rel={log_storage.xes_path}", f"-ret={pnml_path}"]
        result = subprocess.run(cmd, capture_output=True,timeout=60000 )

        responsestring = result.stdout.decode('utf-8')
        precision, recall = 0,0
        if(responsestring.__contains__(",")):
            precision, recall = responsestring.split(", ")

    finally:
        None
        if os.path.exists(xes_path):
            os.remove(xes_path)
        if os.path.exists(pnml_path):
            os.remove(pnml_path)
    return precision, recall