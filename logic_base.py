import shutil
import time
from datetime import timezone, timedelta, datetime
from pathlib import Path
from time import sleep
from typing import Tuple, Dict, List, Callable, Optional

from actions import Action
from devices import DeviceManager
from images import MatchingResult, MatchingRect, Img
from loggers import Logger, KST
from templates import BASE_PATH, TemplateManager
from utils import repeat_retry, ExitRepeatException, ResetRepeatCountException

ORIGIN = 0
GRAY = 1
HSV = 2


class AutoBase:
    food_factory_cache: Dict[Tuple[int, int], bool]  # (offset_y)
    dm: DeviceManager
    log: Logger
    template: TemplateManager
    start_dt: datetime
    img: Tuple[Optional[Img], Optional[Img]]

    def __init__(self, package_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_dt = datetime.now(KST)
        self.dm = DeviceManager(package_name=package_name, scroll_y_size=400)
        self.log = Logger(log_filepath=self.log_filepath())
        self.template = TemplateManager()
        self.img = (None, None)

        self.food_factory_cache = {}

    def log_filepath(self):
        ret = BASE_PATH / 'work' / f'{self.start_dt.strftime("%Y%m%d_%H%M%S")}_log.txt'
        ret.parent.mkdir(exist_ok=True)
        return ret

    def capture_filepath(self):
        dt = datetime.now(KST)
        ret = BASE_PATH / 'work' / self.start_dt.strftime("%Y%m%d_%H%M%S") / f'{dt.strftime("%Y%m%d_%H%M%S")}.png'
        ret.parent.mkdir(exist_ok=True)
        return ret

    def get_click_position(self, action: Action, result: MatchingRect):
        if action.is_click_abs:
            return action.x, action.y
        elif action.is_click_left_top_offset:
            return result.left + action.x, result.top + action.y
        elif action.is_click_left_bottom_offset:
            return result.left + action.x, result.bottom + action.y
        elif action.is_click_right_top_offset:
            return result.right + action.x, result.top + action.y
        elif action.is_click_right_bottom_offset:
            return result.right + action.x, result.bottom + action.y
        elif action.is_click_center:
            return (result.left + result.right) // 2, (result.top + result.bottom) // 2
        return 0, 0

    def do_action(self, act : Action, result: MatchingResult, how_many=-1):
        if act.is_restart:
            self.dm.stop_app()
            sleep(2)
            self.dm.exec_app()
        elif act.is_click:
            cnt = 0
            for ret in result.results:
                cnt += 1
                if 0 <= how_many < cnt:
                    break
                x, y = self.get_click_position(act, ret)
                # self.log.add_log(f'click to x={x}, y={y}, how_many={how_many}')
                self.dm.click(x=x, y=y, hold_duration_ms=act.duration_ms)

    def do_first_action(self, actions: List[Action], result: MatchingResult):
        for action in actions:
            self.do_action(action, result, 1)

    def do_all_actions(self, actions: List[Action], result: MatchingResult):
        for action in actions:
            self.do_action(action, result)
            sleep(0.2)

    def delete_images(self):
        img_path = self.capture_filepath().parent
        if img_path.exists():
            shutil.rmtree(img_path)
        img_path.mkdir(exist_ok=True)

    def screenshot(self, cnt = 1, delete=True):
        ret = []
        for _ in range(cnt):
            sleep(1.1)
            img_filepath1 = self.capture_filepath()
            self.dm.screenshot(img_filepath1)
            ret.append(Img(img_filepath1))
            if delete:
                img_filepath1.unlink()

        self.img = tuple(ret)

    @repeat_retry(repeat=10)
    def _stop_google_ad(self):

        sleep(10)
        self.screenshot()

        actions, result = self.template.get_actions_google_ad_skip(self.img)
        if result:
            self.log.add_log('\t[AD] found Skip button')
            self.do_first_action(actions, result)
            raise ResetRepeatCountException()

        actions, result = self.template.get_actions_google_ad_exit(self.img)
        if result:
            self.log.add_log('\t[AD] found EXIT button')
            self.do_first_action(actions, result)
            raise ResetRepeatCountException()

        if self.template.has_google_ad_miss_click(self.img):
            self.dm.press_back_button()
            raise ExitRepeatException()

        if self.template.has_setup_gear_menu(self.img):
            raise ExitRepeatException()

    def watching_google_ad(self):
        self.dm.click(537, 2199)
        self._stop_google_ad()

    def run(self):
        pass
