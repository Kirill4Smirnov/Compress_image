import os
import glob
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

def compress_image(img_name, dest_path, scale = 0.9, quality = 90, to_JPG = True): #scale must be less than 1
    assert scale < 1.0, f"Scale must be less than 1, your scale is {scale}"

    img = Image.open(img_name)
    print("[*] Initial image shape: ", img.size)

    img_size = os.path.getsize(img_name)
    print("[*] Initial image size: ", get_size_format(img_size))

    img = img.resize((int(img.size[0] * scale), int(img.size[1] * scale)))
    print("[*] New image shape: ", img.size)

    filename, ext = os.path.splitext(img_name)

    if to_JPG:
        new_filename = f"{dest_path}{os.path.basename(filename)}_compressed.jpg"
    else:
        new_filename = f"{dest_path}{os.path.basename(filename)}_compressed{ext}"

    try:
        img.save(new_filename, quality=quality, optimize = True)
    except OSError:
        img = img.convert("RGB")
        img.save(new_filename, quality=quality, optimize = True)

    print("[+] New file saved: ", new_filename)

    new_img_size = os.path.getsize(new_filename)
    print("[+] New image size: ", get_size_format(new_img_size))

def get_latest_files(path, count = 1):
    list_of_files = glob.glob(path)

    latest_files = []

    for i in range(count):
        latest_files.append(max(list_of_files, key=os.path.getctime))

        list_of_files.remove(latest_files[i])
    return latest_files

def main():
    files = get_latest_files("/home/kenlog_new/Pictures/photos/*", count= 2)
    #print(files) #for debug

    for file in files:
        compress_image(file, scale=0.8, dest_path="/home/kenlog_new/Pictures/Compressed_images/")

if __name__ == '__main__':
    main()