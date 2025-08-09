import pm4py
import pandas as pd

from services.log_store import LogStore

class Data_Loader:

    @staticmethod
    def group_dataframe_by_resource(data_storage: LogStore):
        """
        This function splits the logs by the resource.
        In  doing so it accounts for 3 different log modes.
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


