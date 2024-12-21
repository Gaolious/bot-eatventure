from pathlib import Path
from typing import List, Dict, Tuple

import cv2
import numpy as np

box_tolerance = 20
# 테두리 색 (#AA7345)
box_border_color = np.array([69, 115, 170])  # BGR
box_lower_border = np.clip(box_border_color - box_tolerance, 0, 255)
box_upper_border = np.clip(box_border_color + box_tolerance, 0, 255)

# 민무늬 색 (#FFE18A)
box_pattern_color = np.array([138, 225, 255])  # BGR
box_lower_pattern = np.clip(box_pattern_color - box_tolerance, 0, 255)
box_upper_pattern = np.clip(box_pattern_color + box_tolerance, 0, 255)

lower_red1 = np.array([0, 100, 100])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([160, 100, 100])
upper_red2 = np.array([179, 255, 255])

lower_white = np.array([245, 245, 245])  # 허용 범위 하한
upper_white = np.array([255, 255, 255])  # 허용 범위 상한


class MatchingRect:
    ratio: float
    top: int
    left: int
    bottom: int
    right: int
    def __init__(self, ratio: float, left, top, w, h):
        self.ratio = ratio
        self.top = top
        self.left = left
        self.bottom = top + h
        self.right = left + w

    def intersects(self, other):
        """Check if this rectangle intersects with another rectangle."""
        return not (
            self.right <= other.left or
            self.left >= other.right or
            self.bottom <= other.top or
            self.top >= other.bottom
        )

    def __str__(self):
        return f'({self.left}, {self.top}) - ({self.right}, {self.bottom})'

    def __repr__(self):
        return f'({self.left}, {self.top}) - ({self.right}, {self.bottom})'


class MatchingResult:
    is_found: bool

    results: List[MatchingRect]
    def __init__(self):
        self.is_found = False
        self.results = []

    def found(self, ratio: float, left, top, w, h):
        self.is_found = True
        self.results.append(
            MatchingRect(ratio=ratio, left=left, top=top, w=w, h=h)
        )
    def set_max_count(self, cnt: int):
        if len(self.results) > cnt:
            self.results = self.results[:cnt]

    def __str__(self):
        return ', '.join([ str(s) for s in self.results ])

    def __repr__(self):
        return ', '.join([ str(s) for s in self.results ])

    def remove_duplicates(self):
        non_overlapping = []

        # Sort by ratio descending for priority, then by position for consistency
        self.results.sort(key=lambda x: (-x.ratio, x.top, x.left))

        for rect in self.results:
            overlap_found = False
            for existing in non_overlapping:
                if rect.intersects(existing):
                    overlap_found = True
                    break

            if not overlap_found:
                non_overlapping.append(rect)

        self.results = non_overlapping

    def sort(self):
        self.results.sort(key=lambda x: (-x.bottom, -x.right))


class Img:
    png : List
    gray : List
    hsv : List

    def __init__(self, path: Path):
        self.png = []
        self.gray = []
        self.hsv = []
        if not path.is_file():
            raise FileNotFoundError

        self.png = cv2.imread(str(path))
        self.gray = cv2.cvtColor(self.png, cv2.COLOR_BGRA2GRAY)
        self.hsv = cv2.cvtColor(self.png, cv2.COLOR_BGR2HSV)

    def _matching(self, attr, other: 'Img', range: Tuple[int,int,int,int], threshold = 0.80) -> MatchingResult:
        ret = MatchingResult()
        rectangles = []
        sx, sy, ex, ey = range
        src = getattr(self, attr)
        dest = getattr(other, attr)

        w, h = dest.shape[1], dest.shape[0]
        result = cv2.matchTemplate(src, dest, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        locations = []
        for (y, x) in zip(*np.where(np.logical_and(result >= threshold, result <= 1))):
            locations.append((x, y))

        locations.sort()

        for (x, y) in locations:
            found = False
            if x < sx or y < sy or x+w > ex or  y+h > ey:
                continue
            if not found:
                rectangles.append([x, y, w, h])

        for (x, y, w, h) in rectangles:
            match_value = result[y, x]
            ret.found(match_value, top=y, left=x, w=w, h=h)

        if ret.is_found:
            ret.remove_duplicates()

        return ret

    def matching_png(self, other: 'Img', range, threshold = 0.85) -> MatchingResult:
        return self._matching('png', other, range, threshold)

    def matching_gray(self, other: 'Img', range, threshold = 0.85) -> MatchingResult:
        return self._matching('gray', other, range, threshold)

    def matching_hsv(self, other: 'Img', range, threshold = 0.85) -> MatchingResult:
        return self._matching('hsv', other, range, threshold)

    def get_pos_upgrade_arrow(self, factory_only, tolerance = 5) -> List[Tuple[int,int]]:

        # 빨간색 범위 정의 (HSV 기준으로 두 개의 범위 설정)
        ret = []

        # 흰색 마스크 생성
        white_mask = cv2.inRange(self.png, lower_white, upper_white)

        # 빨간색 탐지 설정 (이전과 동일)
        target_color = np.array([75, 83, 255])  # #FF534B의 BGR 값
        lower_red = np.clip(target_color - tolerance, 0, 255)
        upper_red = np.clip(target_color + tolerance, 0, 255)

        # 빨간색 마스크 생성
        red_mask = cv2.inRange(self.png, lower_red, upper_red)

        # 빨간색 컨투어 찾기
        contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 빨간색 원 내부에서 화살표 찾기
        for contour in contours:
            # 최소 외접 원 계산
            area = cv2.contourArea(contour)
            (x, y), radius = cv2.minEnclosingCircle(contour)
            center = (int(x), int(y))
            radius = int(radius)
            if radius < 10:
                continue

            circularity = area / (np.pi * (radius ** 2))
            if circularity < 0.75 or circularity > 1.35:  # 원이 아닌 경우 제외
                continue

            # 원 안에 흰색 화살표가 있는지 확인
            # 원 영역 크롭
            mask_circle = np.zeros_like(red_mask)
            cv2.circle(mask_circle, center, radius, 255, -1)
            cropped_circle = cv2.bitwise_and(self.png, self.png, mask=mask_circle)

            # 흰색 탐지 (그레이스케일 변환)
            gray = cv2.cvtColor(cropped_circle, cv2.COLOR_BGR2GRAY)
            _, white_mask = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)

            # 화살표 모양의 컨투어 찾기
            arrow_contours, _ = cv2.findContours(white_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for arrow_contour in arrow_contours:
                # 화살표의 특징 분석: 꺾임과 모양
                approx = cv2.approxPolyDP(arrow_contour, 0.02 * cv2.arcLength(arrow_contour, True), True)
                if len(approx) != 7:  # 화살표는 다각형으로 간주
                    continue
                p = (center[0], center[1])

                if p[1] < 828: continue
                if factory_only and p[1] >= 1750: continue

                is_skill_arrow = 930 <= p[0] and 2120 <= p[1]
                if factory_only == is_skill_arrow:
                    continue

                ret.append( p )

        return ret

    def get_boxes(self):
        # 테두리 마스크 생성
        border_mask = cv2.inRange(self.png, box_lower_border, box_upper_border)
        # 민무늬 마스크 생성
        pattern_mask = cv2.inRange(self.png, box_lower_pattern, box_upper_pattern)

        # 테두리 컨투어 탐지
        contours, _ = cv2.findContours(border_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        ret = []

        # 조건에 맞는 상자 탐지
        for contour in contours:
            # 최소 외접 사각형 (회전 포함)
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)

            # 사각형의 너비와 높이 계산
            width = int(rect[1][0])
            height = int(rect[1][1])
            if width < 30 or height < 30:
                continue
            aspect_ratio = min(width, height) / max(width, height)  # 정사각형 유사성

            # 정사각형에 가까운지 확인
            if aspect_ratio < 0.8 or aspect_ratio > 1.2:
                continue

            # ROI 추출 (상자 내부)
            mask_box = np.zeros_like(border_mask)
            cv2.drawContours(mask_box, [box], -1, 255, -1)
            roi = cv2.bitwise_and(pattern_mask, pattern_mask, mask=mask_box)

            # 민무늬 탐지
            pattern_contours, _ = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            horizontal_rects = []
            vertical_rects = []

            for p_contour in pattern_contours:
                px, py, pw, ph = cv2.boundingRect(p_contour)
                if pw / ph > 2.0:  # 가로로 긴 직사각형만 추가
                    horizontal_rects.append((px, py, pw, ph))

            # 가로 긴 직사각형이 4개인지 확인
            if len(horizontal_rects) >= 2:
                sx, sy = box[0]
                ex, ey = box[0]
                for x,y in box:
                    sx = min(sx, x)
                    sy = min(sy, y)
                    ex = max(ex, x)
                    ey = max(ey, y)

                p = ((sx+ex)//2, (sy+ey)//2)

                if p[1] < 828 and (p[0] < 200 or p[0] > 840): continue
                if p[1] > 1768: continue

                ret.append(p)

        return ret