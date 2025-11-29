from typing import Optional

import numpy as np
import torch
from torch import nn
from torch.utils.data import TensorDataset, DataLoader

class _LSTMRegressor(nn.Module):
    def __init__(self, n_features: int, hidden_size: int = 32, num_layers: int = 1):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=n_features,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
        )
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        last = out[:, -1, :]
        y = self.fc(last)
        return y.squeeze(-1)

class SequenceDULModel:
    """LSTM-based sequence model for DUL from time-series telemetry."""

    def __init__(self, n_features: int, hidden_size: int = 32, num_layers: int = 1, lr: float = 1e-3):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.net = _LSTMRegressor(n_features, hidden_size, num_layers).to(self.device)
        self.optimizer = torch.optim.Adam(self.net.parameters(), lr=lr)
        self.loss_fn = nn.MSELoss()

    def fit(self, X_seq: np.ndarray, y_seq: np.ndarray, epochs: int = 10, batch_size: int = 32):
        dataset = TensorDataset(
            torch.tensor(X_seq, dtype=torch.float32),
            torch.tensor(y_seq, dtype=torch.float32),
        )
        loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

        self.net.train()
        for epoch in range(epochs):
            total_loss = 0.0
            for xb, yb in loader:
                xb = xb.to(self.device)
                yb = yb.to(self.device)
                self.optimizer.zero_grad()
                pred = self.net(xb)
                loss = self.loss_fn(pred, yb)
                loss.backward()
                self.optimizer.step()
                total_loss += float(loss.item()) * len(xb)
        return total_loss / len(dataset)

    def predict(self, X_seq: np.ndarray) -> np.ndarray:
        self.net.eval()
        with torch.no_grad():
            x = torch.tensor(X_seq, dtype=torch.float32).to(self.device)
            y = self.net(x)
            return y.cpu().numpy()
