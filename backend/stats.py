import pm4py
from pm4py.objects.petri_net.obj import PetriNet, Marking
import subprocess
import NetStorer
import os
def alignment_fitness(net: PetriNet, logs, initial: Marking, final: Marking):
    # Convert log to dataframe and group by org:resource
    fitness = pm4py.fitness_alignments(logs, petri_net=net, initial_marking=initial, final_marking=final)
    return fitness

def alignment_precision(net: PetriNet, logs, initial: Marking, final: Marking):
    precision = pm4py.precision_alignments(logs, petri_net=net, initial_marking=initial, final_marking=final)
    print(precision)
    return precision

def entropy_based_precision_old():

    xes_path = 'temp_log_stats.xes'
    pnml_path = 'temp_net.pnml'
    cmd = ["java", "-jar", f"codebase-master/jbpt-pm/entropia/jbpt-pm-entropia-1.7.jar", "-empr", "-s", f"-rel={xes_path}", f"-ret={pnml_path}"]
    result = subprocess.run(cmd, capture_output=False)
    responsestring = result.stdout.decode('utf-8')
    print("response", responsestring)
    precision, recall = responsestring.split(", ")

    
    return precision, recall

def entropy_based_fitness():
	None
     


def entropy_based_precision(net_storage: NetStorer.NetStorer, net: PetriNet, initial: Marking, final: Marking):
    try:
        xes_path = './entropy_temp_log.xes'
        pnml_path = './entropy_temp_net.pnml'

        print("fiowej")
        print(net_storage.df)
        print(net)
        pm4py.write.write_xes(log=net_storage.df, file_path=xes_path, case_id_key='case:concept:name', encoding="utf-8", )
        pm4py.write.write_pnml(petri_net=net, initial_marking=initial, final_marking=final,file_path=pnml_path)
        
        cmd = ["java", "-jar", f"codebase-master/jbpt-pm/entropia/jbpt-pm-entropia-1.7.jar", "-empr", f"-rel={xes_path}", f"-ret={pnml_path}"]
        result = subprocess.run(cmd)
        responsestring = result.stdout.decode('utf-8')
        print("response: ", responsestring)
        precision, recall = responsestring.split(", ")
    finally:
        if os.path.exists(xes_path):
            os.remove(xes_path)
        if os.path.exists(pnml_path):
            os.remove(pnml_path)
    return precision, recall