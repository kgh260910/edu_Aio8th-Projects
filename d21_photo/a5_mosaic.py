from PIL import Image

# ---- 내가 바꾸는 값 ----
PHOTO = "cat.jpg"
N = 20                           # 점 N 개를 한 칸으로 합친다 (클수록 거칠다)

img = Image.open(PHOTO)
small = img.resize((img.width // N, img.height // N))          # 점의 개수를 줄인다
print("줄인 크기", small.width, "x", small.height, "= 점", small.width * small.height, "개 (원래", img.width * img.height, "개)")
big = small.resize(img.size, Image.NEAREST)                    # 같은 크기로 다시 키운다 (네모 칸이 보인다)
big.save("mosaic.jpg")
print("mosaic.jpg 로 저장했다")
big.show()
