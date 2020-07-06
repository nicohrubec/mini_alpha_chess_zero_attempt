import torch
import torch.nn as nn
import torch.nn.functional as F


class ResLayer(nn.Module):

    def __init__(self):
        super(ResLayer, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=128, out_channels=128, kernel_size=(3, 3), stride=1)
        self.batch_norm1 = nn.BatchNorm2d(128)

        self.conv2 = nn.Conv2d(in_channels=128, out_channels=128, kernel_size=(3, 3), stride=1)
        self.batch_norm2 = nn.BatchNorm2d(128)

    def forward(self, x):
        x = self.conv1(x)
        x = self.batch_norm1(x)
        x = F.relu(x)

        x1 = self.conv2(x)
        x1 = self.batch_norm2(x1)

        out = x + x1
        out = F.relu(out)

        return out


class ResNet(nn.Module):

    def __init__(self):
        super(ResNet, self).__init__()
        self.inp_conv = nn.Conv2d(in_channels=18, out_channels=128, kernel_size=(3, 3), stride=1)
        self.inp_batch_norm = nn.BatchNorm2d(128)

        self.res_layer1 = ResLayer()
        self.res_layer2 = ResLayer()
        self.res_layer3 = ResLayer()
        self.res_layer4 = ResLayer()
        self.res_layer5 = ResLayer()

        self.val_conv = nn.Conv2d(in_channels=128, out_channels=128, kernel_size=(1, 1), stride=1)
        self.val_batch_norm = nn.BatchNorm2d(128)
        self.val_lin1 = nn.Linear(128, 256)
        self.val_lin2 = nn.Linear(256, 1)

    def forward(self, state):
        # input conv layer
        x = self.inp_conv(state)
        x = self.inp_batch_norm(x)
        x = F.relu(x)

        # residual layers
        x = self.res_layer1(x)
        x = self.res_layer2(x)
        x = self.res_layer3(x)
        x = self.res_layer4(x)
        x = self.res_layer5(x)

        # value head
        v = self.val_conv(x)
        v = self.val_batch_norm(v)
        v = F.relu(v)
        v = self.val_lin1(v)
        v = F.relu(v)
        v = self.val_lin2(v)
        v = F.tanh(v)

        return v
