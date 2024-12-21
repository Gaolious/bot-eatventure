import shutil
from datetime import datetime
from time import sleep
from typing import Tuple, Dict, List, Callable, Optional

from actions import Action
from devices import DeviceManager
from images import MatchingResult, MatchingRect, Img
from loggers import Logger, KST
from logic_base import AutoBase
from templates import BASE_PATH, TemplateManager
from utils import repeat_retry, ExitRepeatException, ResetRepeatCountException

ORIGIN = 0
GRAY = 1
HSV = 2


class AutoHelper(AutoBase):

    @repeat_retry(repeat=3)
    def check_init_dialog_box(self):
        """
            화면 전역에 뜨는 dialog box
        :return:
        """
        self.log.add_log('Phase 1. 화면 전역에 뜨는 dialog box 닫기')

        function_list: List[Callable[[Tuple[Img, Img]], Tuple[List[Action], Optional[MatchingResult]]]] = [
            self.template.get_actions_offline_earning_close_box,
            self.template.get_actions_away_earn_close_box,
            self.template.get_actions_on_new_stage_intro2,
            self.template.get_actions_on_new_stage_intro,
        ]

        for fn in function_list:
            actions, result = fn(self.img)
            if result:
                self.log.add_log(f'\tFound : {fn.__name__}')
                self.do_all_actions(actions, result)
                self.screenshot()
                raise ResetRepeatCountException()

        if self.template.has_setup_gear_menu(self.img):
            raise ExitRepeatException()

        if self.template.has_go_to_next_stage(self.img):
            raise ExitRepeatException()

        self.screenshot()

    @repeat_retry(repeat=3)
    def _on_new_stage_intro_popup(self):
        """
        new stage - step 3.
        :return:
        """
        self.screenshot()
        actions, result = self.template.get_actions_on_new_stage_intro(self.img)
        if result:
            self.log.add_log('found [ON_NEW_STAGE_INTRO] and do actions')
            self.do_first_action(actions, result)
            raise ResetRepeatCountException()

    @repeat_retry(repeat=3)
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
            raise ExitRepeatException()

    def check_new_stage_found_go_next_stage_button(self):
        actions, result = self.template.get_actions_go_to_next_stage(self.img)
        if not actions:
            return
        self.log.add_log('found [GO_TO_NEXT_STAGE] and do actions')
        self.do_first_action(actions, result)

        if self._on_new_stage_buy_new_stage():
            if self._on_new_stage_intro_popup():
                pass
            # one more ?
        self.screenshot()

    def _do_upgrade_food_factory_with_gold_button(self, factory_actions, factory_result, gold_button_actions, gold_button_result):

        self.log.add_log('\t[_do_upgrade_food_factory_with_gold_button]')

        for r in range(2000):
            if not (self.template.has_upgrade_coin_active(self.img) or self.template.has_upgrade_coin_deactive(self.img)):
                self.log.add_log('\t업글 열기 - _do_upgrade_food_factory_with_gold_button')
                self.do_first_action(factory_actions, factory_result)

            self.do_first_action(gold_button_actions, gold_button_result)

            self.screenshot()
            if self.template.has_reach_to_maximum_upgrade(self.img):
                """
                    완료면, exit
                """
                self.log.add_log('\t업글 완료 / 업글 닫기 - _do_upgrade_food_factory_with_gold_button')
                self.do_first_action(factory_actions, factory_result)
                raise ExitRepeatException()

            actions, result = self.template.get_actions_serve_box(self.img)
            if result:
                self.log.add_log('\tbox 오픈 - _do_upgrade_food_factory_with_gold_button')
                self.do_all_actions(actions, result)
                self.do_first_action(factory_actions, factory_result)

            actions, result = self.template.get_actions_upgrade_skill_button(self.img)
            if result:
                self.log.add_log('\tskill 업글 - _do_upgrade_food_factory_with_gold_button')
                self.do_all_actions(actions, result)

    @repeat_retry(repeat=2)
    def _do_upgrade_food_factory(self, factory_actions, factory_result):
        self.log.add_log('\t[_do_upgrade_food_factory]')

        if self.template.has_reach_to_maximum_upgrade(self.img):
            """
                완료면, exit
            """
            self.log.add_log('\t업글 완료 - _do_upgrade_food_factory')
            self.do_first_action(factory_actions, factory_result)
            raise ExitRepeatException()

        actions, result = self.template.get_actions_google_ad_timer(self.img)
        if not result:
            self.log.add_log('\tAd Timer 찾지 못함. - _do_upgrade_food_factory')
            self.watching_google_ad()

        actions, result = self.template.get_actions_upgrade_coin_active(self.img)
        if result:
            """
                업글 가능
            """
            self._do_upgrade_food_factory_with_gold_button(factory_actions, factory_result, actions, result)
        else:
            self.log.add_log('\t업글 창 열기 - _do_upgrade_food_factory')
            self.do_first_action(factory_actions, factory_result)

        self.screenshot()
        raise ResetRepeatCountException()


    def _do_upgrade_food_factory_first_time(self, selected_actions, selected_result):
        self.log.add_log('\t[_do_upgrade_food_factory_first_time]')
        actions, result = self.template.get_actions_buy_food_factory_coin(self.img)
        if result:
            self.do_first_action(actions, result)

            self.screenshot()

            actions, result = self.template.get_actions_serve_box(self.img)
            if result:
                self.log.add_log('\tbox 오픈 - _do_upgrade_food_factory_first_time')
                self.do_all_actions(actions, result)

            actions, result = self.template.get_actions_upgrade_skill_button(self.img)
            if result:
                self.log.add_log('\tskill 업글 - _do_upgrade_food_factory_first_time')
                self.do_all_actions(actions, result)

            self.do_first_action(selected_actions, selected_result)

            self.screenshot()
            self._do_upgrade_food_factory(selected_actions, selected_result)

    @repeat_retry(repeat=6)
    def _scan_upgradable_food_factory_top_to_bottom(self):
        """
        업그레이드 가능한 food factory 검색
        :return:
        """
        self.log.add_log(f'\t[_scan_upgradable_food_factory_bottom_to_up]')
        self.screenshot(4)

        if self.template.has_go_to_next_stage(self.img):
            raise ExitRepeatException()

        actions, result = self.template.get_actions_serve_box(self.img)
        if result:
            self.log.add_log('\tbox 오픈')
            self.do_all_actions(actions, result)

        actions, result = self.template.get_actions_upgrade_skill_button(self.img)
        if result:
            self.log.add_log('\tskill 업글')
            self.do_all_actions(actions, result)

        # 1. factory open
        actions, result = self.template.get_actions_upgradable_food_factory_icon(self.img)
        if result:
            result.sort()
            results = result.results[::]
            pos = [f'({res.left},{res.top})' for res in result.results]
            self.log.add_log('\t업그레이드 가능한 food factory 찾음 : ' + ', '.join(pos))

            for ret in results:
                result.results = [ret]
                self.do_first_action(actions, result)
                self.screenshot()
                if self.template.has_unlock_factory_text(self.img):
                    # 처음 open
                    self.log.add_log('\t잠금 해제. 문구 발견')
                    self._do_upgrade_food_factory_first_time(actions, result)
                else:
                    self.log.add_log('\tupgrade food factory')
                    self._do_upgrade_food_factory(actions, result)

                if self.template.has_go_to_next_stage(self.img):
                    raise ExitRepeatException()

            raise ResetRepeatCountException()

        self.dm.move_to_down_1step()

    def scan_boxes(self):
        self.log.add_log('\t[scan_boxes]')
        self.dm.move_to_top()

        for i in range(5):
            self.screenshot(3)
            actions, result = self.template.get_actions_serve_box(self.img)
            if result:
                self.log.add_log('\tbox 오픈')
                self.do_all_actions(actions, result)
            self.dm.move_to_down_1step()

    @repeat_retry(repeat=3)
    def check_upgradable_food_factory(self):
        """
            화면 전역에 뜨는 dialog box
        :return:
        """
        self.log.add_log('Phase 2. Food Factory 찾기 & 업그레이드')
        # self.scan_boxes()
        self.dm.move_to_top()
        if self._scan_upgradable_food_factory_top_to_bottom():
            raise ExitRepeatException()

    @repeat_retry(repeat=3)
    def main_logic(self):
        """
         scroll to top
           find serving_box -> open
           find upgrade skill -> open
           find new factory upgrade -> open

           not found?
           1p down

        :return:
        """
        self.delete_images()
        self.log.add_log('on_new_stage start')

        self.screenshot()
        self.check_init_dialog_box()
        self.check_new_stage_found_go_next_stage_button()
        if self.check_upgradable_food_factory():
            raise ResetRepeatCountException()

    def run(self):
        self.dm.stop_app()
        self.dm.start_app()
        self.template.load_templates()
        self.main_logic()