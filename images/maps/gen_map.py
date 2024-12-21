import json
from pathlib import Path

import cv2
from PIL import Image


BASE_PATH = Path(__file__).parent


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


def draw_rectangle_on_image(file_path, x, y, w, h, output_path):
    """
    Draws a rectangle on an image and saves the result.

    Parameters:
        file_path (str): Path to the input image.
        x (int): X-coordinate of the top-left corner of the rectangle.
        y (int): Y-coordinate of the top-left corner of the rectangle.
        w (int): Width of the rectangle.
        h (int): Height of the rectangle.
        output_path (str): Path to save the output image with the rectangle.

    Returns:
        bool: True if the process is successful, False otherwise.
    """
    try:
        # Load the image
        image = cv2.imread(str(file_path))
        if image is None:
            return False

        # Draw the rectangle
        top_left = (x, y)
        bottom_right = (x + w, y + h)
        color = (255, 0, 0)  # Green color in BGR
        thickness = 2  # Thickness of the rectangle
        cv2.rectangle(image, top_left, bottom_right, color, thickness)

        # Save the modified image
        cv2.imwrite(str(output_path), image)
        return True

    except Exception as e:
        return False

def parse_map_match(sub_dir: Path, info: dict):
    range_info = {
        "xy": [100, 800], "size": [600, 600]
    }
    if 'map_match' not in info:
        return

    d = info['map_match']

    if sub_dir.parent.name == '250':
        input_path = sub_dir / 'src' / 'map_250_0.png'
    else:
        input_path = sub_dir / 'src' / 'map.png'

    output_path = sub_dir / 'template' / 'match_map.png'
    output_path.parent.mkdir(parents=True, exist_ok=True)

    crop_and_save_image_with_alpha(
        input_path=input_path,
        output_path=output_path,
        offset_x=d['pos']['xy'][0],
        offset_y=d['pos']['xy'][1],
        width=d['pos']['size'][0],
        height=d['pos']['size'][1]
    )
    dummy = 200
    dl, dt = d['pos']['xy'][0] - dummy, d['pos']['xy'][1] - dummy
    dr, db = d['pos']['xy'][0] + d['pos']['size'][0] + dummy, d['pos']['xy'][1] + d['pos']['size'][1] + dummy
    dl = max(0, dl)
    dt = max(0, dt)

    range_info['xy'] = [dl, dt]
    range_info['size'] = [dr-dl, db-dt]

    out_info_file = output_path.with_suffix('.json')
    out_info_file.write_text(json.dumps(range_info))

def parse_factory(sub_dir: Path, info: dict):
    if 'map_match' not in info:
        return

    factory_info = info['factory']
    output_path = sub_dir / 'template' / 'factory.json'
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output = []

    idx = 0
    for d in factory_info:

        offset = d.get('offset', 0)
        sx, sy = d['pos']['xy']
        w, h = d['pos']['size']
        output.append(
            {
                'index': idx,
                'offset': offset,
                'pos': { 'xy': (sx, sy), 'size': (w, h)},
                'range': {'xy': (sx, sy), 'size': (w, h)},
            }
        )

        in_filepath = sub_dir / 'src' / f'top_{offset*400:04d}.png'
        out_filepath = sub_dir / 'template' / f'factory_{idx}_1.png'
        draw_rectangle_on_image(in_filepath, sx, sy, w, h, out_filepath)

        in_filepath = sub_dir / 'src' / f'top_{offset*400:04d}_completed.png'
        if in_filepath.exists():
            out_filepath = sub_dir / 'template' / f'factory_{idx}_2.png'
            draw_rectangle_on_image(in_filepath, sx, sy, w, h, out_filepath)

        idx += 1

    output_path.write_text(json.dumps(output))

def run():
    for size in [25, 50, 75, 150, 250]:
        size_dir = BASE_PATH / f"{size}"

        for sub_dir in size_dir.iterdir():

            if not sub_dir.is_dir(): continue
            prefix = f'{size:03d}_'
            if not sub_dir.name.startswith(prefix): continue

            info_json_filename = sub_dir / 'src' / 'info.json'
            if not info_json_filename.is_file():
                print(f"Not yet ready : {sub_dir.name}")
                continue

            info = json.loads(info_json_filename.read_text())
            parse_map_match(sub_dir, info)
            parse_factory(sub_dir, info)

if __name__ == '__main__':
    run()

    # return [d.name for d in Path(path).iterdir() if d.is_dir()]
# for d in data:
#     infile = BASE_PATH / 'images' / 'src' / d['src']
#     outfile = BASE_PATH / 'images' / 'templates' / d['dest']
#     info_file = outfile.with_suffix('.json')
#
#     if not infile.exists():
#         continue
#
#     crop_and_save_image_with_alpha(
#         input_path=infile,
#         output_path=outfile,
#         offset_x=d['pos']['xy'][0],
#         offset_y=d['pos']['xy'][1],
#         width=d['pos']['size'][0],
#         height=d['pos']['size'][1]
#     )
#     info_file.write_text(json.dumps(d['range']))
