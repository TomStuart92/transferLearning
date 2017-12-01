from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os.path
import re
import io
import sys
import tarfile
import json

import numpy as np
import tensorflow as tf
from lib import NodeLookup

# set tensorflow log level to error
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# It's hard to get data into and out of tensorflow library.
# We use these arrays to track inputs and outputs
inputs = []
outputs = []


# tensorflow library runs sys.exit on completion. We monkey patch here to capture exit value
def new_sys_exit(exitValue):
  outputs.append(exitValue)

sys.exit = new_sys_exit


def create_graph():
  # Creates graph from saved graph_def.pb.
  filePath = os.path.join('lib', 'classify_image_graph_def.pb')
  with tf.gfile.FastGFile(filePath, 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')


def run_inference_on_image(_):
  # extract input image
  image = inputs[0]
  image_data = image.read()
  create_graph()

  with tf.Session() as sess:

    # set up softmax_tensor
    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

    # run predictions
    predictionSet = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})
    predictions = np.squeeze(predictionSet)

    # Creates node ID --> English string lookup.
    node_lookup = NodeLookup.NodeLookup()

    # return top 5 predictions
    top_k = predictions.argsort()[-5:][::-1]

    # loop through predictions and return human_string
    data = {}
    for node_id in top_k:
      human_string = node_lookup.id_to_string(node_id)
      score = predictions[node_id]
      data[human_string] = str(score*100)
  return data

def run(inputImage):
    # make sure inputs and outputs are clear
    del inputs[:]
    del outputs[:]

    # add image to inputs
    inputs.append(inputImage)

    # run tensorflow on image
    tf.app.run(main=run_inference_on_image, argv=[sys.argv[0]])

    # return output value
    return outputs[0]
