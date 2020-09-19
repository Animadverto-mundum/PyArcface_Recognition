import torch



class CNN(torch.nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        # 3 64 64
        self.layer1 = torch.nn.Sequential(torch.nn.Conv2d(in_channels=3,
                                                          out_channels=8,
                                                          kernel_size=(3, 3),
                                                          stride=(1, 1),
                                                          padding_mode='SAME'),
                                          torch.nn.ReLU(),
                                          torch.nn.MaxPool2d(kernel_size=(2, 2),
                                                             stride=(2, 2),
                                                             padding=0,
                                                             ),
                                          )
        # 8 32 32
        self.layer2 = torch.nn.Sequential(torch.nn.Conv2d(in_channels=8,
                                                          out_channels=16,
                                                          kernel_size=(5, 5),
                                                          stride=(1, 1),
                                                          padding_mode='SAME'),
                                          torch.nn.ReLU(),
                                          torch.nn.MaxPool2d(kernel_size=(2, 2),
                                                             stride=(2, 2),
                                                             padding=0,
                                                             ),
                                          )
        # 16 13 13
        self.layer3 = torch.nn.Linear(16 * 13 * 13, 2)

    def forward(self, pic):
        data = self.layer1(pic)
        data = self.layer2(data)
        data = data.view(data.size(0), -1)
        data = self.layer3(data)
        return data



