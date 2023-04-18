# VulGNN-LLVM-CPG
Vulnerability Detection using Graph Neural Network on LLVM IR Code Property Graphs

Tested on Ubuntu 18.06
## Dependencies
1. Create a conda env and install the packages mentioned in [requirements.txt](requirements.txt).
2. Install [Joern](https://docs.joern.io/installation), [llvm2cpg 0.8.0](https://github.com/ShiftLeftSecurity/llvm2cpg), and [clang 11](https://releases.llvm.org/11.1.0/tools/clang/docs/index.html).

## Dataset
1. Run [dataset/data_preprocessing.ipynb](/dataset/data_preprocessing.ipynb) for downloading and preprocessing the Big-Vul dataset. It will create [dataset/big_vul_preprocessed.zip](/dataset/big_vul_preprocessed.zip.txt) which has more consistent git commit ids and git repo links which are crucial for the compilation step later to generate IRs and CPGs
2. Run [dataset/ir_cpg_generating.ipynb](/dataset/ir_cpg_generating.ipynb) to generate the LLVM IR and CPG of the functions in Big-Vul. While running the compilation of each repo, it may fail due to missing required development libraries. Use the rerun block in the notebook to restart after installing the required libraries mentioned in the error_dump files for each repo at each pair of consecutive commits (before and after the vulnerability fix). This will generate [dataset/big_vul_ir_cpg.zip](/dataset/big_vul_ir_cpg.zip.txt) and create the train, val, and test sets for the GNN model. In the train set, the negative (non-vul) functions are downsampled, and the positive (vul) functios are oversampled to compensate its imbalance. All three sets are saved in [dataset/cpg_dataset/raw](dataset/cpg_dataset/raw/). [dataset/cpg_dataset](dataset/cpg_dataset/) is dedicated folder to store PyG graph datasets.
3. Run [model/doc2vec.py](/model/doc2vec.py) to train a Doc2Vec model which will be used to vectorize textual CPG nodes and edges so that the GNN can read the CPG. This will create [model/llvm_ir_cpg_d2v.pkl](model/llvm_ir_cpg_d2v.pkl.txt) for later use.
4. The script to train model will create PyG-compatible graphs using Doc2Vec on the go and save the processed sets in [dataset/cpg_dataset/processed](dataset/cpg_dataset/processed/) as `cpg_d2v_*.pt.gz`. If the hardware is limited, replace `InMemoryCPGDataset` with `CPGDataset` which generates and saves individual graph to a file such as `cpg_d2v_train_23.pt` for graph with id 23 in the train set. Both dataset classes are defined in [dataset/cpg_dataset.py](dataset/cpg_dataset.py).

## GNN Models
1. There are two GNN structures constructed: `VulGAT` based on [`GATv2Conv`](https://pytorch-geometric.readthedocs.io/en/latest/generated/torch_geometric.nn.conv.GATv2Conv.html) and `VulDeeperGCN` based on [`DeepGCNLayer`](https://pytorch-geometric.readthedocs.io/en/latest/generated/torch_geometric.nn.models.DeepGCNLayer.html). Check the details in [model/vulgnn.py](model/vulgnn.py).
2. Configure a model in [model/train.py](model/train.py) and run it to train it.
3. Evaluate the model in [model/eval.ipynb](model/eval.ipynb).

### Notes:
[dataset/ir_cpg_gen.sh](/dataset/ir_cpg_gen.sh) will take the git link of a repo, the commit hash representing the interested version of the repo, a dir name to clone the repo, and names of functions of which users wish to generate LLVM IR and CPG. CPG will be retrieved using `Joern` through [dataset/parse_cpg.sc](/dataset/parse_cpg.sc)
