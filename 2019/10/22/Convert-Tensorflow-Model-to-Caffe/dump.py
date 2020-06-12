from tensorflow.python import pywrap_tensorflow
import numpy as np
reader = pywrap_tensorflow.NewCheckpointReader('tfmodel/model.ckpt-1985695')
var_to_shape_map = reader.get_variable_to_shape_map()

tf2caffe_name_dict = {
    'conv1_1/weights' : 'conv1_1_conv_weights',
    'conv1_1/conv1_1/bn/moving_mean' : 'conv1_1_bn_moving_mean',
    'conv1_1/conv1_1/bn/moving_variance' : 'conv1_1_bn_moving_variance',
    'conv1_1/conv1_1/bn/beta' : 'conv1_1_scale_beta',

    'conv1_2/weights' : 'conv1_2_conv_weights',
    'conv1_2/conv1_2/bn/moving_mean' : 'conv1_2_bn_moving_mean',
    'conv1_2/conv1_2/bn/moving_variance' : 'conv1_2_bn_moving_variance',
    'conv1_2/conv1_2/bn/beta' : 'conv1_2_scale_beta',

    'conv2_1/1/weights' : 'conv2_1_1_conv_weights',
    'conv2_1/1/conv2_1/1/bn/moving_mean' : 'conv2_1_1_bn_moving_mean',
    'conv2_1/1/conv2_1/1/bn/moving_variance' : 'conv2_1_1_bn_moving_variance',
    'conv2_1/1/conv2_1/1/bn/beta' : 'conv2_1_1_scale_beta',
    'conv2_1/2/weights' : 'conv2_1_2_conv_weights',
    'conv2_1/2/biases' : 'conv2_1_2_conv_biases',

    'conv2_3/bn/moving_mean' : 'conv2_3_bn_moving_mean',
    'conv2_3/bn/moving_variance' : 'conv2_3_bn_moving_variance',
    'conv2_3/bn/beta' : 'conv2_3_scale_beta',
    'conv2_3/1/weights' : 'conv2_3_1_conv_weights',
    'conv2_3/1/conv2_3/1/bn/moving_mean' : 'conv2_3_1_bn_moving_mean',
    'conv2_3/1/conv2_3/1/bn/moving_variance' : 'conv2_3_1_bn_moving_variance',
    'conv2_3/1/conv2_3/1/bn/beta' : 'conv2_3_1_scale_beta',
    'conv2_3/2/weights' : 'conv2_3_2_conv_weights',
    'conv2_3/2/biases' : 'conv2_3_2_conv_biases',

    'conv3_1/bn/moving_mean' : 'conv3_1_bn_moving_mean',
    'conv3_1/bn/moving_variance' : 'conv3_1_bn_moving_variance',
    'conv3_1/bn/beta' : 'conv3_1_scale_beta',
    'conv3_1/1/weights' : 'conv3_1_1_conv_weights',
    'conv3_1/1/conv3_1/1/bn/moving_mean' : 'conv3_1_1_bn_moving_mean',
    'conv3_1/1/conv3_1/1/bn/moving_variance' : 'conv3_1_1_bn_moving_variance',
    'conv3_1/1/conv3_1/1/bn/beta' : 'conv3_1_1_scale_beta',
    'conv3_1/2/weights' : 'conv3_1_2_conv_weights',
    'conv3_1/2/biases' : 'conv3_1_2_conv_biases',
    'conv3_1/projection/weights' : 'conv3_1_proj_weights',

    'conv3_3/bn/moving_mean' : 'conv3_3_bn_moving_mean',
    'conv3_3/bn/moving_variance' : 'conv3_3_bn_moving_variance',
    'conv3_3/bn/beta' : 'conv3_3_scale_beta',
    'conv3_3/1/weights' : 'conv3_3_1_conv_weights',
    'conv3_3/1/conv3_3/1/bn/moving_mean' : 'conv3_3_1_bn_moving_mean',
    'conv3_3/1/conv3_3/1/bn/moving_variance' : 'conv3_3_1_bn_moving_variance',
    'conv3_3/1/conv3_3/1/bn/beta' : 'conv3_3_1_scale_beta',
    'conv3_3/2/weights' : 'conv3_3_2_conv_weights',
    'conv3_3/2/biases' : 'conv3_3_2_conv_biases',

    'conv4_1/bn/moving_mean' : 'conv4_1_bn_moving_mean',
    'conv4_1/bn/moving_variance' : 'conv4_1_bn_moving_variance',
    'conv4_1/bn/beta' : 'conv4_1_scale_beta',
    'conv4_1/1/weights' : 'conv4_1_1_conv_weights',
    'conv4_1/1/conv4_1/1/bn/moving_mean' : 'conv4_1_1_bn_moving_mean',
    'conv4_1/1/conv4_1/1/bn/moving_variance' : 'conv4_1_1_bn_moving_variance',
    'conv4_1/1/conv4_1/1/bn/beta' : 'conv4_1_1_scale_beta',
    'conv4_1/2/weights' : 'conv4_1_2_conv_weights',
    'conv4_1/2/biases' : 'conv4_1_2_conv_biases',
    'conv4_1/projection/weights' : 'conv4_1_proj_weights',

    'conv4_3/bn/moving_mean' : 'conv4_3_bn_moving_mean',
    'conv4_3/bn/moving_variance' : 'conv4_3_bn_moving_variance',
    'conv4_3/bn/beta' : 'conv4_3_scale_beta',
    'conv4_3/1/weights' : 'conv4_3_1_conv_weights',
    'conv4_3/1/conv4_3/1/bn/moving_mean' : 'conv4_3_1_bn_moving_mean',
    'conv4_3/1/conv4_3/1/bn/moving_variance' : 'conv4_3_1_bn_moving_variance',
    'conv4_3/1/conv4_3/1/bn/beta' : 'conv4_3_1_scale_beta',
    'conv4_3/2/weights' : 'conv4_3_2_conv_weights',
    'conv4_3/2/biases' : 'conv4_3_2_conv_biases',

    'fc1/weights' : 'fc1_fc_weights',
    'fc1/fc1/bn/moving_mean' : 'fc1_bn_moving_mean',
    'fc1/fc1/bn/moving_variance' : 'fc1_bn_moving_variance',
    'fc1/fc1/bn/beta' : 'fc1_scale_beta'
}

for key in var_to_shape_map:
    print key
    if not ('Adam' in key or 'ball' in key or 'power' in key or 'global' in key):
        w = reader.get_tensor(key)

        print key, ' ', tf2caffe_name_dict[key], w.shape

        if (len(w.shape) == 4):
            w = w.transpose(3, 2, 0, 1)  # HWIO (tf filter order) -> OIHW (caffe filter order)

        if (len(w.shape) == 2):
            w = w.transpose(1, 0)  # this is only applied to fc1/weights in this project
            

        dumpname = 'params/' + tf2caffe_name_dict[key] + '.npy'
        np.save(dumpname, w)

print len(tf2caffe_name_dict.keys())