import torch.nn as nn

class cnn_lstm(nn.Module) :
    def __init__(self,batch_size,seq_len=seq_len, ini_len=18) :
        super().__init__()
        self.d_model = 20 
        self.batch_size = batch_size
        self.seq_len = seq_len
        self.hidden_size = 32
        self.num_layers = 1
        self.init_trnsfrm = nn.Sequential(nn.Linear(ini_len,32),nn.ReLU(),nn.Linear(32,32),nn.ReLU(),nn.Linear(32,self.d_model))
        self.batch_norm = nn.BatchNorm1d(self.d_model)
        self.cnn = nn.Sequential(nn.Conv1d(self.d_model, 32,4,1),
                                 nn.Conv1d(32,16,4,1),
                                 nn.Conv1d(16,16,4,1),
                                 nn.MaxPool1d(2,2),
                                 nn.Conv1d(16,self.d_model,4,1))
        self.lstm = nn.LSTM(self.d_model,self.hidden_size,self.num_layers,batch_first=True)
        self.final = nn.Sequential(nn.Linear(self.hidden_size*56,512),nn.ReLU(),nn.Linear(512,1))
    
    def forward(self,batch) :
        h_n, c_n = torch.ones((self.num_layers,self.batch_size,self.hidden_size),dtype=torch.float64),torch.ones((self.num_layers,self.batch_size,self.hidden_size),dtype=torch.float64)
        batch = self.cnn(self.batch_norm(self.init_trnsfrm(batch).transpose(1,2))).transpose(1,2)
        batch,(h_n,c_n) = self.lstm( batch , (h_n,c_n))
        del h_n,c_n
        out = self.final(batch.reshape(self.batch_size,self.hidden_size*56))
        return out