
import cv2


def show_cv_image(image, window_name='image', wait_time=0):
    """Show image using Opencv"""
    # show image
    cv2.imshow(window_name, image)

    # wait for key press to close window
    if cv2.waitKey(wait_time) & 0xFF == ord('q'):
        cv2.destroyAllWindows()


def draw_keypoints(image, keypoints, color=(0, 255, 0)):
    """Draw keypoints on image"""

    if len(keypoints) == 0:
        return image

    # draw keypoints
    for x, y in keypoints:
        cv2.circle(image, (int(x), int(y)), 1, color, 1, lineType=cv2.LINE_AA)

    return image


def show_cv_image_keypoints(image, keypoints, window_name="image", wait_time=0, **kwargs):
    """Show image with keypoints"""

    # convert to BGR
    if image.shape[-1] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    elif image.shape[-1] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
    elif image.shape[-1] == 1:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    # draw keypoints
    image = draw_keypoints(image, keypoints, **kwargs)

    # add text
    if 'text' in kwargs:
        text = kwargs['text']
    else:
        text = "keypoints: {}".format(len(keypoints))
        cv2.putText(image, text, (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (128, 0, 128),
                    1, cv2.LINE_AA)
    # show image
    cv2.imshow(window_name, image)

    # wait for key press to close window
    if cv2.waitKey(wait_time) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
