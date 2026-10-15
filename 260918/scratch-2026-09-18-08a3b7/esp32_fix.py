# -*- coding: utf-8 -*-
"""
Thonny + ESP32 (CH340 등) "Device is busy or does not respond" 해결 스크립트 (Windows 전용)

[원인]
Windows의 pyserial은 시리얼 포트를 열 때 DTR/RTS를 자동으로 어서트합니다.
Thonny는 이 값이 설정되지 않으면(None) 아예 건드리지 않고 넘어가므로
(thonny/plugins/micropython/serial_connection.py 참고)
Windows 기본 동작이 그대로 적용됩니다.

ESP32 개발보드의 자동 리셋 회로에서는 DTR/RTS가 EN / GPIO0 핀에 연결되어 있어,
이 신호가 보드를 리셋 상태로 붙잡아 두거나 부트로더 모드로 떨어뜨립니다.
그 결과 REPL이 응답하지 않고 "Device is busy" 오류가 발생합니다.

macOS의 드라이버는 이렇게 동작하지 않기 때문에 같은 보드라도 맥에서는 멀쩡합니다.

[해결]
Thonny 설정 파일에 dtr = False, rts = False 를 넣어 명시적으로 신호를 내려줍니다.
이 옵션은 Thonny GUI에 노출되어 있지 않아 설정 파일을 직접 고쳐야 합니다.
"""

import configparser
import datetime
import os
import shutil
import subprocess
import sys


def line(msg=""):
    print("  " + msg)


def thonny_is_running():
    """Thonny는 종료 시 설정 파일을 통째로 덮어쓰므로 반드시 닫혀 있어야 한다."""
    try:
        out = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq thonny.exe", "/NH"],
            capture_output=True, text=True, errors="ignore",
        ).stdout
        return "thonny.exe" in out.lower()
    except Exception:
        return False   # 확인 불가 시 진행 (백업은 어차피 생성됨)


def main():
    print("")
    line("==========================================")
    line(" ESP32 \"Device is busy\" 오류 수정")
    line("==========================================")
    print("")

    if thonny_is_running():
        line("[!] Thonny가 아직 실행 중입니다.")
        print("")
        line("    Thonny는 종료할 때 설정 파일을 덮어쓰기 때문에,")
        line("    먼저 Thonny 창을 모두 닫아야 합니다.")
        print("")
        line("    Thonny를 닫은 뒤 이 파일을 다시 더블클릭하세요.")
        return 1

    config = os.path.join(os.environ["APPDATA"], "Thonny", "configuration.ini")
    line("설정 파일:")
    line("  " + config)
    print("")

    if not os.path.exists(config):
        line("[!] 설정 파일이 없습니다.")
        print("")
        line("    Thonny를 한 번 실행했다가 완전히 종료한 뒤")
        line("    이 파일을 다시 더블클릭하세요.")
        return 1

    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = config + ".backup_" + stamp
    shutil.copy2(config, backup)
    line("백업 생성: " + os.path.basename(backup))

    # Thonny와 동일한 방식으로 파싱해야 기존 설정이 손상되지 않는다.
    # (thonny/config.py: ConfigParser(interpolation=None), UTF-8)
    ini = configparser.ConfigParser(interpolation=None)
    with open(config, "r", encoding="UTF-8") as fp:
        ini.read_file(fp)

    changed = []
    for section in ("ESP32", "ESP8266"):
        if not ini.has_section(section):
            ini.add_section(section)

        # DTR/RTS를 명시적으로 내려서 보드가 리셋에 묶이지 않게 한다.
        # (bool은 repr로 저장되므로 "False" 문자열이 맞다)
        for key in ("dtr", "rts"):
            old = ini.get(section, key, fallback=None)
            if old != "False":
                ini.set(section, key, "False")
                changed.append("%s.%s : %s -> False" % (section, key, old))

        # 포트 자동 감지. CH340(0x1A86/0x7523), CP210x 등은 Thonny의
        # 알려진 VID/PID 목록에 있으므로 COM 번호가 PC마다 달라도 찾아낸다.
        # (문자열 값은 따옴표 없이 저장된다 - thonny/config.py set_option 참고)
        old = ini.get(section, "port", fallback=None)
        if old != "auto":
            ini.set(section, "port", "auto")
            changed.append("%s.port : %s -> auto (자동 감지)" % (section, old))

    with open(config, "w", encoding="UTF-8") as fp:
        ini.write(fp)

    print("")
    if changed:
        line("변경된 항목:")
        for item in changed:
            line("  " + item)
    else:
        line("이미 올바르게 설정되어 있습니다. (변경 없음)")

    print("")
    line("==========================================")
    line(" 완료! 이제 Thonny를 실행하세요.")
    line("==========================================")
    print("")
    line("* 포트는 Thonny가 자동으로 찾습니다.")
    line("  USB 포트를 바꿔 꽂아도 괜찮습니다.")
    line("")
    line("* 단, 보드 외에 다른 USB 시리얼 장치는")
    line("  빼두세요. 여러 개면 자동 감지가 헷갈립니다.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print("")
        line("[!] 오류가 발생했습니다: %s" % e)
        line("    선생님께 이 화면을 보여주세요.")
        sys.exit(1)