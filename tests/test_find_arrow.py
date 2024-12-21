from pathlib import Path

import cv2
import numpy as np
import pytest

from images import Img

BASE_PATH = Path(__file__).parent.parent

@pytest.mark.parametrize('img_filepath', [
    BASE_PATH / 'tests' / 'top_2000.png'
])
def test_find_arrow(img_filepath):
    # 이미지 읽기
    img = Img(img_filepath)
    factory = img.get_pos_upgrade_arrow(True, True, False)
    # skill  = img.get_pos_upgrade_arrow(False)

    result = img.png.copy()

    for p in factory:
        cv2.circle(result, p, 30, (255, 0, 0), 2)  # 원 강조

    cv2.imwrite('result.png', result)


@pytest.mark.parametrize('img_filepath', [
    BASE_PATH / 'images' / 'src' / 'boxes.png'
])
def test_find_boxes(img_filepath):
    # 이미지 읽기
    image = cv2.imread(str(img_filepath))

    # 색상 범위 설정 (테두리 색과 민무늬 색)
    tolerance = 20

    # 테두리 색 (#AA7345)
    border_color = np.array([69, 115, 170])  # BGR
    lower_border = np.clip(border_color - tolerance, 0, 255)
    upper_border = np.clip(border_color + tolerance, 0, 255)

    # 민무늬 색 (#FFE18A)
    pattern_color = np.array([138, 225, 255])  # BGR
    lower_pattern = np.clip(pattern_color - tolerance, 0, 255)
    upper_pattern = np.clip(pattern_color + tolerance, 0, 255)

    # 테두리 마스크 생성
    border_mask = cv2.inRange(image, lower_border, upper_border)

    # 민무늬 마스크 생성
    pattern_mask = cv2.inRange(image, lower_pattern, upper_pattern)

    # 테두리 컨투어 탐지
    contours, _ = cv2.findContours(border_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 결과 이미지 복사본 생성
    result = image.copy()

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
            print("조건에 맞는 나무 상자를 찾았습니다!")
            print(box)
            cv2.drawContours(result, [box], -1, (0, 255, 0), 2)  # 상자 강조
            for r in horizontal_rects:
                cv2.rectangle(result, (r[0], r[1]), (r[0] + r[2], r[1] + r[3]), (255, 0, 0), 2)

    # 결과 이미지 저장
    cv2.imwrite('result.png', result)
