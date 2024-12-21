import io
import time
from pathlib import Path
from time import sleep

from PIL import Image
from adbutils import AdbClient
from ppadb.client import Client as AdbClient
from ppadb.device import Device

from PIL import ImageFile

from utils import repeat_retry, ExitRepeatException

ImageFile.LOAD_TRUNCATED_IMAGES = True

class DeviceManager:

    package_name: str
    client: AdbClient
    device: Device

    scroll_y_size: int

    def __init__(self, package_name, scroll_y_size, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_y_size = scroll_y_size
        self.package_name = package_name
        self.client = None
        self.device = None

    def is_running(self) -> bool:
        self.init_adb()
        output = self.device.shell("ps")  # ps 명령어 실행하여 프로세스 리스트 가져오기
        return self.package_name in output

    def is_screen_on(self):
        self.init_adb()
        result = self.device.shell("dumpsys power | grep 'mWakefulness'")
        return "mWakefulness=Awake" in result

    def is_locked(self):
        self.init_adb()
        result = self.device.shell("dumpsys window | grep mDreamingLockscreen")
        return "mDreamingLockscreen=true" in result

    def wake_up_device(self):
        self.init_adb()
        #
        if not self.is_screen_on():
            print("Screen is OFF. Waking up the device.")
            self.device.shell("input keyevent KEYCODE_POWER")
        else:
            print("Screen is already ON.")

        if self.is_locked():
            print("Device is locked. Unlocking...")
        else:
            print("Device is already unlocked.")

    def exec_app(self):
        self.init_adb()

        activity_name = f"{self.package_name}/com.unity3d.player.UnityPlayerActivity"
        self.device.shell(f"am start -n {activity_name}")
        sleep(5)

    def stop_app(self):
        self.init_adb()
        self.device.shell(f"am force-stop {self.package_name}")

    def click(self, x, y, hold_duration_ms=300):
        self.init_adb()
        self.device.input_swipe(x, y, x, y, int(hold_duration_ms))

    @repeat_retry(3)
    def screenshot(self, out_filepath: Path):
        self.init_adb()
        self.device.shell("input text 1")
        screenshot = self.device.screencap()

        # 캡처된 화면 데이터를 이미지로 변환
        image = Image.open(io.BytesIO(screenshot))
        image.save(out_filepath, format="PNG")
        raise ExitRepeatException()

    def init_adb(self):
        # ADB 클라이언트 연결
        if not self.client:
            self.client = AdbClient(host="127.0.0.1", port=5037)

        # 연결된 디바이스 가져오기
        if not self.device:
            devices = self.client.devices()
            if not devices:
                raise Exception('Not found devices')

            self.device = devices[0] if isinstance(devices, list) else devices

    def start_app(self):
        self.wake_up_device()

        if not self.is_running():
            self.exec_app()

    SCROLL_MIN_Y_POS = 360
    SCROLL_MAX_Y_POS = 2100
    SCROLL_X_POS = 500

    def move_to_top(self):
        self.init_adb()
        for _ in range(5):
            self.device.input_swipe(self.SCROLL_X_POS, self.SCROLL_MIN_Y_POS, self.SCROLL_X_POS, self.SCROLL_MAX_Y_POS, int(500))
            time.sleep(0.5)

    def move_to_bottom(self):
        self.init_adb()
        for _ in range(5):
            self.device.input_swipe(self.SCROLL_X_POS, self.SCROLL_MAX_Y_POS, self.SCROLL_X_POS, self.SCROLL_MIN_Y_POS, int(500))
            time.sleep(0.5)

    def swipe(self, sx, sy, ex, ey, duration_ms = 500):
        self.init_adb()
        self.device.input_swipe(sx, sy, ex, ey, int(duration_ms))
        sleep(0.5)


    def move_to_down_1step(self):
        self.init_adb()
        self.device.input_swipe(self.SCROLL_X_POS, self.SCROLL_MAX_Y_POS, self.SCROLL_X_POS, self.SCROLL_MAX_Y_POS - self.scroll_y_size, int(500))
        sleep(1)

    def move_to_down_2step(self):
        self.move_to_down_1step()
        self.move_to_down_1step()

    def move_to_down_3step(self):
        self.move_to_down_2step()
        self.move_to_down_1step()

    def move_to_up_1step(self):
        self.init_adb()
        self.device.input_swipe(self.SCROLL_X_POS, self.SCROLL_MAX_Y_POS - self.scroll_y_size, self.SCROLL_X_POS, self.SCROLL_MAX_Y_POS , int(500))
        sleep(1)

    def press_back_button(self):
        self.init_adb()
        self.device.shell("input keyevent 4")  # KEYCODE_BACK