import math
from functools import cached_property
from time import sleep
from typing import final, Tuple, Callable, List, Dict

from cities import CityManager
from logic_base import AutoBase
from templates import BASE_PATH
from utils import repeat_retry, ExitRepeatException, ResetRepeatCountException

ORIGIN = 0
GRAY = 1
HSV = 2


class AutoHelper(AutoBase):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def initialize(self):
        pass

    # Step 1.
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
        self.screenshot()
        sleep(3)

        for fn in function_list:
            actions, result = fn(self.img)
            if result:
                self.log.add_log(f'\t[O] {fn.__name__}')
                self.do_all_actions(actions, result)
                self.screenshot()
                raise ResetRepeatCountException()
            else:
                self.log.add_log(f'\t[X] {fn.__name__}')


        if self.template.has_setup_gear_menu(self.img):
            self.log.add_log(f'\t[O] has_setup_gear_menu')
            raise ExitRepeatException()

        if self.template.has_go_to_next_stage(self.img):
            self.log.add_log(f'\t[O] has_go_to_next_stage')
            raise ExitRepeatException()

    @repeat_retry(repeat=2)
    def _on_new_stage_intro_popup(self):
        """
        new stage - step 3.
        :return:
        """
        self.screenshot()

        actions, result = self.template.get_actions_on_new_stage_intro2(self.img)
        if result:
            self.log.add_log('\t[O] ON_NEW_STAGE_INTRO FLIGHT')
            self.do_first_action(actions, result)
            raise ResetRepeatCountException()

        actions, result = self.template.get_actions_on_new_stage_intro(self.img)
        if result:
            self.log.add_log('\t[O] ON_NEW_STAGE_INTRO')
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
            self.log.add_log('\t[O] BUY_NEXT_STAGE')
            self.do_first_action(actions, result)
            sleep(2)
            raise ExitRepeatException()


    @repeat_retry(repeat=2)
    def open_factory(self, x, y):
        is_opened = False
        try:

            actions, result = self.template.get_actions_google_ad_timer(self.img)
            if not result:
                self.log.add_log('\t[O] Google adv')
                self.watching_google_ad()

            self.open_upgrade_skill()
            self.open_boxes()

            self.log.add_log(f'\tOpen Factory {x}, {y}')
            self.dm.click(x, y)
            is_opened = True

            self.screenshot()

            if self.template.has_reach_to_maximum_upgrade(self.img):
                raise ExitRepeatException()

            if self.template.has_go_to_next_stage(self.img):
                raise ExitRepeatException()

            if self.template.has_unlock_factory_text(self.img):
                if not is_opened:
                    self.dm.click(x, y)
                    is_opened = True

                actions, result = self.template.get_actions_buy_food_factory_coin(self.img)
                if result:
                    self.log.add_log(f'\t[O] Unlock Factory')
                    self.do_all_actions(actions, result)

                raise ResetRepeatCountException()
            else:
                self.log.add_log(f'\t[X] Unlock Factory')

            functions = [
                self.template.get_actions_upgrade_coin_active,
                self.template.get_actions_upgrade_coin_deactive,
            ]

            for fn in functions:
                actions, result = fn(self.img)
                if result:
                    self.log.add_log(f'\t[O] Upgrade Factory / {fn.__name__}')
                    self.do_first_action(actions, result)
                    raise ResetRepeatCountException()
                else:
                    self.log.add_log(f'\t[X] Upgrade Factory / {fn.__name__}')

        finally:
            if is_opened:
                self.log.add_log(f'\tClose Factory {x}, {y}')
                self.dm.click(x, y)

    # Step 2. find factory to upgrade
    @repeat_retry(repeat=3)
    def find_factory_from_bottom_to_top(self, cnt):
        # self.dm.move_to_bottom()
        self.dm.move_to_top()

        # -----------------------------------
        # skill upgrade / (935, 2129) 7 39
        # -----------------------------------
        # (197, 1704) 7 36
        # (77, 1392) 7 30
        # -----------------------------------
        tolerance = 5
        if cnt[0] >= 2: tolerance = 20
        if cnt[0] >= 3: tolerance = 40

        for i in range(10):
            self.log.add_log(f'[find factory to upgrade] {i+1} / 10')
            self.screenshot()
            # Step 4. GO_TO_NEXT_STAGE
            if self.check_new_stage_found_go_next_stage_button():
                raise ExitRepeatException

            factory_arrows = self.img[0].get_pos_upgrade_arrow(factory_only=True, tolerance=tolerance)
            if not factory_arrows:
                # self.dm.move_to_up_1step()
                self.dm.move_to_down_1step()
                self.open_upgrade_skill()
                self.open_boxes()
                continue

            for p in factory_arrows:
                self.open_factory(p[0] + 40, p[1] + 60)

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
        if skill_arrows:
            self.log.add_log('\t[O] Skill Upgrade')
            for act in self.template.templates[key]['actions']:
                self.dm.click(act.x, act.y, 80)

        else:
            self.log.add_log('\t[X] Skill Upgrade')

    # Step 4.
    def check_new_stage_found_go_next_stage_button(self):
        actions, result = self.template.get_actions_go_to_next_stage(self.img)
        if actions:
            self.log.add_log('\t [GO_TO_NEXT_STAGE] and do actions')
            self.do_first_action(actions, result)

            if self._on_new_stage_buy_new_stage():
                if self._on_new_stage_intro_popup():
                    pass
            return True

    def main_logic(self):
        # Step 1.
        self.check_init_dialog_box()

        # Step 4. GO_TO_NEXT_STAGE
        self.check_new_stage_found_go_next_stage_button()

        cnt = [0]
        # Step 2. find factory to upgrade
        self.find_factory_from_bottom_to_top(cnt)

        self.check_new_stage_found_go_next_stage_button()

    def run(self):

        self.dm.stop_app()
        self.dm.start_app()
        self.template.load_templates()
        self.main_logic()


if __name__ == '__main__':
    helper = AutoHelper("com.hwqgrhhjfd.idlefastfood")
    helper.run()
