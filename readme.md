# Link data: 
[https://drive.google.com/drive/folders/131x8fexwDqoyWqMq4iIEvpWm8FE-EETR](link)
- database để sử dụng cho tìm kiếm: `link/CrawlData_Dogs_Cats` (`images_cat` & `images_dog`)
- database để show trên trang chủ và danh mục sản phẩm: [https://drive.google.com/drive/folders/17SC60cB63BI9_1cw5SwGo3YBYqujCWM0](link)
------------------------------------------------------------------
Vị trí file/folder:
[![Screenshot-2023-01-15-200009.png](https://i.postimg.cc/NFXLPHNW/Screenshot-2023-01-15-200009.png)](https://postimg.cc/K3ZZ1RhN)
---------------------------------------------------------------
# db0.db

## Table: ShopData

### no int

- Đánh số thứ tự.

### id varchar(255)

- Đánh theo mã số của từng thú cưng.

### loai varchar(255)

- Phân loại chó hoặc mèo.

### giong varchar(255)

- Phân loại giống chó/mèo.

### chiTiet text(10000)

- Chi tiết của từng giống chó/mèo.

### gioiTinh varchar(255)

- Giới tính (đực/cái) của từng thú cưng.

### tuoi varchar(255)

- Tuổi của từng thú cưng.

### vacxin varchar(255)

- Tình trạng vắc-xin của từng thú cưng.
