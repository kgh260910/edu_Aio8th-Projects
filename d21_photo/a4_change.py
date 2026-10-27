import numpy as np
from PIL import Image

# ---- 내가 바꾸는 값 ----
PHOTO = "cat.jpg"
AMOUNT = 60                      # 모든 점의 밝기에 더할 숫자 (마이너스면 어두워진다)

gray = np.array(Image.open(PHOTO).convert("L")).astype(int)    # 흑백 숫자표
changed = np.clip(gray + AMOUNT, 0, 255)                        # 더한 뒤 0 ~ 255 밖은 잘라 낸다
result = Image.fromarray(changed.astype(np.uint8))
result.save("changed.jpg")
print("changed.jpg 로 저장했다 : 모든 점에", AMOUNT, "을 더했다")
print("평균 밝기", round(gray.mean(), 1), "→", round(changed.mean(), 1))
result.show()
