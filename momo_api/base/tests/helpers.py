from PIL import Image

from momo_api.base.utils import get_pil_image_as_django_content_file


def create_test_image(filename='test.png', size=(160, 160), color='blue'):
    """
    Create and return a test image as a ContentFile
    """
    image = Image.new('RGBA', size, color)
    image_content_file = get_pil_image_as_django_content_file(image, 'png')
    image_content_file.name = filename
    return image_content_file
