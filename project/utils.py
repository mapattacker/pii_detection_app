import os

import cv2


def delete_all_images(out_folder="output",format=("jpg", "jpeg", "png")):
    for i in os.listdir(out_folder):
        if i.endswith(format):
            img_path = os.path.join(out_folder, i)
            os.remove(img_path)


def label_image_pii(image_path, coord_list, pii_types,
        output_folder="output",
        font_size=0.2):
    """draw and label pii detected in image"""
    im = cv2.imread(image_path)
    height, width, _ = im.shape

    # coordinates for rect
    for coord, pii_type in zip(coord_list, pii_types):
        top = int(coord[0]["X"] * width)
        left = int(coord[0]["Y"] * height)
        bottom = int(coord[2]["X"] * width)
        right = int(coord[2]["Y"] * height)

        cv2.rectangle(im, pt1=(top, left), pt2=(bottom, right), \
                        color=(0,255,0), thickness=1)
        cv2.putText(im, pii_type, (top+2, left),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    font_size, (0, 0, 255), 1,
                    cv2.LINE_AA)

    output_path = os.path.join(output_folder, image_path.split("/")[-1])
    cv2.imwrite(output_path, im)
