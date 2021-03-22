import sys

from PIL import Image
from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile


def compress_image(image, max_res: int = 1024):
    """
    Compressing given image file according max image side.

    :param image: ImageFieldFile object
    :param max_res: int value of max image resolution (default - 1024)
    """
    temp_image = Image.open(image)
    io_stream = BytesIO()
    max_side = max(temp_image.size)

    if max_side > max_res:
        ratio = temp_image.height / temp_image.width
        if temp_image.width != max_side:
            new_height = max_res
            new_width = int(new_height / ratio)
        else:
            new_width = max_res
            new_height = int(new_width * ratio)
        temp_image = temp_image.resize((new_width, new_height))

    temp_image.save(io_stream, format='JPEG', quality=60)
    io_stream.seek(0)
    image_name = image.name.split('.')[0]
    extension = '.jpg'
    upload_image = InMemoryUploadedFile(io_stream,
                                        'ImageField',
                                        f'{image_name}{extension}',
                                        'image/jpeg',
                                        sys.getsizeof(io_stream),
                                        None)
    return upload_image
