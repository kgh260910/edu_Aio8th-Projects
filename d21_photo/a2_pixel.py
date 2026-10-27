from PIL import Image

# ---- 내가 바꾸는 값 ----
PHOTO = "cat.jpg"
X = 300                          # 가로로 몇 번째 점 (0 부터)
Y = 200                          # 세로로 몇 번째 점 (0 부터)

img = Image.open(PHOTO)
r, g, b = img.getpixel((X, Y))   # 이 점의 빨강·초록·파랑 숫자
print("점", (X, Y), "의 색 : 빨강", r, "초록", g, "파랑", b)

gray = img.convert("L")          # 흑백 사진으로 바꾼다 (점마다 숫자 하나, 0 ~ 255)
print("같은 점의 흑백 밝기 :", gray.getpixel((X, Y)))

print("이 점 주변 5 x 5 칸의 흑백 밝기 :")
for dy in range(5):
    row = []
    for dx in range(5):
        row.append(gray.getpixel((X + dx, Y + dy)))
    print(row)
