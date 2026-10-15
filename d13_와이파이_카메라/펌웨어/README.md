# ESP32-CAM 카메라 포함 MicroPython 펌웨어

- 파일: `firmware_AI_THINKER_mpy1.27.0.bin` (1,808,576 바이트)
- 출처: https://github.com/cnadler86/micropython-camera-API/releases (v0.6.2, 2026-01-12) 의 `mpy_cam-v1.27.0-AI_THINKER.zip` 안 `firmware.bin` 을 그대로 옮겼다.
- 기반: MicroPython 1.27.0, 빌드 `ESP32_GENERIC-SPIRAM`, 카메라 모듈 `camera` 포함.
- 올리는 주소: **0x1000** (Thonny 의 Target address 기본값이 ESP32 에서는 0x1000)
- 강사 보드 실측(2026-10-08): 부팅 → `import camera` 성공 → JPEG 사진 · Wi-Fi 웹 서버 스트리밍 · 블루투스 모두 동작.
- 원래(일반) 펌웨어로 되돌리려면 `펌웨어_원복.bat` 더블클릭. 올라가는 파일은 `esp32_generic_mpy1.29.0.bin` (MicroPython 공식 `ESP32_GENERIC-20260824-v1.29.0.bin`, 1,790,544 바이트, 주소 0x1000).
- 원복 실측(2026-10-11, 맥북 + ESP32-CAM-MB): 같은 esptool 명령(`--erase-all -z 0x1000`, 460800 baud)으로 지우기 13.3초 → 쓰기 32.5초 → `Hash of data verified.` → 부팅 줄 `MicroPython v1.29.0 ... Generic ESP32 module with ESP32`(SPIRAM 없음), `import camera` 는 `ImportError`.
- `펌웨어_원복.bat` 은 윈도우 PC 에서 아직 실행해 보지 않았다(굽기 bat 와 파일 이름·문구만 다르다).
- **맥북**: 같은 폴더의 `펌웨어_굽기.command` / `펌웨어_원복.command` 를 Finder 에서 더블클릭한다(Thonny 의 파이썬·esptool 5.2.0 사용, 포트 자동 탐지). 실측(2026-10-13, 맥북 + ESP32-CAM-MB): 굽기 지우기 13.2초 → 쓰기 30.4초 → `Hash of data verified.`, 원복 13.2초 → 33.0초 → 검증, 원복 뒤 `import camera` 는 `ImportError`. 처음 열 때 "확인되지 않은 개발자" 경고가 뜨면 오른쪽 버튼 → 열기(다른 맥에서는 미확인). 실행 권한이 없으면 터미널에서 `chmod +x 펌웨어_*.command`.

## 지원 카메라 센서 (2026-10-15 수업 중 확인)
- **OV2640 모듈만 쓴다.** 강사 보드 실측과 같은 기본 모듈이다.
- **OV3660 모듈은 `Camera(pixel_format=PixelFormat.JPEG, ...)` 줄에서 `OSError: Failed to capture initial frame` 로 멈춘다.** 학생 여러 명이 같은 증상이었고, 카메라 모듈만 OV2640 으로 바꾸자 해결됐다.
- 드라이버 이슈와 일치: https://github.com/cnadler86/micropython-camera-API/issues/55 (OV3660·OV5640 JPEG 실패, 드라이버 6.0.0 은 정상·6.0.1 이후 실패 보고, 1.27.0/0.6.2 에서도 재현, 미해결). 원인·수정은 확인되지 않았다.
- 센서 이름을 읽는 파이썬 API 는 README 에 없다. 렌즈 몸통에 인쇄된 글자(OV2640 / OV3660)로 구분한다.
- 수업 전에 보드마다 `c1_cam_capture.py` 를 한 번 돌려 걸러 내면 30초면 된다.
- 미확인: 드라이버 0.6.0·0.5.0 펌웨어에서 OV3660 이 되는지.
