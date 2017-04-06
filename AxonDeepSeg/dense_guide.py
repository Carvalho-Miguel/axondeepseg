# -*- coding: utf-8 -*-

# guide

import json
import os
import shutil

# Description du fichier config :
# network_learning_rate : float : No idea, but certainly linked to the back propagation ? Default : 0.0005.
# network_n_classes : int : number of labels in the output. Default : 2.
# dropout : float : between 0 and 1 : percentage of neurons we want to keep. Default : 0.75.
# network_depth : int : number of layers WARNING : factualy, there will be 2*network_depth layers. Default : 6.
# network_convolution_per_layer : list of int, length = network_depth : number of convolution per layer. Default : [1 for i in range(network_depth)].
# network_size_of_convolutions_per_layer : list of lists of int [number of layers[number_of_convolutions_per_layer]] : Describe the size of each convolution filter.
# Default : [[3 for k in range(network_convolution_per_layer[i])] for i in range(network_depth)].

# network_features_per_convolution : list of lists of int [number of layers[number_of_convolutions_per_layer[2]] : Numer of different filters that are going to be used.
# Default : [[[64,64] for k in range(network_convolution_per_layer[i])] for i in range(network_depth)]. WARNING ! network_features_per_convolution[k][1] = network_features_per_convolution[k+1][0].

repname = './config_network'
filename = '/dense_config_network.json'


network_learning_rate = 0.0005
network_n_classes = 2
dropout = 0.75
network_depth = 3
network_convolution_per_layer = [2 for i in range(network_depth)]
network_size_of_convolutions_per_layer = [[5,3],[9,3],[5,3]]#[[3 for k in range(network_convolution_per_layer[i])] for i in range(network_depth)]
network_features_per_convolution = [[[1,64],[64,64]],[[64,128],[128,128]],[[128,256],[256,256]]]#,[[256,512],[512,512]],[[512,1024],[1024,1024]],[[1024,2048],[2048,2048]]]

"""
config = {
    'network_learning_rate': 0.0005,
    'network_n_classes': 2,
    'dropout': 0.75,
    'network_depth': 3,
    'network_convolution_per_layer': [1 for i in range(network_depth)],
    'network_size_of_convolutions_per_layer': [[3 for k in range(network_convolution_per_layer[i])] for i in
                                               range(network_depth)],
    'network_features_per_convolution': [[[64,64] for k in range(network_convolution_per_layer[i])] for i in range(network_depth)]
}
"""
config = {
    'network_learning_rate': network_learning_rate,
    'network_n_classes': network_n_classes,
    'network_dropout': dropout,
    'network_depth': network_depth,
    'network_convolution_per_layer': network_convolution_per_layer,
    'network_size_of_convolutions_per_layer': network_size_of_convolutions_per_layer,
    'network_features_per_convolution': network_features_per_convolution
}

# Edit and read the config

with open(repname+filename, 'w+') as f:
    json.dump(config, f, indent=2)

with open(repname+filename, 'r') as fd:
	config_network = json.loads(fd.read())

learning_rate = config_network.get("network_learning_rate", 0.0005)
n_classes = config_network.get("network_n_classes", 2)
dropout = config_network.get("network_dropout", 0.75)
depth = config_network.get("network_depth", 6)
number_of_convolutions_per_layer = config_network.get("network_convolution_per_layer", [1 for i in range(depth)])
size_of_convolutions_per_layer =  config_network.get("network_size_of_convolutions_per_layer",[[3 for k in range(number_of_convolutions_per_layer[i])] for i in range(depth)])
features_per_convolution = config_network.get("network_features_per_convolution",[[[64,64] for k in range(number_of_convolutions_per_layer[i])] for i in range(depth)])

# print(learning_rate,n_classes,dropout,depth,number_of_convolutions_per_layer,size_of_convolutions_per_layer,features_per_convolution)

# training
path_training = './../trainingset/CARS/trainingset'
path_model = './../models/Unet_dense'

# Create the model's folder if it doesn't exist.
if os.path.exists(path_model):
    shutil.rmtree(path_model)
if not os.path.exists(path_model):
    os.makedirs(path_model)

with open(path_model+filename, 'w') as f:
    json.dump(config, f, indent=2)


from dense_network import train_model
train_model(path_training, path_model, config_network)

#from AxonDeepSeg.learn_model import train_model
#train_model(path_training, path_model, learning_rate=0.0005)