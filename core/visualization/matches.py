

import cv2
import matplotlib.cm as cm
import numpy as np


def show_image_pair_matching(image0, image1,
                             kpts0, kpts1,
                             mkpts0, mkpts1,
                             color=None, text=None,
                             path=None,
                             show_keypoints=False, margin=10,
                             opencv_display=False, opencv_title='matches',
                             small_text=[]):
    """Show image pair with matches"""

    # pair shapes
    H0, W0, _ = image0.shape
    H1, W1, _ = image1.shape
    H, W = max(H0, H1), W0 + W1 + margin

    # out image
    img = np.ones((H, W, 3), np.uint8)
    img[:H0, :W0, :] = image0
    img[:H1, W0+margin:, :] = image1

    if show_keypoints:
        kpts0, kpts1 = np.round(kpts0).astype(int), np.round(kpts1).astype(int)
        white = (255, 255, 255)
        black = (0, 0, 0)
        
        for x, y in kpts0:
            cv2.circle(img, (x, y), 2, black, -1, lineType=cv2.LINE_AA)
            cv2.circle(img, (x, y), 1, white, -1, lineType=cv2.LINE_AA)
        
        for x, y in kpts1:
            cv2.circle(img, (x + margin + W0, y), 2, black, -1,
                       lineType=cv2.LINE_AA)
            cv2.circle(img, (x + margin + W0, y), 1, white, -1,
                       lineType=cv2.LINE_AA)

    mkpts0, mkpts1 = np.round(mkpts0).astype(int), np.round(mkpts1).astype(int)
    color = (np.array(color[:, :3])*255).astype(int)[:, ::-1]
    for (x0, y0), (x1, y1), c in zip(mkpts0, mkpts1, color):
        c = c.tolist()
        cv2.line(img, (x0, y0), (x1 + margin + W0, y1),
                 color=c, thickness=1, lineType=cv2.LINE_AA)
        # display line end-points as circles
        cv2.circle(img, (x0, y0), 2, c, -1, lineType=cv2.LINE_AA)
        cv2.circle(img, (x1 + margin + W0, y1), 2, c, -1,
                   lineType=cv2.LINE_AA)

    # Scale factor for consistent visualization across scales.
    sc = min(H / 640., 2.0)

    # Big text.
    Ht = int(30 * sc)  # text height
    txt_color_fg = (255, 255, 255)
    txt_color_bg = (0, 0, 0)
    for i, t in enumerate(text):
        cv2.putText(img, t, (int(8*sc), Ht*(i+1)), cv2.FONT_HERSHEY_DUPLEX,
                    1.0*sc, txt_color_bg, 2, cv2.LINE_AA)
        cv2.putText(img, t, (int(8*sc), Ht*(i+1)), cv2.FONT_HERSHEY_DUPLEX,
                    1.0*sc, txt_color_fg, 1, cv2.LINE_AA)

    # Small text.
    Ht = int(18 * sc)  # text height
    for i, t in enumerate(reversed(small_text)):
        cv2.putText(img, t, (int(8*sc), int(H-Ht*(i+.6))), cv2.FONT_HERSHEY_DUPLEX,
                    0.5*sc, txt_color_bg, 2, cv2.LINE_AA)
        cv2.putText(img, t, (int(8*sc), int(H-Ht*(i+.6))), cv2.FONT_HERSHEY_DUPLEX,
                    0.5*sc, txt_color_fg, 1, cv2.LINE_AA)

    if path is not None:
        cv2.imwrite(str(path), img)

    if opencv_display:
        cv2.imshow(opencv_title, img)
        # wait one second or pressed key
        if cv2.waitKey(500) & 0xFF == ord('q'):
            cv2.destroyAllWindows()

    return img

# TODO: fix plot matches and make it work with the new show_image_pair_matching
def plot_matches(image0, image1, kpts0, kpts1, mkpts0, mkpts1, scores,
                 scale0=None, scale1=None,
                 **kwargs):
    """Plot matches between two images"""

    if scale0 is None:
        scale0 = np.ones(2)

    if scale1 is None:
        scale1 = np.ones(2)

    # scale
    kpts0 = kpts0 / scale0
    kpts1 = kpts1 / scale1
    #
    mkpts0 = mkpts0 / scale0
    mkpts1 = mkpts1 / scale1

    # txt and colors
    color = cm.jet(scores)
    text = ['kpts: {}:{}'.format(len(kpts0), len(
        kpts1)), 'matches: {}'.format(len(mkpts0))]

    # plot
    show_image_pair_matching(image0, image1,
                             kpts0, kpts1,
                             mkpts0, mkpts1,
                             color=color, text=text,
                             path=None,
                             show_keypoints=True, opencv_display=True)
