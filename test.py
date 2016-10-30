#!/usr/bin/env python

from model_defs import *
from utils import *
import argparse
import pandas as pd
import os
import numpy as np
import csv
from keras.models import model_from_json


def run(csv_location,batch_size,mid):
     
 
    #define the batch generator   (validation set)
    val_datagen = CSVGenerator(csv_location=csv_location,
                                 batch_size=batch_size)
    
    val_generator = val_datagen.batch_gen()

    # load json and create model
    json_file = open('models/'+mid+'.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    # load weights into new model
    model.load_weights("models/"+mid+".h5")
    print("Loaded model from disk")
 
    # evaluate loaded model on test data
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    val_loss = model.evaluate_generator(
       generator = val_generator,
       val_samples = val_datagen.get_data_size())
 
    print("%s: %.2f%%" % (model.metrics_names[1], val_loss[1]*100))
    print(val_loss)

    pass


    
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Train VGG19 on tinyimagenet using keras')
    parser.add_argument('--csvpath', type=str, default='preprocessing/valset.csv', help='batch size')
    parser.add_argument('--batchsize', type=str, default='50', help='batch size')
    parser.add_argument('--mid', type=str, default='m1', help='model id for saving')
    args = parser.parse_args()
    
    csv_location = args.csvpath
    batch_size = int(args.batchsize)
    mid = args.mid
 
    #run the model
    run(csv_location=csv_location,batch_size=batch_size,mid=mid)
    
    