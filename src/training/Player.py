import torch

from training.net import ResNet


class Player:

    def __init__(self, device):
        self.device = device
        self.net = ResNet().to(device)
        self.move_log = []

    def reset_log(self):
        self.move_log = None

    def log(self, record):
        self.move_log.append(record)  # add one new training sample

    def sample(self):
        raise NotImplementedError  # sample batches from current log

    def train(self):
        raise NotImplementedError  # sample and train with batches

    def predict(self, state):
        state = torch.tensor(state, dtype=torch.float32).to(self.device)
        state = torch.unsqueeze(state, 0)
        return self.net(state).cpu()  # return a heuristic value from the neural network for a given state

    def load_checkpoint(self, model_name):
        raise NotImplementedError  # if you wanna continue training from previously saved checkpoint
