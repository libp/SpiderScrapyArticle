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

def convert_img_type(infile,):

  encoder_path = "C:/Users/ruonan/libwebp-1.0.0-windows-x64/bin/cwebp.exe"

  dir = '/'.join(infile.split('/')[0:-1])
  imgname = infile.split('/')[-1].split('.')[0]
  output_path = dir+"/webp/"

  if not os.path.exists(output_path):
    os.mkdir(output_path)

  new_size = get_new_size(infile)

  commond = encoder_path + " -q 80 -resize " + str(new_size[0]) + " " + str(new_size[1]) + " " +infile + " -o "+output_path + imgname + ".webp"
  logging.debug(commond)
  os.system(commond)


def get_new_size(infile):
  """
  按照手机浏览的规格（宽500）进行裁剪
  :param infile:
  :return:
  """
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

def single_dir():
  """
  单个文件夹下文件遍历
  :return:
  """
  index = 1
  input_path = "C:/Test01/oumei/*/*.jpg"
  for infile in glob(input_path):
    t = Thread(target=convert_img_type, args=(infile, index,))
    t.start()
    t.join()
    index += 1
    break

def dirs(path):
  """
  多文件夹的递归遍历
  :param path:
  :return:
  """
  parents = os.listdir(path)
  for parent in parents:
    child = os.path.join(path, parent)
    if os.path.isdir(child):
      dirs(child)
    else:
      filepath = path + '/' + parent
      logging.info(filepath)
      # convert_img_type(filepath)
      t = Thread(target=convert_img_type, args=(filepath,))
      t.start()
      t.join()



def spiltpath():
  file = 'C:/Test01/oumei/20140816195310/1.jpg'
  dir = '/'.join(file.split('/')[0:-1])
  imgname = file.split('/')[-1]


if __name__ == "__main__":
  # single_dir()
  path = "C:/Test01/oumei/"
  dirs(path)
  # spiltpath()