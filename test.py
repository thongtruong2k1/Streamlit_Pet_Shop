id = 'database/images_dog/32e8fe0d907b49aebabe7609ee2202aa.jpg'
new_id = id[20:-4]
print(new_id)
name = './Chó/Phốc sóc/0337cd9582f741519112729d59ba7233/51347f5c389640dfaf7c540861fd3438.jpg'
name2 = '0d4e182458f44e3a9304d4be92ba096c'
def get_new_image(image_path):
  count = 0
  for i in range(len(image_path)):
    if image_path[i] == '/':
      count +=1
    if count == 3:
      return i
new_name = f'database/images_cat/{name[15:-37]}.jpg'

import os

for i in os.listdir(".\Chó"):
  print(len(os.listdir(f".\Chó\{i}")))