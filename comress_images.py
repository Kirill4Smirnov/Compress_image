import os
import sys

sys.path.append('/home/kenlog/PycharmProjects/scripts/compress_image')

import glob
from PIL import Image


count = 1
source_folder = "/run/user/1000/gvfs/mtp:host=Xiaomi_Redmi_Note_10_Pro_fb31e353/Внутренний общий накопитель/DCIM/Camera/*"
dest_folder = "/home/kenlog/Pictures/Compressed_images/"
scale = 0.9
rotate = ''

def get_size_format(val, factor=1024, suffix='B'):
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

def compress_image(img_name, dest_path, scale=0.9, quality=90, to_JPG=True, rotate_dir = '', quiet= False):
    """
        scale must be less than 1
        also rotates an image if it is horizontally-oriented
        (for rotate_dir: '' stands for no rotation, '+' for anti-clockwise, '-' for clockwise.
        'a' is automatic mode, rotates by 90 deg if img.size[0] > img.size[1])
    """
    assert scale < 1.0, f"Scale must be less than 1, your scale is {scale}"

    img = Image.open(img_name)
    print("[*] Initial image shape: ", img.size)

    if rotate_dir == 'a':
        if img.size[0] > img.size[1]:
            img = img.transpose(Image.Transpose.ROTATE_90)
    elif rotate_dir == '-':
        img = img.transpose(Image.Transpose.ROTATE_90)
    elif rotate_dir == '+':
        img = img.rotate(270, expand=True)
    elif rotate_dir == '':
        pass

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
        img.save(new_filename, quality=quality, optimize=True)
    except OSError:
        img = img.convert("RGB")
        img.save(new_filename, quality=quality, optimize=True)

    print("[+] New file saved: ", new_filename)

    new_img_size = os.path.getsize(new_filename)
    print("[+] New image size: ", get_size_format(new_img_size))

    if not quiet:
        img.show()


def get_latest_files(path, count=1):
    list_of_files = glob.glob(path)

    latest_files = []

    for i in range(count):
        latest_files.append(max(list_of_files, key=os.path.getctime))

        list_of_files.remove(latest_files[i])
    return latest_files

def check_args(): #change preferences according to sys.argv
    global source_folder
    global dest_folder
    global count
    global scale
    global rotate
    global quiet

    args = sys.argv
    #print(args) #for debug

    if ("-c" in args):
        c_index = args.index('-c')
        count = int(args[c_index + 1])

    if ("--count" in args):
        c_index = args.index('--count')
        count = int(args[c_index + 1])

    if "-d" in args:
        d_index = args.index('-d')
        dest_folder = args[d_index + 1]

    if "--destination" in args:
        d_index = args.index('--destination')
        dest_folder = args[d_index + 1]

    if "-s" in args:
        s_index = args.index('-s')
        source_folder = args[s_index + 1]

        if '*' not in source_folder:
            source_folder = source_folder + "*"

    if "--source" in args:
        s_index = args.index('--source')
        source_folder = args[s_index + 1]

        if '*' not in source_folder:
            source_folder = source_folder + "*"

    if "-S" in args:
        S_index = args.index("-S")
        scale = args[S_index + 1]

    if "--scale" in args:
        S_index = args.index("--scale")
        scale = args[S_index + 1]

    if "-r" in args:
        r_index = args.index("-r")
        rotate = args[r_index + 1]

    if "--rotate" in args:
        r_index = args.index("--rotate")
        rotate = args[r_index + 1]

    if "-q" in args:
        q_index = args.index("-q")
        quiet =True

    if "--quiet" in args:
        q_index = args.index("--quiet")
        quiet = True

    if ("--help" in args) or ("-h" in args):
        print("""
        Image compression utility, compresses N latest images in directory SOURCE, saves in DEST directory

        Params:
        -c or --count: set N number (1 by default)
        -d or --destination: set DEST directory
        -s or --source: set SOURCE
        -S or --scale: set scale of resizing (from 0.0 to 1.0)
        -r or --rotate: rotate all the images following the pattern:
            - is 90 degrees clockwise
            + 90 degrees counterclockwise
            a is automatic mode, which rotates the image so that it becomes vertical
        -q or --quiet: disable showing image after conversion
        
        By Kenlog
        """)
        sys.exit(0)

def main():
    check_args()

    print("Source folder is ", source_folder)

    files = get_latest_files(source_folder, count=count)
    # print(files) #for debug

    for file in files:
        print("Compressing file: ", file)
        compress_image(file, scale=scale, dest_path=dest_folder, rotate_dir=rotate, quiet = quiet)


if __name__ == '__main__':
    main()
