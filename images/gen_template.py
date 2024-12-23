import json
from pathlib import Path

from PIL import Image


BASE_PATH = Path(__file__).parent.parent


def crop_and_save_image_with_alpha(input_path, output_path, offset_x, offset_y, width, height):
    """
    알파 채널을 유지하면서 PNG 파일을 지정된 오프셋과 크기로 잘라서 저장합니다.

    :param input_path: 원본 이미지 경로
    :param output_path: 저장할 이미지 경로
    :param offset_x: 자를 이미지의 시작 X 좌표
    :param offset_y: 자를 이미지의 시작 Y 좌표
    :param width: 잘라낼 이미지의 폭
    :param height: 잘라낼 이미지의 높이
    """
    try:
        # 이미지 열기 (알파 채널 포함)
        with Image.open(input_path).convert("RGBA") as img:
            # 잘라낼 영역 정의 (left, top, right, bottom)
            box = (offset_x, offset_y, offset_x + width, offset_y + height)
            cropped_img = img.crop(box)

            # 잘라낸 이미지 저장 (PNG 형식)
            cropped_img.save(output_path, format="PNG")
            print(f"이미지가 성공적으로 저장되었습니다: {output_path}")
    except Exception as e:
        print(f"오류 발생: {e}")

data = [
    {
        'src' : "skill_upgrade_active.png",
        'dest' : "skill_upgrade_1.png",
        'pos': {
            'xy': (911, 2128),
            'size': (66, 72),
        },
        'range': {
            'xy': (866, 2064),
            'size': (194, 171),
        },
    },
    {
        'src' : "skill_upgrade_active.png",
        'dest' : "menu_gear_1.png",
        'pos': {
            'xy': (952, 76),
            'size': (93, 92),
        },
        'range': {
            'xy': (938, 65),
            'size': (130, 115),
        }
    },
    {
        'src' : "skill_upgrade_active.png",
        'dest' : "factory_open_1.png",
        'pos': {
            'xy': (185, 1275),
            'size': (27, 31),
        },
        'range': {
            'xy': (0, 814),
            'size': (1080, 1058),
        }
    },
    {
        'src' : "away.png",
        'dest' : "away_x_button.png",
        'pos': {
            'xy': (894, 666),
            'size': (40, 45),
        },

        'range': {
            'xy': (0, 14),
            'size': (1080, 1858),
        }
    },
    {
        'src' : "offline_earn.png",
        'dest' : "offline_earn_x_button.png",
        'pos': {
            'xy': (810, 818),
            'size': (111, 90),
        },
        'range': {
            'xy': (794, 801),
            'size': (142, 138),
        }
    },
    {
        'src' : "factory_unlock.png",
        'dest' : "factory_unlock_text.png",
        'pos': {
            'xy': (704, 1446),
            'size': (195, 59),
        },
        'range': {
            'xy': (0, 210),
            'size': (1077, 1911),
        },
    },
    {
        'src' : "factory_unlock.png",
        'dest' : "factory_unlock_gold.png",
        'pos': {
            'xy': (695, 1551),
            'size': (57, 58),
        },
        'range': {
            'xy': (0, 500),
            'size': (1080, 1800),
        },
    },
    {
        'src' : "boxes.png",
        'dest' : "boxes.png",
        'pos': {
            'xy': (674, 1692),
            'size': (91, 79),
        },
        'range': {
            'xy': (0, 210),
            'size': (1077, 1911),
        }
    },
    {
        'src' : "factory_upgrade_gold.png",
        'dest' : "factory_upgrade_gold_active.png",
        'pos': {
            'xy': (701, 1531),
            'size': (60, 100),
        },
        'range': {
            'xy': (0, 210),
            'size': (1077, 1911),
        },
    },
    {
        'src' : "factory_upgrade_gold_2.png",
        'dest' : "factory_upgrade_gold_deactive.png",
        'pos': {
            'xy': (701, 1531),
            'size': (60, 100),
        },
        'range': {
            'xy': (0, 210),
            'size': (1077, 1911),
        },
    },
    {
        'src' : "factory_upgrade_complete.png",
        'dest' : "factory_upgrade_complete.png",
        'pos': {
            'xy': (198, 1515),
            'size': (152, 83),
        },
        'range': {
            'xy': (0, 210),
            'size': (1077, 1911),
        },
    },
    {
        'src' : "next_stage_1.png",
        'dest' : "next_stage_can_go.png",
        'pos': {
            'xy': (51, 2131),
            'size': (118, 116),
        },
        'range': {
            'xy': (3, 2094),
            'size': (193, 190),
        }
    },
    {
        'src' : "next_stage_2.png",
        'dest' : "next_stage_can_go_2.png",
        'pos': {
            'xy': (51, 2131),
            'size': (118, 116),
        },
        'range': {
            'xy': (3, 2094),
            'size': (193, 190),
        }
    },
    { #
        'src' : "next_stage_remodeling.png",
        'dest' : "next_stage_remodeling.png",
        'pos': {
            'xy': (404, 1636),
            'size': (69, 67),
        },
        'range': {
            'xy': (280, 1574),
            'size': (526, 202),
        }
    },
    { #
        'src' : "next_stage_remodeling_2.png",
        'dest' : "next_stage_remodeling_2.png",
        'pos': {
            'xy': (481, 1600),
            'size': (120, 80),
        },
        'range': {
            'xy': (238, 1507),
            'size': (575, 241),
        }
    },

    {  # wait  3~5 seconds
        'src': "next_stage_new.png",
        'dest': "next_stage_new.png",
        'pos': {
            'xy': (466, 1337),
            'size': (144, 93),
        },
        'range': { 'xy': (84, 707), 'size': (926, 1084), }
    },
    { # wait  3~5 seconds
        'src' : "next_stage_new_2.png",
        'dest' : "next_stage_new_2.png",
        'pos': {
            'xy': (453, 1443),
            'size': (167, 65),
        },
        'range': { 'xy': (84, 707), 'size': (926, 1084), }
    },
    {
        'src' : "google_ad.png",
        'dest' : "ad_min.png",
        'pos': {
            'xy': (503, 2297),
            'size': (25, 28),
        },
        'range': {'xy': (198, 2263), 'size': (700, 76)}
    },
    {
        'src' : "google_ad.png",
        'dest' : "ad_sec.png",
        'pos': {
            'xy': (568, 2296),
            'size': (27, 27),
        },
        'range': {'xy': (198, 2263), 'size': (700, 76)}
    },
    {
        'src' : "google_ad_skip.png",
        'dest' : "ad_skip_1.png",
        'pos': {
            'xy': (70, 143),
            'size': (34, 20),
        },
        'range': {'xy': (24, 18), 'size': (1045, 200)}
    },
    {
        'src' : "google_ad_skip_2.png",
        'dest' : "ad_skip_2.png",
        'pos': {
            'xy': (991, 123),
            'size': (42, 42),
        },
        'range': {'xy': (24, 18), 'size': (1045, 200)}
    },
    {
        'src' : "google_ad_skip_3.png",
        'dest' : "ad_skip_3.png",
        'pos': {
            'xy': (994, 122),
            'size': (50, 31),
        },
        'range': {'xy': (24, 18), 'size': (1045, 200)}
    },
    {
        'src' : "google_ad_skip_4.png",
        'dest' : "ad_skip_4.png",
        'pos': {
            'xy': (990, 125),
            'size': (40, 40),
        },
        'range': {'xy': (24, 18), 'size': (1045, 200)}
    },
    {
        'src' : "google_ad_exit_1.png",
        'dest' : "ad_exit_1.png",
        'pos': {
            'xy': (977, 143),
            'size': (37, 36),
        },
        'range': {'xy': (24, 18), 'size': (1045, 200)}
    },
    {
        'src' : "google_ad_exit_2.png",
        'dest' : "ad_exit_2.png",
        'pos': {
            'xy': (997, 102),
            'size': (55, 59),
        },
        'range': {'xy': (24, 18), 'size': (1045, 200)}
    },
    {
        'src' : "google_ad_exit_3.png",
        'dest' : "ad_exit_3.png",
        'pos': {
            'xy': (978, 157),
            'size': (34, 29),
        },
        'range': {'xy': (24, 18), 'size': (1045, 200)}
    },
    {
        'src' : "google_ad_exit_4.png",
        'dest' : "ad_exit_4.png",
        'pos': {
            'xy': (1016, 108),
            'size': (27, 27),
        },
        'range': {'xy': (24, 18), 'size': (1045, 200)}
    },

    {
        'src': "google_ad_miss_click.png",
        'dest': "google_miss_click.png",
        'pos': {
            'xy': (997, 2248),
            'size': (47, 54),
        },
        'range': {
            'xy': (930, 2199),
            'size': (145, 143),
        }
    },
    {
        'src' : "map_250.png",
        'dest' : "map_250.png",
        'pos': {
            'xy': (615, 1688),
            'size': (68, 36),
        },
        'range': {'xy': (400, 1485), 'size': (500, 400),}
    },
    {
        'src' : "map_150.png",
        'dest' : "map_150.png",
        'pos': {
            'xy': (680, 1726),
            'size': (59, 33),
        },
        'range': {'xy': (400, 1485), 'size': (500, 400),}
    },
    {
        'src' : "map_75.png",
        'dest' : "map_75.png",
        'pos': {
            'xy': (689, 1727),
            'size': (40, 30),
        },
        'range': {'xy': (400, 1485), 'size': (500, 400),}
    },
    {
        'src' : "map_50.png",
        'dest' : "map_50.png",
        'pos': {
            'xy': (689, 1727),
            'size': (40, 30),
        },
        'range': {'xy': (400, 1485), 'size': (500, 400),}
    },
    {
        'src' : "map_25.png",
        'dest' : "map_25.png",
        'pos': {
            'xy': (689, 1727),
            'size': (40, 30),
        },
        'range': {'xy': (400, 1485), 'size': (500, 400),}
    },
    {
        'src' : "map_flow.png",
        'dest' : "map_flow_empty.png",
        'pos': {
            'xy': (355, 505),
            'size': (80, 60),
        },
        'range': {'xy': (0, 200), 'size': (1080, 2100),}
    },
    {
        'src' : "active_skill_2.png",
        'dest' : "active_skill_select.png",
        'pos': {
            'xy': (743, 1155),
            'size': (174, 60),
        },
        'range': {'xy': (15, 252), 'size': (1065, 1608),}
    },
    {
        'src' : "active_skill_3.png",
        'dest' : "active_skill_select_text.png",
        'pos': {'xy': (320, 896), 'size': (346, 81)},
        'range': {'xy': (15, 252), 'size': (1065, 1608),}
    },
]

for d in data:
    infile = BASE_PATH / 'images' / 'src' / d['src']
    outfile = BASE_PATH / 'images' / 'templates' / d['dest']
    info_file = outfile.with_suffix('.json')

    if not infile.exists():
        continue

    crop_and_save_image_with_alpha(
        input_path=infile,
        output_path=outfile,
        offset_x=d['pos']['xy'][0],
        offset_y=d['pos']['xy'][1],
        width=d['pos']['size'][0],
        height=d['pos']['size'][1]
    )
    info_file.write_text(json.dumps(d['range']))
