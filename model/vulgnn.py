import torch
from torch_geometric.nn import GATv2Conv, GENConv, DeepGCNLayer, GraphNorm, LayerNorm, TopKPooling, global_mean_pool, global_max_pool
from torch.nn import Linear, ReLU
import torch.nn.functional as F

class VulGAT(torch.nn.Module):
    def __init__(self, num_node_features: int, num_edge_features: int, num_classes: int, hidden_channels: int, num_heads: int, num_layers: int, lin_hidden_channels: list[int]):
        super().__init__()
        self.num_layers = num_layers
        self.conv_layers = torch.nn.ModuleList([])
        self.norm_layers = torch.nn.ModuleList([])
        self.pooling_layers = torch.nn.ModuleList([])
        self.linear_layers = torch.nn.ModuleList([])

        self.conv_layers.append(GATv2Conv(num_node_features, hidden_channels, num_heads, edge_dim=num_edge_features))
        self.norm_layers.append(GraphNorm(hidden_channels * num_heads))
        self.pooling_layers.append(TopKPooling(hidden_channels * num_heads, ratio=0.8))
        for _ in range(num_layers - 1):
            self.conv_layers.append(GATv2Conv(hidden_channels * num_heads, hidden_channels, num_heads, edge_dim=num_edge_features))
            self.norm_layers.append(GraphNorm(hidden_channels * num_heads))
            self.pooling_layers.append(TopKPooling(hidden_channels * num_heads, ratio=0.8))
                
        self.linear_layers.append(Linear(hidden_channels * num_heads * 2, lin_hidden_channels[0]))
        for i in range(1, len(lin_hidden_channels)):
            self.linear_layers.append(Linear(lin_hidden_channels[i - 1], lin_hidden_channels[i]))
        self.linear_layers.append(Linear(lin_hidden_channels[-1], num_classes))

    def forward(self, data):
        x, edge_index, edge_attr, batch = data.x, data.edge_index, data.edge_attr, data.batch

        for i in range(self.num_layers):
            x = self.conv_layers[i](x, edge_index, edge_attr)
            x = self.norm_layers[i](x, batch)
            x = x.relu()
            x, edge_index, edge_attr, batch, _, _ = self.pooling_layers[i](x, edge_index, edge_attr, batch)

        x = torch.cat((global_mean_pool(x, batch), global_max_pool(x, batch)), dim=1)
        x = F.dropout(x, p=0.1, training=self.training)
        for i in range(len(self.linear_layers) - 1):
            x = self.linear_layers[i](x).relu()
        x = self.linear_layers[-1](x)
        return F.log_softmax(x, dim=-1)

class VulDeeperGCN(torch.nn.Module):
    def __init__(self, num_node_features: int, num_edge_features: int, num_classes: int, hidden_channels: int, num_layers: int, lin_hidden_channels: list[int]):
        super().__init__()

        self.node_encoder = Linear(num_node_features, hidden_channels)
        self.edge_encoder = Linear(num_edge_features, hidden_channels)

        self.deep_gcn_layers = torch.nn.ModuleList([])
        for _ in range(num_layers):
            conv = GENConv(hidden_channels, hidden_channels, aggr='softmax', t=1.0, learn_t=True, num_layers=2, norm='layer')
            norm = LayerNorm(hidden_channels, affine=True)
            act = ReLU(inplace=True)
            layer = DeepGCNLayer(conv, norm, act, block='res+', dropout=0.1)
            self.deep_gcn_layers.append(layer)

        self.linear_layers = torch.nn.ModuleList([])
        self.linear_layers.append(Linear(hidden_channels * 2, lin_hidden_channels[0]))
        for i in range(1, len(lin_hidden_channels)):
            self.linear_layers.append(Linear(lin_hidden_channels[i - 1], lin_hidden_channels[i]))
        self.linear_layers.append(Linear(lin_hidden_channels[-1], num_classes))

    def forward(self, data):
        x, edge_index, edge_attr, batch = data.x, data.edge_index, data.edge_attr, data.batch
        x = self.node_encoder(x)
        edge_attr = self.edge_encoder(edge_attr)

        x = self.deep_gcn_layers[0].conv(x, edge_index, edge_attr)
        for deep_gcn_layer in self.deep_gcn_layers[1:]:
            x = deep_gcn_layer(x, edge_index, edge_attr)
        x = self.deep_gcn_layers[0].act(self.deep_gcn_layers[0].norm(x))

        x = torch.cat((global_mean_pool(x, batch), global_max_pool(x, batch)), dim=1)
        x = F.dropout(x, p=0.1, training=self.training)
        for i in range(len(self.linear_layers) - 1):
            x = self.linear_layers[i](x).relu()
        x = self.linear_layers[-1](x)

        return F.log_softmax(x, dim=-1)

def checkpoint(model, filename: str, device: torch.device):
    model.cpu()
    torch.save(model, filename)
    model.to(device)
    
def resume(filename: str):
    return torch.load(filename)
