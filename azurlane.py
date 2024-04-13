import cv2
import numpy as np
import adb_utils


def ensure_image(img):
    img = img.astype("float32")
    if len(img.shape) > 2:
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img


def is_at_login_screen(img):
    # Check if the image is at the login screen
    # This is done by checking if the image matches the template at ./picture_templates/login.png
    template = cv2.imread("./picture_templates/login.png", 0)
    template, img = ensure_image(template), ensure_image(img)
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val > 0.9:
        return True
    else:
        return False


def tag_login_template(img):
    # Tag the login template on the image
    # This is done by finding the template at ./picture_templates/login.png and drawing a rectangle around it
    template = cv2.imread("./templates/login.png", 0)
    template, img = ensure_image(template), ensure_image(img)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

    threshold = 0.8
    loc = np.where(res >= threshold)

    for pt in zip(*loc[::-1]):  # 逆序遍历找到的位置
        cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)
    return img


if __name__ == "__main__":
    img = cv2.imread("test_images/login.png")
    result = tag_login_template(img)
    cv2.imshow("result", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
