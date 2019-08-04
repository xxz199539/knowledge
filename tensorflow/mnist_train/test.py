import os

from tensorflow.python import pywrap_tensorflow

MODEL_SAVE_PATH = './model/regression/'
MODEL_NAME = 'regression.ckpt'
checkpoint_path = os.path.join(MODEL_SAVE_PATH, MODEL_NAME)
reader = pywrap_tensorflow.NewCheckpointReader(checkpoint_path)
var_to_shape_map = reader.get_variable_to_shape_map()
for key in var_to_shape_map:
    print("tensor_name: ", key, end=' ')
    print(reader.get_tensor(key))
