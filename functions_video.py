import cv2
import numpy
from tqdm import tqdm

from logger import logger


def add_object_to_background(background, overlay, x, y):
    background_width = background.shape[1]
    background_height = background.shape[0]

    if x >= background_width or y >= background_height:
        return background

    h, w = overlay.shape[0], overlay.shape[1]

    if x + w > background_width:
        w = background_width - x
        overlay = overlay[:, :w]

    if y + h > background_height:
        h = background_height - y
        overlay = overlay[:h]

    if overlay.shape[2] < 4:
        overlay = numpy.concatenate(
            [
                overlay,
                numpy.ones((overlay.shape[0], overlay.shape[1], 1), dtype=overlay.dtype) * 255
            ],
            axis=2,
        )

    overlay_image = overlay[..., :3]
    mask = overlay[..., 3:] / 255.0

    background[y:y+h, x:x+w] = (1.0 - mask) * background[y:y+h, x:x+w] + mask * overlay_image
    cv2.imwrite('combined2.png', background)

    return background


def load_required_objects(objects_dict, objects_list):
    required_objects = []
    for class_name, count in objects_dict.items():
        temp_counter = 0
        for curr_obj in objects_list:
            if curr_obj.class_name == class_name:
                required_objects.append(curr_obj)
                temp_counter += 1
                if temp_counter == count:
                    break

    if len(required_objects) > 0:
        return required_objects
    else:
        logger.warning('cannot find any fitting objects to generate video')
        raise ValueError('objects is missing')


def generate_frames(fps, background, temp_objects, movement_law, speed_interval):
    ###
    frames = []
    for counter in range(3000):
        frames.append(add_object_to_background(background.copy(), temp_objects[1].image, counter, counter))

    pass


def write_frames_to_file(video_name, fps, frames, video_shape):
    ###
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # print(self.backgrounds[0].shape[:2])
    video = cv2.VideoWriter('test2.mp4', fourcc, 60, video_shape)

    for frame in tqdm(frames):
        video.write(frame)

    video.release()



