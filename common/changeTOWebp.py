# -*- coding: utf-8 -*-
import glob
import os
import threading

from PIL import Image


def create_image(infile, index):
  os.path.splitext(infile)
  im = Image.open(infile)
  print infile
  print index
  im.save("wepy/webp_" + str(index) + ".webp", "WEBP")


def start():
  index = 0
  for infile in glob.glob("20140526190812/*.jpg"):
    t = threading.Thread(target=create_image, args=(infile, index,))
    t.start()
    t.join()
    index += 1


if __name__ == "__main__":
  start()