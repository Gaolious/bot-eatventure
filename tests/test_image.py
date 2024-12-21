import itertools
import os
from pathlib import Path
from unittest import mock

import cv2
import pytest

from auto import AutoHelper
from images import Img

BASE_PATH = Path(__file__).parent.parent.absolute()

@pytest.fixture(scope='function')
def mock_dm():
    with mock.patch('auto.DeviceManager') as dm:
        yield dm

@pytest.fixture(scope='function')
def mock_screenshot():
    with mock.patch('auto.AutoHelper.screenshot') as dm:
        yield dm

@pytest.fixture(scope='function')
def mock_sleep():
    with mock.patch('auto.sleep') as dm:
        yield dm

@pytest.mark.parametrize('dt', [
    '20241206_101217'
])
def test_capture(dt, mock_dm, mock_sleep, mock_screenshot):

    directory_path = BASE_PATH / 'work' / dt
    png_images = [f for f in os.listdir(directory_path) if f.endswith('.png')]

    mock_screenshot.side_effect = itertools.cycle([
        Img(directory_path / png) for png in png_images
    ])

    helper = AutoHelper('')
    helper.template.load_templates()
    helper.main_logic()


@pytest.mark.parametrize('img_filepath', [
    # BASE_PATH / 'work' / '20241206_141932' / '20241206_142003.png',
    BASE_PATH / 'work' / '20241212_164106' / '20241212_164847.png',

    # BASE_PATH / 'work' / '20241206_130847' / '20241206_130904.png',
    # BASE_PATH / 'work' / '20241206_130847' / '20241206_130919.png',
])
def test_find_all(img_filepath, mock_dm, mock_sleep, mock_screenshot):
    helper = AutoHelper('')
    helper.template.load_templates()
    img = Img(img_filepath)

    ans = []
    print(f'\n{img_filepath}')
    for key in helper.template.templates.keys():
        s = ['\t']
        for attr in ['png', 'gray', 'hsv']:
            b, result = helper.template._has_template(attr, key, (img, img))
            s.append( f'{result.results[0].ratio:0.3f}' if b else f'  x  ' )
            if b:
                x, y, w, h = result.results[0].left, result.results[0].top, result.results[0].right - result.results[0].left, result.results[0].bottom - result.results[0].top
                image = getattr(img, attr)
                crop = image[y:y + h, x:x + w]

                outpath = img_filepath.parent / f'{img_filepath.name}_{attr}_{key}.png'
                cv2.imwrite(str(outpath), crop)

        s += [key]

        ans.append(' '.join(s))
    print('\n'.join(ans))

@pytest.mark.parametrize('img_filepath', [
    BASE_PATH / 'work' / '20241209_061843' / '20241209_061855.png',
    # BASE_PATH / 'work' / '20241206_130847' / '20241206_130904.png',
    # BASE_PATH / 'work' / '20241206_130847' / '20241206_130919.png',
])
def test_find_img(img_filepath, mock_dm, mock_sleep, mock_screenshot):
    helper = AutoHelper('')
    helper.template.load_templates()
    img = Img(img_filepath)

    helper.template.has_upgradable_food_factory_icon(img)
    helper.template.has_buy_food_factory_coin(img)
