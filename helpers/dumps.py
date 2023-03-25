import pickle
import networkx as nx


def load_dump(file_name):
    try:
        with open(f'{file_name}.pickle', 'rb') as f:
            response = pickle.load(f)
            print(f'Loading {file_name} from dump. Length: {len(response)}')

            return response
    except:
        if file_name.lower().find('graph') != -1:
            return nx.Graph()
        else:
            return {}


def save_dump(file_name, variable):
    with open(f'{file_name}.pickle', 'wb') as f:
        pickle.dump(variable, f)
