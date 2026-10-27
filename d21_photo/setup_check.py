"""D21 설치 점검 : OK 5개면 통과.  PyCharm 에서 이 파일을 두 번 눌러 열고 실행한다"""
import sys
import platform

print("=" * 44)
print("내 PC 점검 (사진 다루기 준비)")
print("=" * 44)
ok_count = 0

def result(no, title, ok, detail):
    global ok_count
    if ok:
        ok_count += 1
    print(f"[{no}] {'OK  ' if ok else 'FAIL'} {title} : {detail}")

# 1) 파이썬 버전
v = sys.version_info
result(1, "파이썬 버전", (v.major, v.minor) >= (3, 9), f"{v.major}.{v.minor}.{v.micro} (3.9 이상이면 된다)")

# 2) 운영체제
result(2, "운영체제", True, f"{platform.system()} {platform.release()}")

# 3) numpy (숫자표를 다루는 도구)
try:
    import numpy as np
    result(3, "numpy", True, f"버전 {np.__version__}")
except Exception as e:
    np = None
    result(3, "numpy", False, f"{type(e).__name__} : 도구 관리에서 numpy 를 설치하세요")

# 4) Pillow (사진을 여는 도구)
try:
    from PIL import Image
    import PIL
    result(4, "Pillow", True, f"버전 {PIL.__version__}")
except Exception as e:
    Image = None
    result(4, "Pillow", False, f"{type(e).__name__} : 도구 관리에서 pillow 를 설치하세요")

# 5) 사진 한 장 열어 보기
if Image is not None:
    try:
        img = Image.open("street.jpg")
        result(5, "사진 열기", True, f"street.jpg 의 크기 {img.width} x {img.height}")
    except Exception as e:
        result(5, "사진 열기", False, f"{type(e).__name__} : street.jpg 가 이 파일과 같은 폴더에 있어야 한다")
else:
    result(5, "사진 열기", False, "4번이 먼저 OK 여야 한다")

print("=" * 44)
print(f"통과 {ok_count} / 5")
print("모두 OK : 오늘 실습을 이어가면 된다" if ok_count == 5 else "FAIL 줄의 설명을 먼저 해결하세요 (막힐 때 표 참고)")
