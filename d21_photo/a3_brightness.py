import numpy as np
from PIL import Image

# ---- 내가 바꾸는 값 : 비교할 사진들 ----
PHOTOS = ["street.jpg", "cat.jpg", "dog.jpg", "desk.jpg", "fruit.jpg", "moto.jpg", "drone.jpg", "zoo.jpg"]

for name in PHOTOS:
    gray = np.array(Image.open(name).convert("L"))     # 사진 전체의 흑백 숫자표
    average = gray.mean()                               # 모든 점의 평균 밝기 (0 ~ 255)
    print(f"{name:12s} 평균 밝기 {average:6.1f}  가장 어두운 점 {gray.min():3d}  가장 밝은 점 {gray.max():3d}")
