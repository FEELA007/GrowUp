import cv2


def process_image(image, denoise_value, sharpen_value, deblur_value):
    image = image.copy()

    if denoise_value > 0:
        strength = max(1, denoise_value // 10)
        image = cv2.fastNlMeansDenoisingColored(
            image, None, strength, strength, 7, 21
        )

    if sharpen_value > 0:
        amount = sharpen_value / 100.0
        blurred = cv2.GaussianBlur(image, (0, 0), 3)
        image = cv2.addWeighted(image, 1.0 + amount, blurred, -amount, 0)

    if deblur_value > 0:
        amount = deblur_value / 100.0
        blurred = cv2.GaussianBlur(image, (0, 0), 2)
        image = cv2.addWeighted(image, 1.0 + amount, blurred, -amount, 0)

    return image