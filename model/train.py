import sys
sys.path.append('../')
from dataset.cpg_dataset import InMemoryCPGDataset
from torch_geometric.loader import DataListLoader
import torch
from torch_geometric.nn import DataParallel
from sklearn.metrics import confusion_matrix, f1_score, accuracy_score, precision_score, recall_score, roc_auc_score
from vulgnn import VulGAT, VulDeeperGCN, checkpoint, resume
from tqdm import tqdm
import numpy as np
from datetime import datetime
import os
import gc

model_filename_prefix = 'vuldeepergcn_'

train_dataset = InMemoryCPGDataset(root='../dataset/cpg_dataset/')
val_dataset = InMemoryCPGDataset(root='../dataset/cpg_dataset/', val=True)

train_loader = DataListLoader(train_dataset, batch_size=4, shuffle=True)
val_loader = DataListLoader(val_dataset, batch_size=4, shuffle=True)

num_node_features = train_dataset.num_node_features
num_edge_features = train_dataset.num_edge_features
num_classes = train_dataset.num_classes
print("num_node_features:", num_node_features)
print("num_edge_features:", num_edge_features)
print("num_classes:", num_classes)

model = VulDeeperGCN(num_node_features, num_edge_features, num_classes, hidden_channels=128, num_layers=32, lin_hidden_channels=[128])
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = DataParallel(model)
model.to(device)
print(model)

optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)
criterion = torch.nn.NLLLoss()

def train(epoch: int):
    model.train()
    total_loss = 0
    for data_list in tqdm(train_loader, desc=f'Epoch {epoch} training'):
        optimizer.zero_grad()
        out = model(data_list)
        y = torch.cat([data.y for data in data_list]).to(out.device)
        loss = criterion(out, y)
        total_loss += loss.item() * len(data_list)
        loss.backward()
        optimizer.step()
    return total_loss / train_loader.dataset.len()

@torch.no_grad()
def test(dataloader: DataListLoader, dataset_type: str):
    model.eval()
    all_preds = []
    all_labels = []
    correct = 0
    total_loss = 0
    for data_list in tqdm(dataloader, desc=f'Testing on {dataset_type} set'):
        out = model(data_list)
        y = torch.cat([data.y for data in data_list]).to(out.device)
        loss = criterion(out, y)
        total_loss += loss.item() * len(data_list)
        pred = out.argmax(dim=1)
        correct += int((pred == y).sum())
        all_preds.append(pred.cpu().detach().numpy())
        all_labels.append(y.cpu().detach().numpy())
    
    all_preds = np.concatenate(all_preds).ravel()
    all_labels = np.concatenate(all_labels).ravel()
    calculate_metrics(all_preds, all_labels)
    return correct / dataloader.dataset.len(), total_loss / dataloader.dataset.len()

@torch.no_grad()
def predict(dataloader: DataListLoader, dataset_type: str):
    model.eval()
    all_preds = []
    all_labels = []
    correct = 0
    for data_list in tqdm(dataloader, desc=f'Testing on {dataset_type} set'):
        out = model(data_list)
        y = torch.cat([data.y for data in data_list]).to(out.device)
        pred = out.argmax(dim=1)
        correct += int((pred == y).sum())
        all_preds.append(pred.cpu().detach().numpy())
        all_labels.append(y.cpu().detach().numpy())
    
    all_preds = np.concatenate(all_preds).ravel()
    all_labels = np.concatenate(all_labels).ravel()
    calculate_metrics(all_preds, all_labels)
    return correct / dataloader.dataset.len()

def calculate_metrics(y_pred, y_true):
    print(f"Confusion matrix:\n{confusion_matrix(y_pred, y_true)}")
    print(f"F1 Score: {f1_score(y_true, y_pred):.4f}")
    print(f"Accuracy: {accuracy_score(y_true, y_pred):.4f}")
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    try:
        roc = roc_auc_score(y_true, y_pred)
        print(f"ROC AUC: {roc:.4f}")
    except:
        print(f"ROC AUC: notdefined")

num_epochs = 128
early_stop_thresh = 4
min_epochs = 16
best_loss = None
best_epoch = 0

train_losses = []
val_losses = []
for epoch in range(num_epochs):
    train_loss = train(epoch)
    torch.cuda.empty_cache()
    gc.collect()

    val_acc, val_loss = test(val_loader, dataset_type='validation')
    torch.cuda.empty_cache()
    gc.collect()

    train_losses.append(train_loss)
    val_losses.append(val_loss)
    print(f'End of Epoch {epoch}, Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}')
    if epoch == 0:
        best_loss = val_loss
        checkpoint(model.module, model_filename_prefix + 'best_model.pt', device)
    elif val_loss < best_loss:
        best_loss = val_loss
        best_epoch = epoch
        checkpoint(model.module, model_filename_prefix + 'best_model.pt', device)
    elif epoch - best_epoch - min_epochs > early_stop_thresh:
        print(f'Early stopped training at epoch {epoch}')
        break

timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
os.rename(model_filename_prefix + 'best_model.pt',  model_filename_prefix + f'model_{timestamp}.pt')

model_filename =  model_filename_prefix + f'model_{timestamp}.pt'
test_dataset = InMemoryCPGDataset(root='../dataset/cpg_dataset/', test=True)
test_loader = DataListLoader(test_dataset, batch_size=1, shuffle=False)
model = resume(model_filename_prefix + f'model_{timestamp}.pt')
model = DataParallel(model)
model.to(device)
test_acc, test_loss = test(test_loader, dataset_type='testing')
os.rename(model_filename,  model_filename_prefix + f'model_{timestamp}_test{test_acc:.4f}.pt')
