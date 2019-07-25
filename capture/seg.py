import os
from io import BytesIO
from django.core.files.base import ContentFile

import numpy as np
from PIL import Image, ImageFilter

import tensorflow as tf
import sys
import datetime


class DeepLabModel(object):
  """Class to load deeplab model and run inference."""

  INPUT_TENSOR_NAME = 'ImageTensor:0'
  OUTPUT_TENSOR_NAME = 'SemanticPredictions:0'
  INPUT_SIZE = 513
  FROZEN_GRAPH_NAME = 'frozen_inference_graph'

  def __init__(self, tarball_path):
    """Creates and loads pretrained deeplab model."""
    self.graph = tf.Graph()

    graph_def = None
    graph_def = tf.GraphDef.FromString(open(tarball_path + "/frozen_inference_graph.pb", "rb").read()) 

    if graph_def is None:
      raise RuntimeError('Cannot find inference graph in tar archive.')

    with self.graph.as_default():
      tf.import_graph_def(graph_def, name='')

    self.sess = tf.Session(graph=self.graph)

  def run(self, image):
    """Runs inference on a single image.

    Args:
      image: A PIL.Image object, raw input image.

    Returns:
      resized_image: RGB image resized from original input image.
      seg_map: Segmentation map of `resized_image`.
    """
    start = datetime.datetime.now()

    width, height = image.size
    resize_ratio = 1.0 * self.INPUT_SIZE / max(width, height)
    target_size = (int(resize_ratio * width), int(resize_ratio * height))
    resized_image = image.convert('RGB').resize(target_size, Image.ANTIALIAS)
    batch_seg_map = self.sess.run(
        self.OUTPUT_TENSOR_NAME,
        feed_dict={self.INPUT_TENSOR_NAME: [np.asarray(resized_image)]})
    seg_map = batch_seg_map[0]

    end = datetime.datetime.now()

    diff = end - start
    print("Time taken to evaluate segmentation is : " + str(diff))

    return resized_image, seg_map

def drawSegment(baseImg, matImg):
  width, height = baseImg.size
  dummyImg = np.zeros([height, width, 4], dtype=np.uint8)
  for x in range(width):
            for y in range(height):
                color = matImg[y,x]
                (r,g,b) = baseImg.getpixel((x,y))
                if color == 0:
                    dummyImg[y,x,3] = 0
                else :
                    dummyImg[y,x] = [r,g,b,255]
  img = Image.fromarray(dummyImg)
  #img.save(outputFilePath)
  return img
  
### Merge background image with captured image
def mergeBackground(segmentImg, captureimg_path, bgimg_path):
  output_size = (1600, 1200)
  radius = 5
  img = segmentImg.resize(output_size, Image.BICUBIC).filter(ImageFilter.GaussianBlur(radius/2))
  capture_img = Image.open(captureimg_path)
  capture_img = capture_img.convert("RGBA")
  bg_img = Image.open(bgimg_path)
  bg_img = bg_img.convert("RGBA").resize(output_size)
  merge_img = Image.new("RGBA", output_size)
  merge_img.paste(bg_img, (0,0,1600,1200))
  merge_img.paste(capture_img, (0,0,1600,1200), img)
  merge_img = merge_img.convert("RGB")
  merge_img.save(captureimg_path, format='JPEG')
  return merge_img

'''
inputFilePath = sys.argv[1]
outputFilePath = sys.argv

if inputFilePath is None or outputFilePath is None:
  print("Bad parameters. Please specify input file path and output file path")
  exit()

modelType = "mobile_net_model"
if len(sys.argv) > 3 and sys.argv[3] == "1":'''

modelType = "xception_model"

MODEL = DeepLabModel(modelType)
print('model loaded successfully : ' + modelType)

def run_visualization(captureimg_path, bgimg_path):
  """Inferences DeepLab model and visualizes result."""
  try:
  	#print("Trying to open : " + sys.argv[1])
  	print("Trying to open : " + captureimg_path)
  	# f = open(sys.argv[1])
  	jpeg_str = open(captureimg_path, "rb").read()
  	orignal_im = Image.open(BytesIO(jpeg_str))
  except IOError:
    print('Cannot retrieve image. Please check file: ' + captureimg_path)
    return

  print('running deeplab on image %s...' % captureimg_path)
  resized_im, seg_map = MODEL.run(orignal_im)

  # vis_segmentation(resized_im, seg_map)
  segmentImg = drawSegment(resized_im, seg_map)
  
  mergeImg = mergeBackground(segmentImg, captureimg_path, bgimg_path)
  
  THUMBNAIL_SIZE = (120, 80)
  image = Image.open(captureimg_path)
  image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
  image.save(captureimg_path.split('/')[0] + '/thumbnails/' + captureimg_path.split('/')[-1].split('.')[0] + '_thumbnail.' + captureimg_path.split('/')[-1].split('.')[-1], format='JPEG')
  

#run_visualization(inputFilePath)

