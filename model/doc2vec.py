import pandas as pd
import json
import re
from tqdm import tqdm
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.models.keyedvectors import KeyedVectors
from multiprocessing import Pool, cpu_count
import pickle
import os
import logging
import gzip

D2V_MODEL_PATH = 'llvm_ir_cpg_d2v.pkl.gz'
TRAIN_DATA_PATH = 'llvm_ir_cpg_d2v_train_data.pkl.gz'
LLVM_IR_CPG_DF_PATH = '../dataset/big_vul_ir_cpg.zip'
WORKERS = cpu_count()
VECTOR_SIZE = 100
MIN_COUNT = 1
WINDOW = 10
EPOCHS = 20

def parse_cpg_sentences(cpg):
    cpg_sentences = []
    cpg = json.loads(cpg)
    for node in cpg['nodes']:
        cpg_sentences.append(node['feature'])
    for edge in cpg['edges']:
        if 'feature' in edge:
            cpg_sentences.append(edge['feature'])
    return cpg_sentences

def tokenize(sentence):
    tokens = re.split('([,.\\?:;\'\"\|()\[\]{} ])', sentence)
    return [token for token in tokens if len(token) > 0 and token != ' ']

if __name__ == '__main__':
    if os.path.exists(D2V_MODEL_PATH):
        print(f'A pretrained Doc2Vec model is found as {D2V_MODEL_PATH}')
        exit()
    sentences = []
    if os.path.exists(TRAIN_DATA_PATH):
        print(f'A Doc2Vec-compatible training data is found at {TRAIN_DATA_PATH}')
        print(f'Loading the training data from {TRAIN_DATA_PATH}')
        with gzip.open(TRAIN_DATA_PATH, 'rb') as data_gz:
            sentences = pickle.load(data_gz)
    else:
        print(f'Loading the dataset from {LLVM_IR_CPG_DF_PATH}')
        ir_cpg_df = pd.read_pickle(LLVM_IR_CPG_DF_PATH)
        with Pool(processes=WORKERS) as pool:
            for cpg_sentences in tqdm(pool.imap(parse_cpg_sentences, ir_cpg_df['cpg'].tolist()), total=ir_cpg_df.shape[0], desc='Creating sentence set'):
                sentences += cpg_sentences
        sentences = [TaggedDocument(tokenize(sentence), [i]) for i, sentence in tqdm(enumerate(sentences), total=len(sentences), desc='Tokenizing sentences')]
        print(f'Saving the training data to {TRAIN_DATA_PATH}')
        with gzip.open(TRAIN_DATA_PATH, 'wb') as data_gz:
            pickle.dump(sentences, data_gz)

    print("Initialising a Doc2Vec model...")
    model = Doc2Vec(
        vector_size=VECTOR_SIZE,
        dm=1,
        dm_concat=1,
        min_count=MIN_COUNT,
        window=WINDOW,
        workers=WORKERS,
        epochs=EPOCHS
    )
    print("Building the model's vocabulary...")
    model.build_vocab(sentences)
    
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    model.train(
        sentences,
        epochs=model.epochs,
        total_examples=model.corpus_count
    )

    model.dv = KeyedVectors(model.vector_size)
    print(f'Saving the trained Doc2Vec model to {D2V_MODEL_PATH}')
    with gzip.open(D2V_MODEL_PATH, 'wb') as model_gz:
        pickle.dump(model, model_gz)