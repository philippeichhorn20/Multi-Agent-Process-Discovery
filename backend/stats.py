import pm4py
from pm4py.objects.petri_net.obj import PetriNet, Marking
import subprocess

def alignment_fitness(net: PetriNet, logs, initial: Marking, final: Marking):
    # Convert log to dataframe and group by org:resource
    fitness = pm4py.fitness_alignments(logs, petri_net=net, initial_marking=initial, final_marking=final)
    return fitness

def alignment_precision(net: PetriNet, logs, initial: Marking, final: Marking):
    precision = pm4py.precision_alignments(logs, petri_net=net, initial_marking=initial, final_marking=final)
    print(precision)
    return precision

def entropy_based_precision():
    xes_path = 'temp_log.xes'
    pnml_path = 'temp_net.pnml'
    cmd = ["java", "-jar", f"codebase-master/jbpt-pm/entropia/jbpt-pm-entropia-1.7.jar", "-empr", "-s", f"-rel={xes_path}", f"-ret={pnml_path}"]
    result = subprocess.run(cmd, capture_output=True)
    responsestring = result.stdout.decode('utf-8')
    precision, recall = responsestring.split(", ")
    return precision, recall

def entropy_based_fitness():
	None