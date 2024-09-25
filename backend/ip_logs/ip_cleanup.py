import xml.dom.minidom as minidom
import random

def determine_agent(concept_name):
    if concept_name.startswith("s"):
        if( random.randint(0,1) == 1):
            return ["Agent 1"]
        else:
            return ["Agent 2"]
    elif (
        concept_name.startswith("t")
        or concept_name.startswith("a!")
        or concept_name.startswith("b?")
    ):
        return ["Agent 1"]
    elif (
        concept_name.startswith("q")
        or concept_name.startswith("a?")
        or concept_name.startswith("b!")
    ):
        return ["Agent 2"]
    else:
        return ["Unknown"]


def add_org_resource(input_path, output_path):
    # Parse the XML file
    dom = minidom.parse(input_path)

    # Process each trace
    for trace in dom.getElementsByTagName("trace"):
        for event in trace.getElementsByTagName("event"):
            concept_name_elem = event.getElementsByTagName("string")
            for elem in concept_name_elem:
                if elem.getAttribute("key") == "concept:name":
                    concept_name = elem.getAttribute("value")
                    agents = determine_agent(concept_name)

                    # Remove existing org:resource elements
                    for org_elem in event.getElementsByTagName("string"):
                        if org_elem.getAttribute("key") == "org:resource":
                            event.removeChild(org_elem)

                    # Add new org:resource elements
                    for agent in agents:
                        org_resource_elem = dom.createElement("string")
                        org_resource_elem.setAttribute("key", "org:resource")
                        org_resource_elem.setAttribute("value", agent)
                        event.appendChild(org_resource_elem)
                    break

    # Write the modified XML to the output file
    with open(output_path, "w", encoding="utf-8") as f:
        # Split the XML string into lines
        xml_string = dom.toprettyxml(indent="\t")
        lines = xml_string.split("\n")

        # Remove empty lines and write to file
        non_empty_lines = [line for line in lines if line.strip()]
        f.write("\n".join(non_empty_lines))


# Example usage
log_path = "/Users/philippeichhorn/Downloads/logs1/IP-12/IP-12_init_log.xes"
output_path = "./IP-12_init_log_new.xes"

add_org_resource(log_path, output_path)
