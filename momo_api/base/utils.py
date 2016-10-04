import os
from cStringIO import StringIO

from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile


def get_pil_image_as_django_content_file(pil_image, image_format):
    """
    Return the given PIL Image as a Django ContentFile.
        image = generate_some_image_with_pil()
        image_format = 'png'
        image_as_django_content_file = get_pil_image_as_string(image, image_format)
        storage.save('some/path/', image_as_django_content_file)
    """
    # PIL does not handle jpg
    if image_format.lower() == 'jpg':
        image_format = 'jpeg'

    try:
        img_io = StringIO()
        pil_image.save(img_io, image_format)
        img_data = img_io.getvalue()
        return ContentFile(img_data)
    finally:
        img_io.close()


def get_static_asset_path(directory_name, file_name):
    """
    Get filepath for a static asset located in the static root
    """
    static_root_path = settings.STATIC_ROOT
    file_path = '{}{}'.format(directory_name, file_name)
    return os.path.join(static_root_path, file_path)


def open_image_file(image_file_path):
    """
    Open an image file from the given image filepath
    """
    return File(open(image_file_path, 'r'))
