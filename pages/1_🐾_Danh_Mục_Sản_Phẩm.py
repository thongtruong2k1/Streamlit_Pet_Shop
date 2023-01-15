import streamlit as st
import sqlite3
from sqlite3 import Error
import Data_Shop_CatsnDogs
import os
from PIL import Image
import base64
from pathlib import Path
print("=========================")
st.set_page_config("Animals Store", page_icon="dog", layout="wide")
st.markdown("""<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css" integrity="sha384-xOolHFLEh07PJGoPkLv1IbcEPTNtaed2xpHsD9ESMhqIYd0nLMwNLD69Npy4HI+N" crossorigin="anonymous">""", unsafe_allow_html=True)

st.markdown("""
<nav class="navbar navbar-expand-lg navbar-light bg-light">
  <a class="navbar-brand" href="/"><img width="200" height="100" src="https://dogily.vn/wp-content/uploads/2020/07/dogily-logo.png" class="header_logo header-logo entered lazyloaded" alt="Dogily Petshop – Bán chó mèo cảnh, thú cưng Tphcm, Hà nội" data-lazy-src="https://dogily.vn/wp-content/uploads/2020/07/dogily-logo.png" data-ll-status="loaded"></a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>

  <div class="collapse navbar-collapse" id="navbarSupportedContent">
    <ul class="navbar-nav mr-auto">
      <li class="nav-item active">
        <a class="nav-link" href="/" target="_parent"><b>Home</b> <span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="/Danh_Mục_Sản_Phẩm" target="_parent"><b>Danh Mục Sản Phẩm</b></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="/Tìm_Kiếm" target="_parent"><b>Tìm Kiếm</b></a>
      </li>
    </ul>
  </div>
</nav>
""", unsafe_allow_html=True)

tab1, tab2= st.tabs(["Dog", "Cat"])

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

def create_database():
  df = Data_Shop_CatsnDogs.Data_Shop_CatsnDogs()
  list_of_Dogs = df.queryAllDatas("select distinct giong from ShopData where loai='Chó'")
  list_of_Cats = df.queryAllDatas("select distinct giong from ShopData where loai='Mèo'")  
  ob_dog = []
  ob_cat = []
  for i in range(len(list_of_Dogs)):
    if i < len(list_of_Cats):
      ob_dog.append(df.queryData(f"select * from ShopData where loai='Chó' and giong='{list_of_Dogs[i][0]}'"))
      ob_cat.append(df.queryData(f"select * from ShopData where loai='Mèo' and giong='{list_of_Cats[i][0]}'"))
    else:
      ob_dog.append(df.queryData(f"select * from ShopData where loai='Chó' and giong='{list_of_Dogs[i][0]}'"))
  return list_of_Cats, list_of_Dogs, ob_dog, ob_cat


list_of_Cats, list_of_Dogs, ob_dog, ob_cat = create_database()
# st.write(detail_Cats)

with tab1:
    st.header("Chọn loại chó mà bạn thích")
    
    col1, col2 = st.columns(2)
    with col1:
        for i in range(0,int(len(list_of_Dogs) /2)):
          parent_dir = f"./Chó/{list(ob_dog[i])[3]}"
          image_folder = os.listdir(parent_dir)[0]
          parent_dir += "/" + image_folder
          image_path = parent_dir + "/" + os.listdir(parent_dir)[0]
          write_animals(list(ob_dog[i])[2:4], image_path)
          st.markdown("----------------------------------")

    with col2:
      for i in range(int(len(list_of_Dogs) /2),len(list_of_Dogs)):
        parent_dir = f"./Chó/{list(ob_dog[i])[3]}"
        image_folder = os.listdir(parent_dir)[0]
        parent_dir += "/" + image_folder
        image_path = parent_dir + "/" + os.listdir(parent_dir)[0]
        write_animals(list(ob_dog[i])[2:4], image_path)
        st.markdown("----------------------------------")

with tab2:
    st.header("Chọn loại mèo mà bạn thích")
    
    col1, col2 = st.columns(2)
    with col1:
        for i in range(0,int(len(list_of_Cats) /2) + 1):
          parent_dir = f"./Mèo/{list(ob_cat)[i][3]}"
          image_folder = os.listdir(parent_dir)[0]
          parent_dir += "/" + image_folder
          image_path = parent_dir + "/" + os.listdir(parent_dir)[0]
          write_animals(list(ob_cat)[i][2:4], image_path)
          st.markdown("----------------------------------")

    with col2:
        for i in range(int(len(list_of_Cats) /2) + 1,len(list_of_Cats)):
          parent_dir = f"./Mèo/{list(ob_cat)[i][3]}"
          image_folder = os.listdir(parent_dir)[0]
          parent_dir += "/" + image_folder
          image_path = parent_dir + "/" + os.listdir(parent_dir)[0]
          write_animals(list(ob_cat)[i][2:4], image_path)
          st.markdown("----------------------------------")

st.markdown("""
<script src="https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js" integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.min.js" integrity="sha384-+sLIOodYLS7CIrQpBjl+C7nPvqq+FbNUBDunl/OZv93DB7Ln/533i8e/mZXLi/P+" crossorigin="anonymous"></script>
""", unsafe_allow_html=True)