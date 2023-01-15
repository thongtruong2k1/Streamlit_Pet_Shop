# import thu vien
import os
from keras.utils import img_to_array
from keras.applications import EfficientNetB0
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
    img = img.resize((224,224))
    img = img.convert("RGB")
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0) # Thêm chiều (số lượng hình ảnh)
    return x

def extract_vector(model, image_path):
    print("Xu ly : ", image_path)
    img = Image.open(image_path)
    img_tensor = image_preprocess(img)

    # Trich dac trung
    vector = model.predict(img_tensor)[0]
    # Chuan hoa vector = chia L2 norm(Khoang cach vector den goc toa do)
    vector = vector / np.linalg.norm(vector)
    return vector



# Dinh nghia thu muc data

data_folder = r"./image_database"

# Khoi tao model
model = get_extract_model()

vectors = []
paths = []

for image_path in os.listdir(data_folder):
    # Noi full path
    image_path_full = os.path.join(data_folder, image_path)
    # Trich dac trung
    image_vector = extract_vector(model, image_path_full)
    # Add dac trung va full path vao list
    vectors.append(image_vector)
    paths.append(image_path_full)


# save vao file
vector_file = "vectors.pkl"
path_file = "paths.pkl"

pickle.dump(vectors, open(vector_file, "wb"))
pickle.dump(paths, open(path_file, "wb"))

