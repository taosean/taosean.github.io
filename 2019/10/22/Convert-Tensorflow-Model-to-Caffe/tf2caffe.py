import caffe
import numpy as np
import os
import sys
sys.path.append('caffemodel')

caffe.set_mode_gpu()
caffe.set_device(0)
net = caffe.Net('caffemodel/VeReID.prototxt', caffe.TEST)

convlayer = []
bnlayer = []
scalelayer = []

caffe_name_dict = {
'conv1_1': [],
'conv1_2': [],
'conv2_1': [],
'conv2_3': [],
'conv3_1': [],
'conv3_3': [],
'conv4_1': [],
'conv4_3': [],
'fc1': [],
}

"""{
    'conv1_1': ['conv1_1_conv', 'conv1_1_bn', 'conv1_1_scale'], 
    'conv1_2': ['conv1_2_conv', 'conv1_2_bn', 'conv1_2_scale'], 
    'conv2_1': ['conv2_1_1_conv', 'conv2_1_1_bn', 'conv2_1_1_scale', 'conv2_1_2_conv']}
    'conv2_3': ['conv2_3_bn', 'conv2_3_scale', 'conv2_3_1_conv', 'conv2_3_1_bn', 'conv2_3_1_scale', 'conv2_3_2_conv'], 
    'conv3_1': ['conv3_1_bn', 'conv3_1_scale', 'conv3_1_1_conv', 'conv3_1_1_bn', 'conv3_1_1_scale', 'conv3_1_2_conv', 'conv3_1_proj'], 
    'conv3_3': ['conv3_3_bn', 'conv3_3_scale', 'conv3_3_1_conv', 'conv3_3_1_bn', 'conv3_3_1_scale', 'conv3_3_2_conv'], 
    'conv4_1': ['conv4_1_bn', 'conv4_1_scale', 'conv4_1_1_conv', 'conv4_1_1_bn', 'conv4_1_1_scale', 'conv4_1_2_conv', 'conv4_1_proj'], 
    'conv4_3': ['conv4_3_bn', 'conv4_3_scale', 'conv4_3_1_conv', 'conv4_3_1_bn', 'conv4_3_1_scale', 'conv4_3_2_conv'], 
    'fc1': ['fc1_fc', 'fc1_bn', 'fc1_scale'], 
"""

for key in net.params.keys():
    print key
    
    for k in caffe_name_dict.keys():
        if k in key:
            caffe_name_dict[k].append(key) 
            break

print caffe_name_dict

param_path = 'params/'

for key in caffe_name_dict.keys():
    caffe_layer_names = caffe_name_dict[key]

    for layer_name in caffe_layer_names:

        if layer_name.endswith('conv') or layer_name.endswith('proj'):
            weights_path = param_path + layer_name + '_weights.npy'
            assert os.path.exists(weights_path)
            conv_weights = np.load(weights_path)
            net.params[layer_name][0].data[...] = conv_weights
            print layer_name, weights_path, conv_weights.shape, '******'

            if len(net.params[layer_name]) == 2:
                biases_path = param_path + layer_name + '_biases.npy'
                assert os.path.exists(biases_path)
                conv_biases = np.load(biases_path)
                net.params[layer_name][1].data[...] = conv_biases
                print layer_name, biases_path, conv_biases.shape, '******'


        if layer_name.endswith('bn'):
            mean_path = param_path + layer_name + '_moving_mean.npy'
            variance_path = param_path + layer_name + '_moving_variance.npy'
            assert os.path.exists(mean_path)
            assert os.path.exists(variance_path)
            bn_mean = np.load(mean_path)
            bn_variance = np.load(variance_path)
            net.params[layer_name][0].data[...] = bn_mean
            net.params[layer_name][1].data[...] = bn_variance  # + 0.001
            net.params[layer_name][2].data[...] = 1
            print layer_name, mean_path, variance_path, bn_mean.shape, bn_variance.shape


        if layer_name.endswith('scale'):
            beta_path = param_path + layer_name + '_beta.npy'
            assert os.path.exists(beta_path)
            bn_beta = np.load(beta_path)
            net.params[layer_name][0].data[...] = np.ones_like(bn_beta)
            net.params[layer_name][1].data[...] = bn_beta
            print layer_name, beta_path, bn_beta.shape

        if layer_name.endswith('fc'):
            weights_path = param_path + layer_name + '_weights.npy'
            assert os.path.exists(weights_path)
            fc_weights = np.load(weights_path)
            net.params[layer_name][0].data[...] = fc_weights
            print layer_name, weights_path, fc_weights.shape


# for i, key in enumerate(bnlayer):
#     mean_name = param_path+key+'_moving_mean.npy'
#     variance_name = param_path+key+'_moving_variance.npy'
#     beta_name = param_path+key+'_beta.npy'
#     gamma_name = param_path + key + '_gamma.npy'
#     assert os.path.exists(mean_name)
#     assert os.path.exists(variance_name)
#     assert os.path.exists(beta_name)
#     assert os.path.exists(gamma_name)
#     bn_mean=np.load(mean_name)
#     bn_variance=np.load(variance_name)
#     bn_beta=np.load(beta_name)
#     bn_gamma=np.load(gamma_name)
#     net.params[key][0].data[...]= bn_mean[...]
#     net.params[key][1].data[...] = bn_variance[...] #+ 0.001
#     net.params[key][2].data[...]=1
#     net.params[scalelayer[i]][0].data[...] = bn_gamma[...]
#     net.params[scalelayer[i]][1].data[...] = bn_beta[...]

# #print net.params['P5'][0].data.shape
# for key in convlayer:
#     print key
#     if len(net.params[key])==2:
#         if 'rpn' in key:
#             layer = '_'.join(key.split('_')[:-1])
#         else:
#             layer = key
#         print layer
#         print key
#         weights_name=param_path+layer+'_weights.npy'
#         biases_name=param_path+layer+'_biases.npy'
#         #print weights_name
#         assert os.path.exists(weights_name)
#         assert os.path.exists(biases_name)
#         conv_weights=np.load(weights_name)
#         conv_biases = np.load(biases_name)
#         net.params[key][0].data[...] = conv_weights[...]
#         net.params[key][1].data[...] = conv_biases[...]
#     if len(net.params[key])==1:
#         if 'rpn' in key:
#             layer = '_'.join(key.split('_')[:-1])
#         else:
#             layer = key
#         weights_name=param_path+layer+'_weights.npy'
#         #biases_name=param_path+key+'_biases.npy'
#         assert os.path.exists(weights_name)
#         conv_weights = np.load(weights_name)
#         net.params[key][0].data[...] = conv_weights[...]
#         #assert os.path.exists(biases_name)

net.save('caffemodel/VeReID.caffemodel')


