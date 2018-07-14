# -*- coding: utf-8 -*-
from glob import glob
import os
from  threading import Thread

import logging
from PIL import Image


logging.basicConfig(
    level=logging.DEBUG,
    format=
    '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    )

def convert_img_type(infile, index):

  encoder_path = "C:/Users/ruonan/libwebp-1.0.0-windows-x64/bin/cwebp.exe"
  output_path = "C:/Test01/20150806205033/webp/"
  if not os.path.exists(output_path):
    os.mkdir(output_path)
  new_size = get_new_size(infile)
  commond = encoder_path + " -q 80 -resize " + str(new_size[0]) + " " + str(new_size[1]) + " " +infile + " -o "+output_path + str(index) + ".webp"
  logging.debug(commond)
  os.system(commond)


def get_new_size(infile):
  img = Image.open(infile)
  width = img.size[0]
  height = img.size[1]
  phone_px = 500
  scale = float(phone_px) / width
  if width <= phone_px:
    return width,height
  else:
    height = int(height * scale)
  return phone_px, height

def start():
  index = 1
  input_path = "C:/Test01/20150806205033/*.jpg"
  for infile in glob(input_path):
    print infile
    t = Thread(target=convert_img_type, args=(infile, index,))
    t.start()
    t.join()
    index += 1


if __name__ == "__main__":
  start()