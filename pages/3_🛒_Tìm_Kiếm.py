import streamlit as st
import sqlite3
from Image_Extraction import search_image
import requests
from io import StringIO
import pandas as pd
import newtracking
import cv2
from PIL import Image, ImageTk
from st_clickable_images import clickable_images
# import search_image
import base64
from pathlib import Path
import io
st.set_page_config("Animals Store", page_icon="dog", layout="wide")
st.markdown("""<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css" integrity="sha384-xOolHFLEh07PJGoPkLv1IbcEPTNtaed2xpHsD9ESMhqIYd0nLMwNLD69Npy4HI+N" crossorigin="anonymous">""", unsafe_allow_html=True)
session = newtracking.load_model('D:\SearchingByImage1\do_an_streamlit\yolov7-tiny.onnx')
st.markdown("""
<nav class="navbar navbar-expand-lg navbar-light bg-light">
  <a class="navbar-brand" href="/"><img width="200" height="100" src="https://dogily.vn/wp-content/uploads/2020/07/dogily-logo.png" class="header_logo header-logo entered lazyloaded" alt="Dogily Petshop – Bán chó mèo cảnh, thú cưng Tphcm, Hà nội" data-lazy-src="https://dogily.vn/wp-content/uploads/2020/07/dogily-logo.png" data-ll-status="loaded"></a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>

  <div class="collapse navbar-collapse" id="navbarSupportedContent">
    <ul class="navbar-nav mr-auto">
      <li class="nav-item active">
        <a class="nav-link" href="/" rel="nofollow" target="_blank" dir="auto"><b>Home</b> <span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="/Danh_Mục_Sản_Phẩm"><b>Danh Mục Sản Phẩm</b></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="/Tìm_Kiếm"><b>Tìm Kiếm</b></a>
      </li>
    </ul>
  </div>
</nav>
""", unsafe_allow_html=True)

def show_kitty():
    image = requests.get("https://cataas.com/cat").content
    st.image(image)

uploaded_file = st.file_uploader("Choose a file")
import pickle
import numpy as np
# def create_col(value):
#   if value == 1:
#     col1 = st.columns(1)
conn = sqlite3.connect(r"D:\SearchingByImage1\do_an_streamlit\new_database.db")
c=conn.cursor()
def show_label(image_path):
  model = search_image.get_extract_model()
  search_vector = search_image.extract_vector(model, image_path)
  s = pickle.load(open(r"D:\SearchingByImage1\do_an_streamlit\new_vectors.pkl","rb"))
  d = np.array(s)
  vectors=d[:,1]
  vectors=vectors.tolist()
  paths=d[:,0]
  # Tinh khoang cach tu search_vector den tat ca cac vector
  distance = np.linalg.norm(vectors - search_vector, axis=1) #là căn bậc hai của tổng bình phương các phần tử của ma trận (duyệt theo phần tử trong vector axis=1)
  # Sap xep va lay ra K vector co khoang cach ngan nhat
  K = 6
  ids = np.argsort(distance)[: K]
  list_image = []
  list_breed = []
  for id in ids:
    c.execute("SELECT path FROM products where id="+str(id))
    image = c.fetchone()
    c.execute("SELECT breed FROM products where id="+str(id))
    breed = c.fetchone()
    list_image.append(image)
    list_breed.append(breed)
  return list_image, list_breed
  # col1, col2, col3 = st.columns(3)
  # with col1:

def img_to_bytes(img_path):
  img_bytes = Path(img_path).read_bytes()
  encoded_img = base64.b64encode(img_bytes).decode()
  return encoded_img

def write_animals(info, image):
  image_byte = img_to_bytes(image)
  return st.markdown(f"""
          <div class="text-center">
            <a href='http://localhost:8501/Chi_Tiết_Sản_Phẩm/?giong={info[1]}&loai={info[0]}' target="_parent">
                <img src='data:image/jpeg;charset=utf-8;base64,{image_byte}' style='height: 60%; width: 60%; object-fit: contain; border:1px solid black'>
              </a>
            <a href='http://localhost:8501/Chi_Tiết_Sản_Phẩm/?giong={info[1]}&loai={info[0]}' target="_parent">
                <h3 style='text-align: center; color: black; font-size: 30px;'>{info[1]}</h3>
            </a>
          </div>
          """, unsafe_allow_html=True)


i = 0
if uploaded_file is not None:
  path="./"+uploaded_file.name
  images,boxes=newtracking.predict(path,session)
  image = cv2.cvtColor(images,cv2.COLOR_BGR2RGB) #Change cvt Color to original image
  cv2.imwrite('cat_dog_pre.jpg',image)
  st.image('cat_dog_pre.jpg')
  len_box = len(boxes)
  # for i in range(len_box):
  #   col
  list_image = []
  col1, col2, col3 = st.columns(3)
  # for box in boxes:
  while i < len_box:
    if i < len_box:
      if i in [0,3,6]:
        with col1:
          form = st.form(f"my_form{i}")
          image = cv2.imread(path)
          x1, y1, x2, y2 = boxes[i][1:5]
          crop_img = image[y1:y2, x1:x2]
          crop_img = cv2.cvtColor(crop_img,cv2.COLOR_BGR2RGB)
          crop_img = cv2.resize(crop_img,(300,300))
          image_name = f"./images/{i}.jpg"
          cv2.imwrite(image_name, crop_img)
          form.image(crop_img)
          selected = form.form_submit_button("Select")
          if selected:
            list_image, list_breed = show_label(image_name)
          i += 1
    if i < len_box:
      if i in [1,4,7]:
        with col2:
          form = st.form(f"my_form{i}")
          image = cv2.imread(path)
          x1, y1, x2, y2 = boxes[i][1:5]
          crop_img = image[y1:y2, x1:x2]
          crop_img = cv2.cvtColor(crop_img,cv2.COLOR_BGR2RGB)
          crop_img = cv2.resize(crop_img,(300,300))
          image_name = f"./images/{i}.jpg"
          cv2.imwrite(image_name, crop_img)
          form.image(crop_img)
          selected = form.form_submit_button("Select")
          if selected:
            list_image, list_breed = show_label(image_name)
          i += 1
    if i < len_box:
      if i in [2,5,8]:
        with col3:
          form = st.form(f"my_form{i}")
          image = cv2.imread(path)
          x1, y1, x2, y2 = boxes[i][1:5]
          crop_img = image[y1:y2, x1:x2]
          crop_img = cv2.cvtColor(crop_img,cv2.COLOR_BGR2RGB)
          crop_img = cv2.resize(crop_img,(300,300))
          image_name = f"./images/{i}.jpg"
          cv2.imwrite(image_name, crop_img)
          form.image(crop_img)
          selected = form.form_submit_button("Select")
          if selected:
            list_image, list_breed = show_label(image_name)
          i += 1
  if len(list_image) > 0:
    col1, col2 = st.columns(2)
    with col1:
      for i in range(3):
        name_path = "database/"+list_image[i][0]
        if list_image[0][0][7:10] == 'dog':
          write_animals(["Chó",list_breed[i][0]], name_path)
        else:
          write_animals(["Mèo",list_breed[i][0]], name_path)
    with col2:
      for i in range(3,6):
        name_path = "database/"+list_image[i][0]
        if list_image[0][0][7:10] == 'dog':
          write_animals(["Chó",list_breed[i][0]], name_path)
        else:
          write_animals(["Mèo",list_breed[i][0]], name_path)  


st.markdown("""
<script src="https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js" integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.min.js" integrity="sha384-+sLIOodYLS7CIrQpBjl+C7nPvqq+FbNUBDunl/OZv93DB7Ln/533i8e/mZXLi/P+" crossorigin="anonymous"></script>
""", unsafe_allow_html=True)