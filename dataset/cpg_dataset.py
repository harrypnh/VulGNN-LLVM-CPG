import sys
sys.path.append('../')
from torch_geometric.data import Dataset, Data
import torch
from model.doc2vec import tokenize
import os
import pickle
import pandas as pd
from tqdm import tqdm
import json
import gzip

class CPGDataset(Dataset):
    def __init__(self, root, filename_prefix='big_vul_ir_cpg_', d2v_path='../model/llvm_ir_cpg_d2v.pkl', test=False, val=False, transform=None, pre_transform=None, pre_filter=None):
        self.test = test
        self.val = val
        if test and val:
            print('ERROR: Either \'test\' or \'val\' can be True.')
            return
        elif test:
            self.filename = filename_prefix + 'test.zip'
        elif val:
            self.filename = filename_prefix + 'val.zip'
        else:
            self.filename = filename_prefix + 'train.zip'
        self.d2v_path = d2v_path
        print(f"Loading raw dataset for {'testing' if self.test else 'validation' if self.val else 'training'} from {os.path.join(root, 'raw', self.filename)}")
        self.data = pd.read_pickle(os.path.join(root, 'raw', self.filename))
        super(CPGDataset, self).__init__(root, transform, pre_transform, pre_filter)
        print(f"Dataset for {'testing' if self.test else 'validation' if self.val else 'training'} is ready")

    @property
    def num_classes(self):
        return len(self.data['vul'].unique())

    @property
    def raw_file_names(self):
        return self.filename

    @property
    def processed_file_names(self):
        if self.test:
            return [f'cpg_d2v_test_{i}.pt' for i in list(self.data.index)]
        elif self.val:
            return [f'cpg_d2v_val_{i}.pt' for i in list(self.data.index)]
        else:
            return [f'cpg_d2v_train_{i}.pt' for i in list(self.data.index)]
    
    def download(self):
        pass

    def process(self):
        sorted_data = self.data.sort_values(by='cpg', key=lambda x: x.str.len())
        print(f'Loading the pretrained Doc2Vec model from {self.d2v_path}')
        with open(self.d2v_path, 'rb') as d2v_pkl:
            self.d2v_model = pickle.load(d2v_pkl)
        edge_types_df = pd.get_dummies(pd.DataFrame({'value': [0, 1, 2, 3]}, index=['AST', 'CFG', 'CDG', 'DDG']), columns=['value'], dtype=float)
        self.edge_types = {edge_type: torch.tensor(edge_types_df.loc[edge_type].tolist()) for edge_type in edge_types_df.index.tolist()}

        for entry in tqdm(sorted_data.itertuples(), total=sorted_data.shape[0], desc='Creating PyG graphs'):
            if os.path.exists(os.path.join(self.processed_dir, f'cpg_d2v_test_{entry.Index}.pt')) and self.test:
                continue
            elif os.path.exists(os.path.join(self.processed_dir, f'cpg_d2v_val_{entry.Index}.pt')) and self.val:
                continue
            elif os.path.exists(os.path.join(self.processed_dir, f'cpg_d2v_train_{entry.Index}.pt')) and not self.test and not self.val:
                continue
            cpg = json.loads(entry.cpg)
            code_embeddings, code_mapping = self.__load_cpg_nodes(cpg['nodes'])
            edge_index, edge_attr = self.__load_cpg_edges(cpg['edges'], code_mapping)
            data = Data(
                x=code_embeddings,
                edge_index=edge_index,
                edge_attr=edge_attr,
                y=torch.tensor([entry.vul])
            )
            
            if self.test:
                torch.save(data, os.path.join(self.processed_dir, f'cpg_d2v_test_{entry.Index}.pt'))
            elif self.val:
                torch.save(data, os.path.join(self.processed_dir, f'cpg_d2v_val_{entry.Index}.pt'))
            else:
                torch.save(data, os.path.join(self.processed_dir, f'cpg_d2v_train_{entry.Index}.pt'))

    def __load_cpg_nodes(self, nodes):
        node_mapping = {}
        node_embeddings = []
        for i, node in enumerate(nodes):
            node_mapping[node['id']] = i
            node_embeddings.append(torch.tensor(self.d2v_model.infer_vector(tokenize(node['feature'])), dtype=torch.float32))
        node_embeddings = torch.stack(node_embeddings)
        return node_embeddings, node_mapping
    
    def __load_cpg_edges(self, edges, node_mapping):
        if len(edges) == 0:
            return None, None
        sources = []
        destinations = []
        for edge in edges:
            sources.append(node_mapping[edge['from_id']])
            destinations.append(node_mapping[edge['to_id']])
        edge_index = torch.tensor([sources, destinations])
        
        edge_features = []
        edge_type_tensors = []
        for edge in edges:
            if 'feature' in edge:
                edge_features.append(torch.tensor(self.d2v_model.infer_vector(tokenize(edge['feature'])), dtype=torch.float32))
            else:
                edge_features.append(torch.tensor([0] * self.d2v_model.vector_size, dtype=torch.float32))
            edge_type_tensors.append(self.edge_types[edge['type']])
        edge_type_tensors = torch.stack(edge_type_tensors)
        edge_embeddings = torch.stack(edge_features)
        edge_attr = torch.cat((edge_type_tensors, edge_embeddings), dim=1)
        return edge_index, edge_attr

    def len(self):
        return self.data.shape[0]

    def get(self, index):
        if self.test:
            data = torch.load(os.path.join(self.processed_dir, f'cpg_d2v_test_{index}.pt'))
        elif self.val:
            data = torch.load(os.path.join(self.processed_dir, f'cpg_d2v_val_{index}.pt'))
        else:
            data = torch.load(os.path.join(self.processed_dir, f'cpg_d2v_train_{index}.pt'))
        return data
    
    def get_class_info(self):
        print(f"non-vul\t{self.data['vul'].value_counts()[0]}")
        print(f"vul\t{self.data['vul'].value_counts()[1]}")

class InMemoryCPGDataset(Dataset):
    def __init__(self, root, filename_prefix='big_vul_ir_cpg_', d2v_path='../model/llvm_ir_cpg_d2v.pkl', test=False, val=False, transform=None, pre_transform=None, pre_filter=None):
        self.test = test
        self.val = val
        if test and val:
            print('ERROR: Either \'test\' or \'val\' can be True.')
            return
        elif test:
            self.filename = filename_prefix + 'test.zip'
        elif val:
            self.filename = filename_prefix + 'val.zip'
        else:
            self.filename = filename_prefix + 'train.zip'
        self.d2v_path = d2v_path
        super(InMemoryCPGDataset, self).__init__(root, transform, pre_transform, pre_filter)
        print(f'Loading the processed dataset from {self.processed_paths[0]}')
        with gzip.open(self.processed_paths[0], 'rb') as data_list_gz:
            self.data_list = pickle.load(data_list_gz)
        print(f"Dataset for {'testing' if self.test else 'validation' if self.val else 'training'} is ready")

    @property
    def raw_file_names(self):
        return self.filename

    @property
    def processed_file_names(self):
        if self.test:
            return ['cpg_d2v_test.pt.gz']
        elif self.val:
            return ['cpg_d2v_val.pt.gz']
        else:
            return ['cpg_d2v_train.pt.gz']

    def download(self):
        pass

    def process(self):
        print(f"Loading raw dataset for {'testing' if self.test else 'validation' if self.val else 'training'} from {os.path.join(self.raw_dir, self.filename)}")
        raw_data = pd.read_pickle(os.path.join(self.raw_dir, self.filename))
        print(f'Loading the pretrained Doc2Vec model from {self.d2v_path}')
        with open(self.d2v_path, 'rb') as d2v_pkl:
            self.d2v_model = pickle.load(d2v_pkl)
        edge_types_df = pd.get_dummies(pd.DataFrame({'value': [0, 1, 2, 3]}, index=['AST', 'CFG', 'CDG', 'DDG']), columns=['value'], dtype=float)
        self.edge_types = {edge_type: torch.tensor(edge_types_df.loc[edge_type].tolist()) for edge_type in edge_types_df.index.tolist()}
        data_list = []
        for entry in tqdm(raw_data.itertuples(), total=raw_data.shape[0], desc='Creating PyG graphs'):
            if os.path.exists(os.path.join(self.processed_dir, f'cpg_d2v_test_{entry.Index}.pt')) and self.test:
                data = torch.load(os.path.join(self.processed_dir, f'cpg_d2v_test_{entry.Index}.pt'))
                data_list.append(data)
                continue
            elif os.path.exists(os.path.join(self.processed_dir, f'cpg_d2v_val_{entry.Index}.pt')) and self.val:
                data = torch.load(os.path.join(self.processed_dir, f'cpg_d2v_val_{entry.Index}.pt'))
                data_list.append(data)
                continue
            elif os.path.exists(os.path.join(self.processed_dir, f'cpg_d2v_train_{entry.Index}.pt')) and not self.test and not self.val:
                data = torch.load(os.path.join(self.processed_dir, f'cpg_d2v_train_{entry.Index}.pt'))
                data_list.append(data)
                continue
            cpg = json.loads(entry.cpg)
            code_embeddings, code_mapping = self.__load_cpg_nodes(cpg['nodes'])
            edge_index, edge_attr = self.__load_cpg_edges(cpg['edges'], code_mapping)
            data = Data(
                x=code_embeddings,
                edge_index=edge_index,
                edge_attr=edge_attr,
                y=torch.tensor([entry.vul])
            )
            data_list.append(data)

        print(f'Saving the processed dataset to {self.processed_paths[0]}')
        with gzip.open(self.processed_paths[0], 'wb') as data_list_gz:
            pickle.dump(data_list, data_list_gz)

    def __load_cpg_nodes(self, nodes):
        node_mapping = {}
        node_embeddings = []
        for i, node in enumerate(nodes):
            node_mapping[node['id']] = i
            node_embeddings.append(torch.tensor(self.d2v_model.infer_vector(tokenize(node['feature'])), dtype=torch.float32))
        node_embeddings = torch.stack(node_embeddings)
        return node_embeddings, node_mapping
    
    def __load_cpg_edges(self, edges, node_mapping):
        if len(edges) == 0:
            return None, None
        sources = []
        destinations = []
        for edge in edges:
            sources.append(node_mapping[edge['from_id']])
            destinations.append(node_mapping[edge['to_id']])
        edge_index = torch.tensor([sources, destinations])
        
        edge_features = []
        edge_type_tensors = []
        for edge in edges:
            if 'feature' in edge:
                edge_features.append(torch.tensor(self.d2v_model.infer_vector(tokenize(edge['feature'])), dtype=torch.float32))
            else:
                edge_features.append(torch.tensor([0] * self.d2v_model.vector_size, dtype=torch.float32))
            edge_type_tensors.append(self.edge_types[edge['type']])
        edge_type_tensors = torch.stack(edge_type_tensors)
        edge_embeddings = torch.stack(edge_features)
        edge_attr = torch.cat((edge_type_tensors, edge_embeddings), dim=1)
        return edge_index, edge_attr

    def len(self):
        return len(self.data_list)

    def get(self, index):
        return self.data_list[index]