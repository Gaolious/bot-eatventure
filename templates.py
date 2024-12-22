import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional

from actions import Action
from images import Img, MatchingResult

BASE_PATH = Path(__file__).parent

class TemplateManager:
    OFFLINE_EARNING_CLOSE_BOX = 'offline_earnings_close_box'
    # CLOUD_SAVE_FOUND_CHOOSE_BOX = 'cloud_save_found_choose_box'
    SETUP_GEAR_APPEAR = 'setup_gear_appear'
    AWAY_EARN_CLOSE_BOX = 'away_earn_close_box'
    # END_OF_RACE_CLOSE_BOX = 'end_of_race_box'

    UPGRADE_SKILL_BUTTON = 'upgrade_skill_button'
    SERVE_BOX = 'serve_box'
    UPGRADABLE_FOOD_FACTORY_ICON = 'found_upgradable_food_factory'
    FOOD_UPGRADE_COIN_ACTIVE = 'food_upgrade_coin_active'
    UPGRADE_COIN_DEACTIVE = 'food_upgrade_coin_deactive'
    REACH_TO_MAXIMUM_UPGRADE = 'reach_to_maximum_upgrade'
    UNLOCK_FACTORY_TEXT = 'unlock_factory_text'
    BUY_FOOD_FACTORY_COIN = 'buy_food_factory_coin'
    GO_TO_NEXT_STAGE = 'go_to_next_stage'

    BUY_NEXT_STAGE = 'buy_next_stage'
    ON_NEW_STAGE_INTRO = 'on_new_stage_intro'
    ON_NEW_STAGE_INTRO2 = 'on_new_stage_intro2'

    GOOGLE_AD_TIMER = 'google_ad_timer'
    GOOGLE_AD_SKIP = 'google_ad_skip'
    GOOGLE_AD_EXIT = 'google_ad_exit'
    GOOGLE_AD_MISS_CLICK = 'google_ad_miss_click'

    MAX_LEVEL_25 = 'max_level_25'
    MAX_LEVEL_50 = 'max_level_50'
    MAX_LEVEL_75 = 'max_level_75'
    MAX_LEVEL_150 = 'max_level_150'
    MAX_LEVEL_250 = 'max_level_250'

    ACTIVE_SKILL_SELECT_BUTTON = 'active_skill_select_button'
    ACTIVE_SKILL_SELECT_TEXT = 'active_skill_select_text'

    templates : Dict[str, Dict[str, List]]= {
        OFFLINE_EARNING_CLOSE_BOX: {
            'templates' : [
                BASE_PATH / 'images' / 'templates' / 'offline_earn_x_button.png',
            ],
            'actions': [ Action.click_center() ]
        },
        SETUP_GEAR_APPEAR: {
            'templates' : [
                BASE_PATH / 'images' / 'templates' / 'menu_gear_1.png',
            ],
            'actions': []
        },
        AWAY_EARN_CLOSE_BOX: {
            'templates' : [
                BASE_PATH / 'images' / 'templates' / 'away_x_button.png',
            ],
            'actions': [ Action.click_center() ]

        },
        ################################################################################################################
        #
        ################################################################################################################
        MAX_LEVEL_25: {'templates' : [BASE_PATH / 'images' / 'templates' / 'map_25.png'], 'actions': []},
        MAX_LEVEL_50: {'templates' : [BASE_PATH / 'images' / 'templates' / 'map_50.png'], 'actions': []},
        MAX_LEVEL_75: {'templates' : [BASE_PATH / 'images' / 'templates' / 'map_75.png'], 'actions': []},
        MAX_LEVEL_150: {'templates' : [BASE_PATH / 'images' / 'templates' / 'map_150.png'], 'actions': []},
        MAX_LEVEL_250: {'templates' : [BASE_PATH / 'images' / 'templates' / 'map_250.png'], 'actions': []},

        ################################################################################################################
        #
        ################################################################################################################
        UPGRADE_SKILL_BUTTON: {  # 우하단. 업그레이드 버튼
            'templates': [
                BASE_PATH / 'images' / 'templates' / 'skill_upgrade_1.png',
            ],
            'actions':
                [Action.click_abs(980, 2202)] +  # 우하단 메뉴 버튼
                [Action.click_abs(842, 954, 80)] * 10  + # 업글
                [Action.click_abs(920, 778, 80)] # X 버튼
        },
        SERVE_BOX: {  # 박스
            'templates': [
                BASE_PATH / 'images' / 'templates' / 'boxes.png',
            ],
            'actions': [ Action.click_center(), ]
        },
        UPGRADABLE_FOOD_FACTORY_ICON: { # 빨간원 배경에 위를 가르키는 흰색 화살표
            'templates': [
                BASE_PATH / 'images' / 'templates' / 'factory_open_1.png',
            ],
            'actions': [ Action.click_rb(x=40, y=80), ]
        },
        FOOD_UPGRADE_COIN_ACTIVE: { # 파랑 배경에 코인 (업그레이드) or Open
            'templates': [
                BASE_PATH / 'images' / 'templates' / 'factory_upgrade_gold_active.png',
            ],
            'actions': [ Action.click_center(duration_ms=3000), ]
        },
        BUY_FOOD_FACTORY_COIN: { # 파랑 배경에 코인 (업그레이드) or Open
            'templates': [
                BASE_PATH / 'images' / 'templates' / 'factory_upgrade_gold_active.png',
            ],
            'actions': [ Action.click_center(duration_ms=300), ]
        },
        UPGRADE_COIN_DEACTIVE: { # 회색 배경에 코인 (업그레이드) deactive (gold 부족)
            'templates': [
                BASE_PATH / 'images' / 'templates' / 'factory_upgrade_gold_deactive.png',
            ],
            'actions': [ Action.click_center(duration_ms=2000), ]
        },
        UNLOCK_FACTORY_TEXT: { # 잠금 해제 text
            'templates': [
                BASE_PATH / 'images' / 'templates' / 'factory_unlock_text.png',
            ],
            'actions': [ Action.click_center(duration_ms=500), ]
        },
        REACH_TO_MAXIMUM_UPGRADE: {
            'templates': [
                BASE_PATH / 'images' / 'templates' / 'factory_upgrade_complete.png',
            ],
            'actions': []
        },
        GO_TO_NEXT_STAGE: {
            'templates': [
                BASE_PATH / 'images' / 'templates' / 'next_stage_can_go.png',
                BASE_PATH / 'images' / 'templates' / 'next_stage_can_go_2.png',
            ],
            'actions': [Action.click_lb(x=-20, y=-20)]
        },
        BUY_NEXT_STAGE: {
            'templates': [
                BASE_PATH / 'images' / 'templates' / 'next_stage_remodeling.png',
                BASE_PATH / 'images' / 'templates' / 'next_stage_remodeling_2.png',
            ],
            'actions': [Action.click_center()]
        },
        ON_NEW_STAGE_INTRO: {
            'templates': [
                BASE_PATH / 'images' / 'templates' / 'next_stage_new.png',
            ],
            'actions': [Action.click_center()]
        },
        ON_NEW_STAGE_INTRO2: {
            'templates': [
                BASE_PATH / 'images' / 'templates' / 'next_stage_new_2.png',
            ],
            'actions': [Action.click_center()]
        },
        GOOGLE_AD_TIMER: {
            'templates': [
                BASE_PATH / 'images' / 'templates' / 'ad_min.png',
                BASE_PATH / 'images' / 'templates' / 'ad_sec.png',
            ],
            'actions': [
                # Action.click_abs(537, 2199)
            ]
        },
        GOOGLE_AD_SKIP: {
            'templates': [
                BASE_PATH / 'images' / 'templates' / 'ad_skip_1.png',
                BASE_PATH / 'images' / 'templates' / 'ad_skip_2.png',
                BASE_PATH / 'images' / 'templates' / 'ad_skip_3.png',
                BASE_PATH / 'images' / 'templates' / 'ad_skip_4.png',
            ],
            'actions': [Action.click_center()]
        },
        GOOGLE_AD_EXIT: {
            'templates': [
                BASE_PATH / 'images' / 'templates' / 'ad_exit_1.png',
                BASE_PATH / 'images' / 'templates' / 'ad_exit_2.png',
                BASE_PATH / 'images' / 'templates' / 'ad_exit_3.png',
            ],
            'actions': [Action.click_center()]
        },
        GOOGLE_AD_MISS_CLICK: {
            'templates': [
                BASE_PATH / 'images' / 'templates' / 'google_miss_click.png',
            ],
            'actions': []
        },
        ACTIVE_SKILL_SELECT_BUTTON: {
            'templates': [
                BASE_PATH / 'images' / 'templates' / 'active_skill_select.png',
            ],
            'actions': [Action.click_center()]
        },
        ACTIVE_SKILL_SELECT_TEXT: {
            'templates': [
                BASE_PATH / 'images' / 'templates' / 'active_skill_select_text.png',
            ],
            'actions': []
        }
    }
    #     ACTIVE_SKILL_SELECT_BUTTON = 'active_skill_select_button'
    #     ACTIVE_SKILL_SELECT_TEXT = 'active_skill_select_text'
    images = {}
    ranges = {}

    def load_templates(self):
        for key in self.templates:
            for filepath in self.templates[key]['templates']:
                p = str(filepath)

                if p not in self.images:
                    self.images[p] = Img(filepath)

                    info_file = filepath.with_suffix('.json')
                    data = json.loads(info_file.read_text())
                    x, y = data['xy']
                    w, h = data['size']
                    self.ranges[p] = (x, y, x+w, y+h)

    def _has_template(self, attr, key, capture_image: Tuple[Img, Img], threshold = 0.85) -> Tuple[bool, MatchingResult]:
        for filepath in self.templates[key]['templates']:
            p = str(filepath)

            for target in capture_image:
                result = None

                if attr == 'png':
                    result = target.matching_png(self.images[p], self.ranges[p], threshold )
                elif attr == 'gray':
                    result = target.matching_gray(self.images[p], self.ranges[p], threshold )
                elif attr == 'hsv':
                    result = target.matching_hsv(self.images[p], self.ranges[p], threshold )

                if result.is_found:
                    return True, result


        return False, None

    def _get_action(self, attr, key, capture_image: Tuple[Img, Img], threshold = 0.85) -> Tuple[List[Action], Optional[MatchingResult]]:
        ret, result = self._has_template(attr, key, capture_image, threshold)
        if ret:
            return self.templates[key]['actions'], result
        return [], None

    def get_actions_offline_earning_close_box(self, capture_image: Tuple[Img, Img] ) -> Tuple[List[Action], Optional[MatchingResult]]:
        return self._get_action('png', self.OFFLINE_EARNING_CLOSE_BOX, capture_image)

    # def get_actions_need_to_restart_client(self, capture_image: Tuple[Img, Img] ) -> Tuple[List[Action], Optional[MatchingResult]]:
    #     return self._get_action('png', self.NEED_TO_RESTART_CLIENT, capture_image)

    def get_actions_away_earn_close_box(self, capture_image: Tuple[Img, Img] ) -> Tuple[List[Action], Optional[MatchingResult]]:
        return self._get_action('png', self.AWAY_EARN_CLOSE_BOX, capture_image)

    # def get_actions_end_of_race_close_box(self, capture_image: Img ) -> Tuple[List[Action], Optional[MatchingResult]]:
    #     return self._get_action('png', self.END_OF_RACE_CLOSE_BOX, capture_image)

    def has_setup_gear_menu(self, capture_image: Tuple[Img, Img] ) -> bool:
        ret, _ = self._has_template('png', self.SETUP_GEAR_APPEAR, capture_image)
        return ret

    def get_actions_upgrade_skill_button(self, capture_image: Tuple[Img, Img] ) -> Tuple[List[Action], Optional[MatchingResult]]:
        return self._get_action('png', self.UPGRADE_SKILL_BUTTON, capture_image)

    def has_upgrade_skill_button(self, capture_image: Tuple[Img, Img] ) -> bool:
        ret, _ = self._has_template('png', self.UPGRADE_SKILL_BUTTON, capture_image)
        return ret

    def get_actions_serve_box(self, capture_image: Tuple[Img, Img] ) -> Tuple[List[Action], Optional[MatchingResult]]:
        return self._get_action('gray', self.SERVE_BOX, capture_image)

    def has_serve_box(self, capture_image: Tuple[Img, Img] ) -> bool:
        ret, _ = self._has_template('gray', self.SERVE_BOX, capture_image)
        return ret

    def get_actions_upgradable_food_factory_icon(self, capture_image: Tuple[Img, Img] ) -> Tuple[List[Action], Optional[MatchingResult]]:
        return self._get_action('gray', self.UPGRADABLE_FOOD_FACTORY_ICON, capture_image)

    def has_upgradable_food_factory_icon(self, capture_image: Tuple[Img, Img] ) -> bool:
        ret, _ = self._has_template('gray', self.UPGRADABLE_FOOD_FACTORY_ICON, capture_image)
        return ret

    def get_actions_upgrade_coin_active(self, capture_image: Tuple[Img, Img] ) -> Tuple[List[Action], Optional[MatchingResult]]:
        return self._get_action('png', self.FOOD_UPGRADE_COIN_ACTIVE, capture_image)

    def has_upgrade_coin_active(self, capture_image: Tuple[Img, Img] ) -> bool:
        ret, _ = self._has_template('png', self.FOOD_UPGRADE_COIN_ACTIVE, capture_image)
        return ret

    def get_actions_buy_food_factory_coin(self, capture_image: Tuple[Img, Img] ) -> Tuple[List[Action], Optional[MatchingResult]]:
        return self._get_action('png', self.BUY_FOOD_FACTORY_COIN, capture_image)

    def has_buy_food_factory_coin(self, capture_image: Tuple[Img, Img] ) -> bool:
        ret, _ = self._has_template('png', self.BUY_FOOD_FACTORY_COIN, capture_image)
        return ret

    def get_actions_upgrade_coin_deactive(self, capture_image: Tuple[Img, Img] ) -> Tuple[List[Action], Optional[MatchingResult]]:
        return self._get_action('png', self.UPGRADE_COIN_DEACTIVE, capture_image)

    def has_upgrade_coin_deactive(self, capture_image: Tuple[Img, Img] ) -> bool:
        ret, _ = self._has_template('png', self.UPGRADE_COIN_DEACTIVE, capture_image)
        return ret

    def get_actions_unlock_factory_text(self, capture_image: Tuple[Img, Img] ) -> Tuple[List[Action], Optional[MatchingResult]]:
        return self._get_action('png', self.UNLOCK_FACTORY_TEXT, capture_image)

    def has_unlock_factory_text(self, capture_image: Tuple[Img, Img] )  -> bool:
        ret, _ = self._has_template('png', self.UNLOCK_FACTORY_TEXT, capture_image)
        return ret

    def get_actions_reach_to_maximum_upgrade(self, capture_image: Tuple[Img, Img] ) -> Tuple[List[Action], Optional[MatchingResult]]:
        return self._get_action('png', self.REACH_TO_MAXIMUM_UPGRADE, capture_image)

    def has_reach_to_maximum_upgrade(self, capture_image: Tuple[Img, Img] )  -> bool:
        ret, _ = self._has_template('png', self.REACH_TO_MAXIMUM_UPGRADE, capture_image)
        return ret

    def get_actions_go_to_next_stage(self, capture_image: Tuple[Img, Img] ) -> Tuple[List[Action], Optional[MatchingResult]]:
        """
        좌하단 업글 버튼
        :param capture_image:
        :return:
        """
        return self._get_action('hsv', self.GO_TO_NEXT_STAGE, capture_image)

    def has_go_to_next_stage(self, capture_image: Tuple[Img, Img] )  -> bool:
        ret, _ = self._has_template('png', self.GO_TO_NEXT_STAGE, capture_image)
        return ret

    def get_actions_buy_new_stage(self, capture_image: Tuple[Img, Img]) -> Tuple[List[Action], Optional[MatchingResult]]:
        """
        gold로 이동
        :param capture_image:
        :return:
        """
        return self._get_action('png', self.BUY_NEXT_STAGE, capture_image)

    def has_buy_new_stage(self, capture_image: Tuple[Img, Img]) -> bool:
        ret, _ = self._has_template('png', self.BUY_NEXT_STAGE, capture_image)
        return ret

    def get_actions_on_new_stage_intro2(self, capture_image: Tuple[Img, Img]) -> Tuple[List[Action], Optional[MatchingResult]]:
        """
        intro
        :param capture_image:
        :return:
        """
        return self._get_action('png', self.ON_NEW_STAGE_INTRO2, capture_image)

    def has_on_new_stage_intro2(self, capture_image: Tuple[Img, Img]) -> bool:
        ret, _ = self._has_template('png', self.ON_NEW_STAGE_INTRO2, capture_image)
        return ret

    def get_actions_on_new_stage_intro(self, capture_image: Tuple[Img, Img]) -> Tuple[List[Action], Optional[MatchingResult]]:
        """
        intro
        :param capture_image:
        :return:
        """
        return self._get_action('png', self.ON_NEW_STAGE_INTRO, capture_image)

    def has_on_new_stage_intro(self, capture_image: Tuple[Img, Img]) -> bool:
        ret, _ = self._has_template('png', self.ON_NEW_STAGE_INTRO, capture_image)
        return ret

    def get_actions_google_ad_timer(self, capture_image: Tuple[Img, Img]) -> Tuple[List[Action], Optional[MatchingResult]]:
        """
        intro
        :param capture_image:
        :return:
        """
        return self._get_action('gray', self.GOOGLE_AD_TIMER, capture_image)

    def get_actions_google_ad_skip(self, capture_image: Tuple[Img, Img]) -> Tuple[List[Action], Optional[MatchingResult]]:
        return self._get_action('gray', self.GOOGLE_AD_SKIP, capture_image)

    def has_google_ad_skip(self, capture_image: Tuple[Img, Img]) -> bool:
        ret, _ = self._has_template('gray', self.GOOGLE_AD_SKIP, capture_image)
        return ret

    def get_actions_google_ad_exit(self, capture_image: Tuple[Img, Img]) -> Tuple[List[Action], Optional[MatchingResult]]:
        return self._get_action('gray', self.GOOGLE_AD_EXIT, capture_image)

    def has_google_ad_exit(self, capture_image: Tuple[Img, Img]) -> bool:
        ret, _ = self._has_template('gray', self.GOOGLE_AD_EXIT, capture_image)
        return ret

    def has_google_ad_miss_click(self, capture_image: Tuple[Img, Img]) -> bool:
        ret, _ = self._has_template('gray', self.GOOGLE_AD_MISS_CLICK, capture_image)
        return ret

    def has_maximum_level_25(self, capture_image: Tuple[Img, Img] ) -> bool:
        ret, _ = self._has_template('png', self.MAX_LEVEL_25, capture_image)
        return ret
    def has_maximum_level_50(self, capture_image: Tuple[Img, Img] ) -> bool:
        ret, _ = self._has_template('png', self.MAX_LEVEL_50, capture_image)
        return ret
    def has_maximum_level_75(self, capture_image: Tuple[Img, Img] ) -> bool:
        ret, _ = self._has_template('png', self.MAX_LEVEL_75, capture_image)
        return ret
    def has_maximum_level_150(self, capture_image: Tuple[Img, Img] ) -> bool:
        ret, _ = self._has_template('png', self.MAX_LEVEL_150, capture_image)
        return ret
    def has_maximum_level_250(self, capture_image: Tuple[Img, Img] ) -> bool:
        ret, _ = self._has_template('png', self.MAX_LEVEL_250, capture_image)
        return ret

    def get_actions_active_skill_select_button(self, capture_image: Tuple[Img, Img]) -> Tuple[List[Action], Optional[MatchingResult]]:
        return self._get_action('png', self.ACTIVE_SKILL_SELECT_BUTTON, capture_image)

    def has_active_skill_select_button(self, capture_image: Tuple[Img, Img]) -> bool:
        ret, _ = self._has_template('png', self.ACTIVE_SKILL_SELECT_BUTTON, capture_image)
        return ret