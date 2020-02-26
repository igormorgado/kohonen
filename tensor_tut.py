import os
import logging

# DISABLE GPU 
#os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

#os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3" 
#logging.getLogger("tensorflow").setLevel(logging.CRITICAL) 
#logging.getLogger("tensorflow_hub").setLevel(logging.CRITICAL)    
#logging.getLogger('tensorflow').disabled = True
#logging.getLogger('tensorflow_hub').disabled = True

import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_datasets as tfds

print("Version: ", tf.__version__)
print("Eager mode: ", tf.executing_eagerly())
print("Hub Version: ", hub.__version__)
print("GPU is", "available" if tf.config.experimental.list_physical_devices("GPU") else "NOT AVAILABLE")

print(tf.reduce_sum(tf.random.normal([1000, 1000])))
