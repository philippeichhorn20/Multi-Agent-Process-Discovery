
import logging
import os
from pm4py import write_pnml

def export_to_pnml(net, initial_marking, final_marking):
    logging.info("Exporting Petri net to PNML")
    temp_pnml_path = 'final_output.pnml'
    try:
        write_pnml(net, initial_marking, final_marking, temp_pnml_path)
        with open(temp_pnml_path, 'r') as pnml_file:
            pnml_content = pnml_file.read()
        return pnml_content
    except Exception as e:
        logging.error(f"Error during PNML export: {str(e)}")
        raise
    finally:
        if os.path.exists(temp_pnml_path):
            os.remove(temp_pnml_path)
