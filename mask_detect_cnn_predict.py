import torch
import cv2


class Net():
    def __init__(self):
        self.path = 'mask_detect_cnn.pkl'

    def load(self, path=0):
        if path == 0:
            path = self.path
        self.cnn_net = torch.load(self.path)

    def predict(self, data):
        if type(data) == str:
            data = cv2.imread(data)
        pic = cv2.resize(data, (64, 64))
        pic = torch.tensor(pic.T, dtype=torch.float32)
        prediction = self.cnn_net(pic.unsqueeze(0)).detach().numpy()
        label_predicted = prediction.tolist()[0].index(prediction[0].max())
        return label_predicted


