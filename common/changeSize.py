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


def decode_img_from_webp_to_jpg(infile,):
  """
  将webp解压为png,解码后图片大了十倍
  :param infile:
  :return:
  """
  encoder_path = "C:/Users/ruonan/libwebp-1.0.0-windows-x64/bin/dwebp.exe"

  dir = '/'.join(infile.split('/')[0:-1]).replace("Test01", "Test02");
  imgname = infile.split('/')[-1].split('.')[0]
  # output_path = (dir+"/").replace("/","\\")
  output_path = (dir + "/")
  # print output_path

  if not os.path.exists(output_path):
    os.mkdir(output_path)

  # new_size = get_new_size(infile)

  commond = encoder_path + " "+ infile + " " +  " -o " + output_path + imgname + ".png"
  logging.debug(commond)
  os.system(commond)

def convert_img_size(infile,):
  """
  将图片压缩到单独的webp下
  :param infile:
  :return:
  """

  dir = '/'.join(infile.split('/')[0:-1]).replace("Test01", "Test03");
  imgname = infile.split('/')[-1].split('.')[0]
  output_path = (dir + "/")
  if not os.path.exists(output_path):
    os.mkdir(output_path)

  im = Image.open(infile)
  new_size = get_new_size(infile)

  im.thumbnail((new_size[0], new_size[1]))
  # im.resize((new_size[0], new_size[1]))

  im.save(output_path+imgname+'.jpg', 'JPEG')


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
      convert_img_size(filepath)
      # decode_img_from_webp_to_jpg(filepath)



if __name__ == "__main__":
  path = "C:/Test01/rihan/"
  dirs(path)