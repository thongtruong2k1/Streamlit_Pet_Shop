import streamlit as st
import sqlite3
import os
import Data_Shop_CatsnDogs
from PIL import Image
import base64
from pathlib import Path

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

placeholder = st.empty()


# Replace the chart with several elements:
with placeholder.container():
  def detail(info):
    return st.markdown(f"""
            <div class="container">
              <div class="text-center">
                <h3 style='text-align: center; font-size: 60px;'>{info[3]}</h3>
                <p style='text-align: center; font-size: 20px;'>
                  <br><b>Loại</b>: {info[2]} <br>
                  <b>Giới tính</b>: {info[5]} <br>
                  <b>Vacxin</b>: {info[7]} <br>
                  <b>Tuổi</b>: {info[6]} </br>
                </p>
                <a class="btn btn-primary" href="https://oa.zalo.me/2174863095751901558" role="button">
                  <span style="color:black; font-weight: bold;">Chat với Dogily</span>
                </a>
                <a href="tel:0965086079" target="_self" class="btn btn-primary">
                  <span style="color:yellow; font-weight: bold;">Hotline: 0965.086.079</span>
                </a>
            </div>
              """, unsafe_allow_html=True)
col1 , col2 = st.columns(2)

httpQuery = st.experimental_get_query_params()
loai = httpQuery["loai"][0]
giong = httpQuery["giong"][0]
id = httpQuery["id"][0]

df = Data_Shop_CatsnDogs.Data_Shop_CatsnDogs()

def create_database():
  list_of_Dogs = df.queryAllDatas("select distinct giong from ShopData where loai='Chó'")
  list_of_Cats = df.queryAllDatas("select distinct giong from ShopData where loai='Mèo'")
  return list_of_Cats, list_of_Dogs

def get_new_image(image_path):
  count = 0
  for i in range(len(image_path)):
    if image_path[i] == '/':
      count +=1
    if count == 3:
      return i

# cho = {loai}
# print(cho)
if loai == "Chó" :
  cho = 1 
else :
  cho = 0
with col1  : 
  parent_dir = f"./{loai}/{giong}"
  image_folder = os.listdir(parent_dir)[0]
  parent_dir += "/" + image_folder
  image_path = parent_dir + "/" + os.listdir(parent_dir)[0]
  loai_pet = 'cat' if loai=='Mèo' else 'dog'
  new_image = f'database/images_{loai_pet}/{id}.jpg'
  image = Image.open(new_image)
  st.image(image, width=400)
  st.markdown("----------------------------------")

with col2 :   
  queryObj = df.queryData(f"select * from ShopData where loai=\'{loai}\' and giong=\'{giong}\';")
  # queryObj2 = df.queryAllDatas(f"select * from ShopData where loai=\'{loai}\'")
  # st.write(queryObj2)
  detail(queryObj)
  st.markdown("----------------------------------")

st.markdown("""
<div class="container section-title-container" style="margin-bottom:0px;">
    <h2 class="section-title section-title-center">
        <b></b>
        <span class="section-title-main" style="font-size:150%;">Các Thú Cưng Cùng Loại</span>
        <b></b>
    </h2>
</div>
""", unsafe_allow_html=True)
def img_to_bytes(img_path):
  img_bytes = Path(img_path).read_bytes()
  encoded_img = base64.b64encode(img_bytes).decode()
  return encoded_img


# @st.experimental_memo
def write_animals(info, image):
  index = get_new_image(image) + 1
  id_image = image[index:-37]
  loai = 'cat' if info[0]=='Mèo' else 'dog'
  new_image = f'database/images_{loai}/{id_image}.jpg'
  image_byte = img_to_bytes(new_image)
  return st.markdown(f"""
          <div class="text-center">
            <a href='http://localhost:8501/Chi_Tiết_Sản_Phẩm/?giong={info[1]}&loai={info[0]}&id={id_image}' target="_parent">
                <img src='data:image/jpeg;charset=utf-8;base64,{image_byte}' style='height: 200px; width: 210px; object-fit: contain; border:1px solid black'>
              </a>
            <a href='http://localhost:8501/Chi_Tiết_Sản_Phẩm/?giong={info[1]}&loai={info[0]}&id={id_image}' target="_parent">
                <h3 style='text-align: center; color: black; font-size: 30px;'>{info[1]}</h3>
            </a>
          </div>
          """, unsafe_allow_html=True)

def write_animals_no_name(id_image):
  loai_eng = 'cat' if loai=='Mèo' else 'dog'
  image_path = f'database/images_{loai_eng}/{id_image}.jpg'
  image_byte_new = img_to_bytes(image_path)
  return st.markdown(f"""
          <div class="text-center">
            <a href='http://localhost:8501/Chi_Tiết_Sản_Phẩm/?giong={giong}&loai={loai}&id={id_image}' target="_parent">
                <img src='data:image/jpeg;charset=utf-8;base64,{image_byte_new}' style='height: 200px; width: 210px; object-fit: contain; border:1px solid black'>
              </a>
          </div>
          """, unsafe_allow_html=True)

def create_details(list_of_Cats, list_of_Dogs):
  ob_dog = []
  ob_cat = []
  for i in range(len(list_of_Dogs)):
    if i <= 10:
      ob_dog.append(df.queryData(f"select * from ShopData where loai='Chó' and giong='{list_of_Dogs[i][0]}'"))
      ob_cat.append(df.queryData(f"select * from ShopData where loai='Mèo' and giong='{list_of_Cats[i][0]}'"))
    else:
      ob_dog.append(df.queryData(f"select * from ShopData where loai='Chó' and giong='{list_of_Dogs[i][0]}'"))
  return ob_dog, ob_cat

list_theo_giong = os.listdir(f".\{loai}\{giong}")
col1, col2, col3, col4, col5 = st.columns(5)
if len(list_theo_giong) <= 5:
  try:
    with col1:
      id_image = list_theo_giong[0]
      write_animals_no_name(id_image)
      st.markdown("----------------------------------")
    with col2:
      id_image = list_theo_giong[1]
      write_animals_no_name(id_image)
      st.markdown("----------------------------------")
    with col3:
      id_image = list_theo_giong[2]
      write_animals_no_name(id_image)
      st.markdown("----------------------------------")
    with col4:
      id_image = list_theo_giong[3]
      write_animals_no_name(id_image)
      st.markdown("----------------------------------")
    with col5:
      id_image = list_theo_giong[4]
      write_animals_no_name(id_image)
      st.markdown("----------------------------------")
  except:
    pass
else:
  try:
    with col1:
      for i in [0,6]:
          id_image = list_theo_giong[i]
          write_animals_no_name(id_image)
          st.markdown("----------------------------------")
    with col2:
      for i in [1,7]:
          id_image = list_theo_giong[i]
          write_animals_no_name(id_image)
          st.markdown("----------------------------------")
    with col3:
      for i in [2,8]:
          id_image = list_theo_giong[i]
          write_animals_no_name(id_image)
          st.markdown("----------------------------------")
    with col4:
      for i in [3,9]:
          id_image = list_theo_giong[i]
          write_animals_no_name(id_image)
          st.markdown("----------------------------------")
    with col5:
      for i in [4,10]:
          id_image = list_theo_giong[i]
          write_animals_no_name(id_image)
          st.markdown("----------------------------------")
  except:
    pass
print("=================")

st.markdown(f"""
<div class="container section-title-container" style="margin-bottom:0px;">
    <h2 class="section-title section-title-center">
        <b></b>
        <span class="section-title-main" style="font-size:150%;">Các Giống {loai} Khác</span>
        <b></b>
    </h2>
</div>
""", unsafe_allow_html=True)
list_of_Cats, list_of_Dogs = create_database()
ob_dog, ob_cat = create_details(list_of_Cats, list_of_Dogs)

def create_pet_image(ob, list_of_pet, loai_pet):
  temp = (giong,)
  index = list_of_pet.index(temp)
  ob.pop(index)
  with col1:
    for i in range(0,2):
        parent_dir = f"./{loai_pet}/{list(ob[i])[3]}"
        image_folder = os.listdir(parent_dir)[0]
        parent_dir += "/" + image_folder
        image_path = parent_dir + "/" + os.listdir(parent_dir)[0]
        write_animals(list(ob[i])[2:4], image_path)
        st.markdown("----------------------------------")
  with col2:
    for i in range(2,4):
        parent_dir = f"./{loai_pet}/{list(ob[i])[3]}"
        image_folder = os.listdir(parent_dir)[0]
        parent_dir += "/" + image_folder
        image_path = parent_dir + "/" + os.listdir(parent_dir)[0]
        write_animals(list(ob[i])[2:4], image_path)
        st.markdown("----------------------------------")
  with col3:
    for i in range(4,6):
        parent_dir = f"./{loai_pet}/{list(ob[i])[3]}"
        image_folder = os.listdir(parent_dir)[0]
        parent_dir += "/" + image_folder
        image_path = parent_dir + "/" + os.listdir(parent_dir)[0]
        write_animals(list(ob[i])[2:4], image_path)
        st.markdown("----------------------------------")
  with col4:
    for i in range(6,8):
        parent_dir = f"./{loai_pet}/{list(ob[i])[3]}"
        image_folder = os.listdir(parent_dir)[0]
        parent_dir += "/" + image_folder
        image_path = parent_dir + "/" + os.listdir(parent_dir)[0]
        write_animals(list(ob[i])[2:4], image_path)
        st.markdown("----------------------------------")
  with col5:
    for i in range(8,10):
        parent_dir = f"./{loai_pet}/{list(ob[i])[3]}"
        image_folder = os.listdir(parent_dir)[0]
        parent_dir += "/" + image_folder
        image_path = parent_dir + "/" + os.listdir(parent_dir)[0]
        write_animals(list(ob[i])[2:4], image_path)
        st.markdown("----------------------------------")

col1, col2, col3, col4, col5 = st.columns(5)

if cho == 1:
  create_pet_image(ob_dog, list_of_Dogs, 'Chó')
else:
  create_pet_image(ob_cat, list_of_Cats, 'Mèo')

# test = df.queryAllDatas("select * from ShopData where id='179132fbe27c4f3c8eab5a547d51a6d3'")
# st.write(test)

st.markdown("""
<script src="https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js" integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.min.js" integrity="sha384-+sLIOodYLS7CIrQpBjl+C7nPvqq+FbNUBDunl/OZv93DB7Ln/533i8e/mZXLi/P+" crossorigin="anonymous"></script>
""", unsafe_allow_html=True)