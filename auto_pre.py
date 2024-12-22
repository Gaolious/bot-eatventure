import math
import random
import shutil
from time import sleep
from typing import Tuple, List, Dict

from cities import CityManager
from images import Img
from logic_base import AutoBase
from templates import BASE_PATH
from utils import repeat_retry, ExitRepeatException, ResetRepeatCountException

ORIGIN = 0
GRAY = 1
HSV = 2


class AutoHelper(AutoBase):
    city: CityManager

    max_level: int
    name: str
    factory_info: List[Dict]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.city = CityManager()
        self.max_level = 0
        self.name = ''
        self.factory_info = []

    def open_map(self):
        self.dm.click(x=100, y=2200)
        sleep(0.3)

    def open_map_250(self):
        self.dm.click(x=191, y=672)
        sleep(0.3)

    def close_map(self):
        self.dm.click(x=884, y=671)
        sleep(0.3)

    def close_map_250(self):
        self.dm.click(x=1000, y=200)
        sleep(0.3)

    def active_skill_select_last(self):
        """

        :return:
        """
        boxes = [
            [
                {'xy': (220, 1022), 'size': (200, 195)},
                {'xy': (440, 1022), 'size': (200, 195)},
                {'xy': (660, 1022), 'size': (200, 195)},
            ],
            [
                {'xy': (220, 1240), 'size': (200, 195)},
                {'xy': (440, 1240), 'size': (200, 195)},
                {'xy': (660, 1240), 'size': (200, 195)},
            ],
        ]
        scroll_s = (540, 1530)
        scroll_e = (540, 1020)

        self.screenshot()
        actions, result = self.template.get_actions_active_skill_select_button(self.img)
        if result:
            self.log.add_log('\t[O] Choose Active Skill (for last factory)')
            self.do_all_actions(actions, result)
            factory_count = max(0, len(self.factory_info) - 1)
            rows = factory_count // 3
            cols = factory_count % 3

            if rows >= 2:
                self.dm.swipe(scroll_s[0], scroll_s[1], scroll_e[0], scroll_e[1])
                sleep(0.3)

            row = 1 if rows >= 1 else 0
            col = cols
            x, y = boxes[row][col]['xy']
            w, h = boxes[row][col]['size']
            x += w//2
            y += h//2
            self.dm.click(x=x, y=y)
            sleep(0.3)
            self.do_all_actions(actions, result)

    def open_active_skill(self):
        self.dm.click(x=540, y=270)  # black circle
        sleep(0.3)

        self.active_skill_select_last()

        self.dm.click(x=900, y=890)  # red-white X
        sleep(0.3)

    def save_to_map(self, max_level, name, is_completed):
        self.dm.move_to_top()

        if max_level == 250:
            self.open_map()
            self.open_map_250()
            self.dm.move_to_top()
            for i in range(4):
                img_filepath = BASE_PATH / 'images' / 'maps' / str(max_level) / f'{max_level:03d}_{name}' / f'map_250_{i}.png'
                img_filepath.parent.mkdir(exist_ok=True)
                self.dm.screenshot(img_filepath)
                self.dm.move_to_down_1step()
                self.log.add_log(f'capture image : {img_filepath}')

            self.close_map_250()
            self.close_map()

        if not is_completed:
            img_filepath = BASE_PATH / 'images' / 'maps' / str(max_level) / f'{max_level:03d}_{name}' / f'map.png'
            img_filepath.parent.mkdir(exist_ok=True)
            self.open_map()
            self.dm.screenshot(img_filepath)
            self.close_map()

            self.log.add_log(f'capture image : {img_filepath}')

        offset = 0
        factory_opened = False
        for p in range(10):
            if is_completed:
                img_filepath = BASE_PATH / 'images' / 'maps' / str(max_level) / f'{max_level:03d}_{name}' / f'top_{offset:04d}_completed.png'
            else:
                img_filepath = BASE_PATH / 'images' / 'maps' / str(max_level) / f'{max_level:03d}_{name}' / f'top_{offset:04d}.png'

            img_filepath.parent.mkdir(exist_ok=True)

            self.log.add_log(f'capture image : {img_filepath}')
            self.dm.screenshot(img_filepath)
            if not factory_opened:
                img = Img(img_filepath)
                factory_arrows = img.get_pos_upgrade_arrow(factory_only=True)
                if factory_arrows:
                    x, y = factory_arrows[0]
                    self.dm.click(x, y)
                    self.screenshot()
                    actions, result = self.template.get_actions_buy_food_factory_coin(self.img)
                    if result:
                        self.do_first_action(actions, result)
                    factory_opened = True

            offset += self.dm.scroll_y_size
            self.dm.move_to_down_1step()

    def get_level_city(self) -> Tuple[int, str]:
        max_level = 0
        name = ''

        self.open_map()
        try:
            self.screenshot()

            if self.template.has_maximum_level_250(self.img):
                max_level = 250
            elif self.template.has_maximum_level_150(self.img):
                max_level = 150
            elif self.template.has_maximum_level_75(self.img):
                max_level = 75
            elif self.template.has_maximum_level_50(self.img):
                max_level = 50
            elif self.template.has_maximum_level_25(self.img):
                max_level = 25
            else:
                return max_level, name

            if max_level == 250:
                self.open_map_250()
                self.dm.move_to_top()
                self.screenshot()

            name = self.city.find_city(max_level=max_level, capture_image=self.img)

            if max_level == 250:
                self.close_map_250()

            return max_level, name
        finally:
            self.close_map()

    sx, sy, ex, ey = 0, 0, 0, 0
    curr_offset_y = 0
    curr_factory_x = 0
    curr_factory_y = 0
    curr_factory_offset = 0

    def init_screen_pos(self):
        self.log.add_log('\t[O] init_screen_pos')
        self.curr_offset_y = 0
        self.dm.move_to_top()

    def init_factory_pos(self, sx, sy, ex, ey, offset):
        self.sx, self.sy, self.ex, self.ey = sx, sy, ex, ey
        x, y = (sx+ex)//2, (sy+ey)//2
        self.log.add_log(f'\t[O] init_factory_pos x={x}, y={y}, offset={offset}')
        self.curr_factory_x = x
        self.curr_factory_y = y
        self.curr_factory_offset = offset

    def adjust_factory_offset(self, open_box=False):

        self.log.add_log(f'\t[O] adjust_factory_offset current offset={self.curr_offset_y}, factory offset={self.curr_factory_offset}')
        if self.curr_offset_y > self.curr_factory_offset:
            self.init_screen_pos()

        while self.curr_offset_y < self.curr_factory_offset:
            self.log.add_log(f'[adjust_factory_offset] : {self.curr_offset_y} -> {self.curr_offset_y+1} / Scroll Down')
            self.curr_offset_y += 1
            self.dm.move_to_down_1step()
            if open_box:
                self.open_boxes()

    # Step 3. open boxes, upgrade skills
    def open_boxes(self):
        self.screenshot()
        boxes = self.img[0].get_boxes()
        if boxes:
            for boxx, boxy in boxes:
                self.log.add_log(f'\t[O] Open Box {boxx}, {boxy}')
                self.dm.click(boxx, boxy)

        else:
            self.log.add_log('\t[X] BOX Open')

    # Step 3. open boxes, upgrade skills
    def open_upgrade_skill(self):
        self.screenshot()
        key = self.template.UPGRADE_SKILL_BUTTON
        skill_arrows = self.img[0].get_pos_upgrade_arrow(factory_only=False)
        if skill_arrows or random.randint(0,3) == 0:
            self.log.add_log('\t[O] Skill Upgrade')
            for act in self.template.templates[key]['actions']:
                self.dm.click(act.x, act.y, 80)
        else:
            self.log.add_log('\t[X] Skill Upgrade')


    def open_boxes_and_upgrade_skill(self):
        self.open_upgrade_skill()
        self.open_boxes()

    def do_upgrade_factory_upgrade(self, max_level, with_box_open, is_last, cnt):
        functions = [
            self.template.get_actions_upgrade_coin_active,
            self.template.get_actions_upgrade_coin_deactive,
        ]

        for fn in functions:
            actions, result = fn(self.img)
            if result:
                repeat = 1
                if not with_box_open:
                    repeat = math.ceil(max_level / 50)

                self.log.add_log(f'\t[O] Upgrade Repeat = {repeat} / {fn.__name__}')
                self.do_first_action(actions, result, duration_multiply=repeat)

                if is_last and 2 == cnt[0]:
                    self.open_active_skill()

                self.screenshot()
                self.dm.click(x=self.curr_factory_x, y=self.curr_factory_y)

                if self.template.has_reach_to_maximum_upgrade(self.img):
                    self.log.add_log('\t[O] 업글 완료')
                    raise ExitRepeatException()

                if with_box_open:
                    self.open_boxes_and_upgrade_skill()
                raise ResetRepeatCountException()

        self.log.add_log(f'\t[X] Not found coin.')

    def do_upgrade_factory_unlock(self, with_box_open):
        self.log.add_log('\t[do_upgrade_factory_unlock]')
        actions, result = self.template.get_actions_buy_food_factory_coin(self.img)
        if result:
            self.do_first_action(actions, result)
            if with_box_open:
                self.open_boxes_and_upgrade_skill()
            raise ResetRepeatCountException()

    def is_factory_opened(self):
        ret = self.template.has_upgrade_coin_active(self.img)
        ret = ret or self.template.has_upgrade_coin_deactive(self.img)
        ret = ret or self.template.has_reach_to_maximum_upgrade(self.img)
        ret = ret or self.template.has_unlock_factory_text(self.img)
        return ret

    def adjust_factory_position(self):
        self.screenshot()
        factory_arrows = self.img[0].get_pos_upgrade_arrow(factory_only=True, tolerance=20)
        min_dist = -1
        tx, ty = 0, 0
        self.log.add_log(f'\t[Adjust Factory Position] start')

        lx, rx = self.sx - 20, (self.sx + self.ex) // 2

        for x, y in factory_arrows:
            if not ( lx <= x <= rx ):
                continue

            d = abs(y - self.sy)
            if min_dist < 0 or min_dist > d:
                min_dist = d
                tx, ty = x, y + 37  # distance between [center of arrow], [top of box] = 37

        if min_dist >= 0 and min_dist < 400:
            self.log.add_log(f'\t[Adjust Factory Position] ({self.sx},{self.sy}) - ({self.ex},{self.ey}) / Arrow : ({tx},{ty})')
            self.dm.swipe(self.sx, ty, self.sx, self.sy, 1000)

        self.log.add_log(f'\t[Adjust Factory Position] end')

    @repeat_retry(repeat=2)
    def click_factory(self, tobe_open=True):
        if not tobe_open:
            self.dm.click(x=1, y=309)
        else:
            self.screenshot()
            if self.is_factory_opened() != tobe_open:
                self.log.add_log(f'\t[click_factory] is_factory_opened={not tobe_open}. Try to click factory. x={self.curr_factory_x}, y={self.curr_factory_y}')
                self.dm.click(x=self.curr_factory_x, y=self.curr_factory_y)
                self.screenshot()

            if self.is_factory_opened() == tobe_open:
                raise ExitRepeatException()
            else:
                self.adjust_factory_position()

    @repeat_retry(repeat=2)
    def do_upgrade_factory_open(self, max_level, with_box_open, is_last, cnt):
        try:
            self.log.add_log(f'[do_upgrade_factory_open] / with_box_open={with_box_open}')
            if with_box_open:
                actions, result = self.template.get_actions_google_ad_timer(self.img)
                if not result:
                    self.log.add_log('\t[O] Google adv')
                    # upgrade window off
                    self.watching_google_ad()
                    self.init_screen_pos()
                    self.adjust_factory_offset(with_box_open)

            if not self.click_factory(tobe_open=True):
                self.log.add_log('\tExit. do_upgrade_factory_open / Not Found click_factory ')
                return

            ### click
            if self.template.has_go_to_next_stage(self.img):
                self.log.add_log('\tExit. do_upgrade_factory_open / 다음 stage로 이동')
                raise ExitRepeatException()
            else:
                self.log.add_log('\t[X] has_go_to_next_stage')

            if self.template.has_reach_to_maximum_upgrade(self.img):
                self.log.add_log('\t[O] 업글 완료')
                self.click_factory(tobe_open=False)
                raise ExitRepeatException()
            else:
                self.log.add_log('\t[X] has_reach_to_maximum_upgrade')

            if self.template.has_unlock_factory_text(self.img):
                # 처음 open
                self.log.add_log('\t[O] 잠금 해제')
                self.do_upgrade_factory_unlock(with_box_open=with_box_open)
            else:
                self.log.add_log('\t[X] has_unlock_factory_text')

            cnt[0] += 1
            self.do_upgrade_factory_upgrade(max_level=max_level, with_box_open=with_box_open, is_last=is_last, cnt=cnt)
        finally:
            self.click_factory(tobe_open=False)

    def on_not_found_city(self):
        info_filepath = BASE_PATH / 'images' / 'maps' / '250' / 'unknown.txt'
        if not info_filepath.exists():
            cnt = 0
        else:
            cnt = int(info_filepath.read_text())

        cnt += 1
        info_filepath.write_text(str(cnt))

        self.save_to_map(
            max_level=250,
            name=f'Unknown {cnt:05d}',
            is_completed=False
        )


    def main_logic(self):
        self.check_init_dialog_box()

        self.screenshot()
        self.check_new_stage_found_go_next_stage_button()

        self.max_level, self.name = self.get_level_city()

        if not self.name:
            self.log.add_log('Not Found City')
            self.on_not_found_city()
            return

        self.factory_info = self.city.get_factory_info(max_level=self.max_level, name=self.name)

        print(f'Max Level : {self.max_level}, name : {self.name}')
        print(f"Factories : {len(self.factory_info)}")
        for d in self.factory_info:
            print(f'\t{d}')

        self.init_screen_pos()

        factory_list = []  # (is_last, with_box_open, factory)
        if self.factory_info:
            factory_list.append((False, True, self.factory_info[0]))
        if len(self.factory_info) > 1:
            factory_list.append((True, True, self.factory_info[-1]))
        for i in range( 1, len(self.factory_info) - 1 ):
            factory_list.append((False, False, self.factory_info[i]))

        for is_last, with_box_open, factory in factory_list:
            self.click_factory(tobe_open=False)
            offset = factory['offset']
            sx, sy, ex, ey = factory['pos']
            self.log.add_log(f'First/Last Factory Upgrade ({sx}, {sy}, {ex}, {ey}), offset={offset}')
            self.init_factory_pos(sx=sx, sy=sy, ex=ex, ey=ey, offset=offset)
            self.adjust_factory_offset(with_box_open)
            cnt = [0]
            if not self.do_upgrade_factory_open(max_level=self.max_level, with_box_open=with_box_open, is_last=is_last, cnt=cnt):
                self.log.add_log(f'Failed to do_upgrade_factory_open')
                return
            if self.template.has_go_to_next_stage(self.img):
                break

        # do upgrade every thing.
        if self.check_new_stage_found_go_next_stage_button():
            return True

    @repeat_retry(repeat=2)
    def _on_new_stage_intro_popup(self):
        """
        new stage - step 3.
        :return:
        """
        sleep(1)
        self.screenshot()
        actions, result = self.template.get_actions_on_new_stage_intro2(self.img)
        if result:
            self.log.add_log('found [ON_NEW_STAGE_INTRO 2] and do actions')
            self.do_first_action(actions, result)
            raise ResetRepeatCountException()

        actions, result = self.template.get_actions_on_new_stage_intro(self.img)
        if result:
            self.log.add_log('found [ON_NEW_STAGE_INTRO] and do actions')
            self.do_first_action(actions, result)
            raise ResetRepeatCountException()

    @repeat_retry(repeat=2)
    def _on_new_stage_buy_new_stage(self):
        """
        new stage - step 2. buy new stage
        :return:
        """
        self.screenshot()
        actions, result = self.template.get_actions_buy_new_stage(self.img)
        if result:
            self.log.add_log('found [BUY_NEXT_STAGE] and do actions')
            self.do_first_action(actions, result)
            sleep(2)
            if self.max_level == 250:
                sleep(5)

            raise ExitRepeatException()

    def check_new_stage_found_go_next_stage_button(self):
        self.screenshot()
        actions, result = self.template.get_actions_go_to_next_stage(self.img)
        if actions:
            self.log.add_log('found [GO_TO_NEXT_STAGE] and do actions')
            self.do_first_action(actions, result)

            if self._on_new_stage_buy_new_stage():
                if self._on_new_stage_intro_popup():
                    self.check_init_dialog_box()
                    pass
            return True

    @repeat_retry(repeat=3)
    def check_init_dialog_box(self):
        """
            화면 전역에 뜨는 dialog box
        :return:
        """
        self.log.add_log('[check_init_dialog_box]')

        function_list = [
            self.template.get_actions_offline_earning_close_box,
            self.template.get_actions_away_earn_close_box,
            self.template.get_actions_on_new_stage_intro2,
            self.template.get_actions_on_new_stage_intro,
        ]
        sleep(2)
        self.screenshot()

        for fn in function_list:
            actions, result = fn(self.img)
            if result:
                self.log.add_log(f'\t[O] {fn.__name__}')
                self.do_all_actions(actions, result)
                raise ResetRepeatCountException()
            else:
                self.log.add_log(f'\t[X] {fn.__name__}')


        if self.template.has_setup_gear_menu(self.img):
            self.log.add_log(f'\t[O] has_setup_gear_menu')
            raise ExitRepeatException()

        if self.template.has_go_to_next_stage(self.img):
            self.log.add_log(f'\t[O] has_go_to_next_stage')
            raise ExitRepeatException()


    def run(self):
        # self.screenshot(delete=False)
        self.dm.stop_app()
        self.dm.start_app()
        self.template.load_templates()
        self.city.load_cities()

        while True:
            work_path = self.log_filepath().parent
            if work_path.exists():
                shutil.rmtree(work_path)
                
            if not self.main_logic():
                break


if __name__ == '__main__':
    helper = AutoHelper("com.hwqgrhhjfd.idlefastfood")
    helper.run()
