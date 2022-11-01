import os
from PIL import Image

def get_size_format(val, factor = 1024, suffix = 'B'):
    """
       Scale bytes to its proper byte format
       e.g:
           1253656 => '1.20MB'
           1253656678 => '1.17GB'
       """

    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if val < factor:
            return f"{val:.2f}{unit}{suffix}"
        val /= factor
    return f"{val:.2f}E{suffix}"

print(get_size_format(1253656))