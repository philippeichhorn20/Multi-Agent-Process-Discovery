import pm4py
import pandas as pd

from Reducer import Reducer 
from NetStorer import NetStorer

class Data_Loader:
    def create_petri_net(path):
        log = pm4py.read_xes(file_path=path)
        df = pm4py.convert_to_dataframe(log)
        df_grouped = df.groupby(by='org:resource')    # groups it by agent, in this dataset called "org:resource"
        list_of_nets = []

        for name, group in df_grouped:
            # using Inductive Miner to discover a petri net of each agent seperately
            net, im, fm = pm4py.discover_petri_net_inductive(group, activity_key='concept:name', case_id_key='case:concept:name', timestamp_key='time:timestamp')
            list_of_nets.append((net, im, fm))
        return list_of_nets
    
    @staticmethod
    def group_dataframe_by_resource(data_storage: NetStorer):
        """
        This function builds seperate petri nets for each Agent (1: org:resource, 2: org:group, 3: org:resource)
        It fetches initializes the 
        """
        df = data_storage.df

        if 'org:group' in df.columns:
            df['org:agent'] = df['org:group']
        else:
            df['org:agent'] = df['org:resource']

        if "msgFlow" in df.columns and "msgType" in df.columns:
            print("Log 2 mode")
            df['org:messageString'] = df.apply(
            lambda row: f"{row['msgFlow']}!" if row['msgType'] == 'send' else (f"{row['msgFlow']}?" if row['msgType'] == 'receive' else ''),
            axis=1
        )
        elif "Message:Sent" in df.columns and "Message:Rec" in df.columns:
            print("Log 3 mode")
            df['org:messageString'] = df.apply(
                lambda row: (
                    (str(row['Message:Sent'])+"!" if pd.notnull(row['Message:Sent']) and row['Message:Sent']!="null" else '') +
                    (str(row['Message:Rec'])+"?" if pd.notnull(row['Message:Rec']) and row['Message:Rec']!="null" else '')
                ),
                axis=1
            )
        else:
            print("Log 1 mode")
            df['org:messageString'] = df['concept:name']
            return df.groupby(by='org:agent')
        df['concept:name'] = df['concept:name'] + "__" + df['org:messageString']
        df_grouped = df.groupby(by='org:agent')    # groups it by the new column 'org:agent'
        return df_grouped

    def get_net_from_pnml(path):
        net, im, fm = pm4py.read_pnml(path)
        x = net,im,fm
        return [x]

    def encode_messages_from_name_string(name: str):
        messages_in = []
        messages_out = []
        isInteraction = '!' in name or '?' in name
        if not isInteraction:
            return False, messages_in, messages_out
        
        # D3__m2, m1!m4, m15?