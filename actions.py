class Action:
    _ACTION_RESTART = 10
    _ACTION_CLICK_ABSOLUTE_POS = 20
    _ACTION_CLICK_LT_OFFSET = 21
    _ACTION_CLICK_LB_OFFSET = 22
    _ACTION_CLICK_RB_OFFSET = 23
    _ACTION_CLICK_RT_OFFSET = 24
    _ACTION_CLICK_CENTER = 25

    action_type: int
    x: int
    y: int
    duration_ms: int

    @classmethod
    def click_abs(cls, x, y, duration_ms=300):
        ret = Action()
        ret.action_type = cls._ACTION_CLICK_ABSOLUTE_POS
        ret.x = x
        ret.y = y
        ret.duration_ms = duration_ms
        return ret

    @classmethod
    def click_rb(cls, x, y, duration_ms=300):
        ret = Action()
        ret.action_type = cls._ACTION_CLICK_RB_OFFSET
        ret.x = x
        ret.y = y
        ret.duration_ms = duration_ms
        return ret

    @classmethod
    def click_rt(cls, x, y, duration_ms=300):
        ret = Action()
        ret.action_type = cls._ACTION_CLICK_RT_OFFSET
        ret.x = x
        ret.y = y
        ret.duration_ms = duration_ms
        return ret

    @classmethod
    def click_lt(cls, x, y, duration_ms=300):
        ret = Action()
        ret.action_type = cls._ACTION_CLICK_LT_OFFSET
        ret.x = x
        ret.y = y
        ret.duration_ms = duration_ms
        return ret

    @classmethod
    def click_lb(cls, x, y, duration_ms=300):
        ret = Action()
        ret.action_type = cls._ACTION_CLICK_LB_OFFSET
        ret.x = x
        ret.y = y
        ret.duration_ms = duration_ms
        return ret

    @classmethod
    def click_center(cls, duration_ms=300):
        ret = Action()
        ret.action_type = cls._ACTION_CLICK_CENTER
        ret.duration_ms = duration_ms
        return ret

    @classmethod
    def restart(cls):
        ret = Action()
        ret.action_type = cls._ACTION_RESTART

    @property
    def is_restart(self):
        return self.action_type == self._ACTION_RESTART

    @property
    def is_click_abs(self):
        return self.action_type == self._ACTION_CLICK_ABSOLUTE_POS

    @property
    def is_click_left_top_offset(self):
        return self.action_type == self._ACTION_CLICK_LT_OFFSET

    @property
    def is_click_right_bottom_offset(self):
        return self.action_type == self._ACTION_CLICK_RB_OFFSET

    @property
    def is_click_left_bottom_offset(self):
        return self.action_type == self._ACTION_CLICK_LB_OFFSET

    @property
    def is_click_right_top_offset(self):
        return self.action_type == self._ACTION_CLICK_RT_OFFSET

    @property
    def is_click_center(self):
        return self.action_type == self._ACTION_CLICK_CENTER

    @property
    def is_click(self):
        return self.is_click_abs or self.is_click_left_top_offset or self.is_click_right_bottom_offset or self.is_click_center or self.is_click_left_bottom_offset or self.is_click_right_top_offset

    def __str__(self):
        if self.is_restart:
            return f'RESTART'
        elif self.is_click_abs:
            return f'CLICK ABS {self.x},{self.y}'
        elif self.is_click_left_top_offset:
            return f'CLICK LT {self.x},{self.y}'
        elif self.is_click_right_bottom_offset:
            return f'CLICK RB {self.x},{self.y}'
        elif self.is_click_center:
            return f'CLICK CENTER'
        return 'unknown'

    def __repr__(self):
        if self.is_restart:
            return f'RESTART'
        elif self.is_click_abs:
            return f'CLICK ABS {self.x},{self.y}'
        elif self.is_click_left_top_offset:
            return f'CLICK LT {self.x},{self.y}'
        elif self.is_click_right_bottom_offset:
            return f'CLICK RB {self.x},{self.y}'
        elif self.is_click_center:
            return f'CLICK CENTER'
        return 'unknown'