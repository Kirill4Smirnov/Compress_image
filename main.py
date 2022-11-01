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

def compress_image(img_name, scale = 0.9, quality = 90, to_JPG = True): #scale must be less than 1
    assert scale < 1.0, f"Scale must be less than 1, your scale is {scale}"

    img = Image.open(img_name)
    print("[*] Initial image shape: ", img.size)

    img_size = os.path.getsize(img_name)
    print("[*] Initial image size: ", get_size_format(img_size))

    img = img.resize((int(img.size[0] * scale), int(img.size[1] * scale)))
    print("[*] New image shape: ", img.size)

    filename, ext = os.path.splitext(img_name)

    if to_JPG:
        new_filename = f"{filename}_compressed.jpg"
    else:
        new_filename = f"{filename}_compressed{ext}"

    try:
        img.save(new_filename, quality=quality, optimize = True)
    except OSError:
        img = img.convert("RGB")

        img.save(new_filename, quality=quality, optimize = True)
    print("[+] New file saved: ", new_filename)

    new_img_size = os.path.getsize(new_filename)
    print("[+] New image size: ", get_size_format(new_img_size))

def main():
    compress_image("/home/kenlog_new/Pictures/Screenshots/Screenshot from 2022-10-11 14-29-50.png")

if __name__ == '__main__':
    main()