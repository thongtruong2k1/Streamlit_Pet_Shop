from keras.preprocessing.image import img_to_array
from keras.applications.efficientnet import EfficientNetB0
from keras.models import Model

from PIL import Image
import pickle
import numpy as np

# Ham tao model
def get_extract_model():
    model = EfficientNetB0(weights="imagenet")
    extract_model = Model(inputs=model.inputs, outputs=model.get_layer("top_dropout").output)
    return extract_model

# Ham tien xu ly, chuyen doi hinh anh thanh tensor
def image_preprocess(img):
    img = img.resize((224, 224))
    img = img.convert("RGB")
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    return x

def extract_vector(model, image_path):
    print("Loading...")
    img = Image.open(image_path)
    img_tensor = image_preprocess(img)
    # Trich dac trung
    vector = model.predict(img_tensor)[0]
    # Chuan hoa vector = chia L2 norm(Khoang cach vector den goc toa do)
    vector = vector / np.linalg.norm(vector)
    return vector

def predict(search_image, model):
    # Khoi tao model

    # Trich dac trung anh search
    search_vector = extract_vector(model, search_image)

    # Load 4700 vector tu vectors.pkl ra bien
    vectors = pickle.load(open("Image_Search/vectors.pkl","rb"))
    paths = pickle.load(open("Image_Search/paths.pkl","rb"))

    # Tinh khoang cach tu search_vector den tat ca cac vector
    distance = np.linalg.norm(vectors - search_vector, axis=1) #là căn bậc hai của tổng bình phương các phần tử của ma trận (duyệt theo phần tử trong vector axis=1)
    # print(distance)
    # Sap xep va lay ra K vector co khoang cach ngan nhat
    K = 6
    ids = np.argsort(distance)[: K]
    print(ids)
    # Tao output
    # nearest_image = [(paths[id], distance[id]) for id in ids]
    nearest_image = [paths[id] for id in ids]
    return nearest_image
    
