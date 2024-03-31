import torch
from torchvision import models, transforms

class FeatureExtractor:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = models.resnet50(pretrained=True).to(self.device)
        self.model.eval()
        self.transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def extract_features(self, frame):
        frame = self.transform(frame).unsqueeze(0).to(self.device)
        with torch.no_grad():
            features = self.model(frame)
        return features.squeeze().cpu().numpy()