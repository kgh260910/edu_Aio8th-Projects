from PIL import Image

# ---- 내가 바꾸는 값 ----
PHOTO = "cat.jpg"                # 같은 폴더에 있는 사진 이름

img = Image.open(PHOTO)          # 사진을 연다
print("가로", img.width, "점")
print("세로", img.height, "점")
print("점의 개수", img.width * img.height, "개")
print("색 방식", img.mode)        # RGB = 점마다 빨강·초록·파랑 숫자 3개
