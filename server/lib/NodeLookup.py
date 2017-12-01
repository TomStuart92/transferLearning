import os.path
import tensorflow as tf

class NodeLookup(object):
  def __init__(self):
    label_lookup_path = os.path.join('lib', 'classification_labels.pbtxt')
    self.node_lookup = self.load(label_lookup_path)


  def load(self, label_lookup_path):
    if not tf.gfile.Exists(label_lookup_path):
      tf.logging.fatal('File does not exist %s', label_lookup_path)

    # Loads mapping from string UID to integer node ID.
    node_id_to_name = {}
    proto_as_ascii = tf.gfile.GFile(label_lookup_path).readlines()

    # extracts target_class
    for line in proto_as_ascii:
      if line.startswith('  target_class:'):
        target_class = int(line.split(': ')[1])
      if line.startswith('  target_class_string:'):
        target_class_string = line.split(': ')[1]
        node_id_to_name[target_class] = target_class_string[1:-2]
    return node_id_to_name

  def id_to_string(self, node_id):
    if node_id not in self.node_lookup:
      return ''
    return self.node_lookup[node_id]
