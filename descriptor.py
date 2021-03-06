#coding:utf-8
import cv2
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
from skimage.feature import local_binary_pattern as lbp
import math
import pandas as pd
from ops import *

     
def lbp_classifier():
    iset='ccbr'
    number = 10
    img_gallery, y_gallery = load_gallery(iset,1)
    lra_train1 = np.array([calHistogram(lbp(img,8,2),24,20) for img in img_gallery])
    lra_train2 = load_lra_train(iset, number, resize = 1)
    lra_train2 = np.array([calHistogram(lbp(img,8,2),24,20) for img in lra_train2])
    lra_train = np.vstack((lra_train1,lra_train2))
    
    # LRA Matrix
    project_m = np.hstack((np.eye(149),np.zeros((149,number*140))))
    W = np.dot(project_m,np.linalg.pinv(lra_train.T))
    #W = np.dot(np.eye(149),np.linalg.pinv(lra_train1.T))
    
    # Test Image
    probe = np.loadtxt('probe.txt',dtype='string',delimiter=' ')
    probe = pd.DataFrame(probe,columns=['path','ori_pose','ori_ill'])
    #label = np.repeat(range(149)*19,6)
    #label = np.repeat(range(149),6) 
    label = range(149)*19 #
    pose = ['041', '050', '080', '130','140', '190']
    light = ['00','01','02','03','04','05','06','08','09','10','11',
        '12','13','14','15','16','17','18','19']
    total = []
    for ipose in pose:
        count = 0
        #probe_pose = probe[probe.ori_pose==ipose].values
        probe_pose = probe[probe.ori_pose==ipose].values
        for i in range(probe_pose.shape[0]):
            if(iset == 'ccbr'):
                name = 'ccbr_probe/'+probe_pose[i,0][:-3]+'jpg'
            else:
                name = 'cpf_probe/'+probe_pose[i,0][:-3]+'bmp'
            img = cv2.imread(name,0)
            feat = calHistogram(lbp(img,8,2),24,20)
            ilabel = np.dot(W,feat).argmax()
            if(ilabel == label[i]):
                count = count+1
        print('Current Acc: %d / %d , %f' % (count,i,count/float(i)))
        total.append(count/float(i))

############################  GAN ###############33
def load_gan_gallery():
    trainData = np.zeros((149,64,64))    
    yTrain=range(149)
    gallery = np.loadtxt('gallery.txt',dtype='string',delimiter=' ')
    for i in range(149):
        iname = '/home/pris/frontal_multipie_new/'+gallery[i,0][3:]
        trainData[i,:,:] = np.float32(cv2.imread(iname,0))
    return trainData, np.array(yTrain)      
    
def lbp_classifier():
    img_gallery, y_gallery = load_gan_gallery()
    lra_train = np.array([calHistogram(lbp(img,8,2),16,16) for img in img_gallery])
    #lra_train = np.array([lbp(img,8,2).flatten() for img in img_gallery])
    
    # LRA Matrix
    #project_m = np.hstack((np.eye(149),np.zeros((149,number*140))))
    #W = np.dot(project_m,np.linalg.pinv(lra_train.T))
    W = np.dot(np.eye(149),np.linalg.pinv(lra_train.T))
    
    # Test Image
    probe = np.loadtxt('probe.txt',dtype='string',delimiter=' ')
    probe = pd.DataFrame(probe,columns=['path','ori_pose','ori_ill'])
    #label = np.repeat(range(149)*19,6)
    #label = np.repeat(range(149),6) 
    label = range(149)*19 #
    pose = ['041', '050', '080', '130','140', '190']
    light = ['00','01','02','03','04','05','06','08','09','10','11',
        '12','13','14','15','16','17','18','19']
    total = []
    for ipose in pose:
        count = 0
        #probe_pose = probe[probe.ori_ill==ipose].values
        probe_pose = probe[probe.ori_pose==ipose].values
        for i in range(probe_pose.shape[0]):
            name = '/home/pris/frontal_multipie_new2/'+probe_pose[i,0][3:]
            img = cv2.imread(name,0)
            feat = calHistogram(lbp(img,8,2),16,16)
            #feat = lbp(img,8,2).flatten()
            ilabel = np.dot(W,feat).argmax()
            if(ilabel == label[i]):
                count = count+1
        print('Current Acc: %d / %d , %f' % (count,i,count/float(i)))
        total.append(count/float(i))

def lbp_classifier():
    img_gallery, y_gallery = load_gan_gallery()
    lra_train = np.array([img.flatten() for img in img_gallery])
    #lra_train = np.array([lbp(img,8,2).flatten() for img in img_gallery])
    
    # LRA Matrix
    #project_m = np.hstack((np.eye(149),np.zeros((149,number*140))))
    #W = np.dot(project_m,np.linalg.pinv(lra_train.T))
    W = np.dot(np.eye(149),np.linalg.pinv(lra_train.T))
    
    # Test Image
    probe = np.loadtxt('probe.txt',dtype='string',delimiter=' ')
    probe = pd.DataFrame(probe,columns=['path','ori_pose','ori_ill'])
    #label = np.repeat(range(149)*19,6)
    #label = np.repeat(range(149),6) 
    label = range(149)*19 #
    pose = ['041', '050', '080', '130','140', '190']
    light = ['00','01','02','03','04','05','06','08','09','10','11',
        '12','13','14','15','16','17','18','19']
    total = []
    for ipose in pose:
        count = 0
        #probe_pose = probe[probe.ori_ill==ipose].values
        probe_pose = probe[probe.ori_pose==ipose].values
        for i in range(probe_pose.shape[0]):
            name = '/home/pris/frontal_multipie_new/'+probe_pose[i,0][3:]
            img = cv2.imread(name,0)
            feat = np.array(img.flatten(),dtype='float64')
            ilabel = []
            for j in range(149):
                ilabel.append(np.linalg.norm(lra_train[j]-feat))
            ilabel = np.argmin(ilabel)
            if(ilabel == label[i]):
                count = count+1
        print('Current Acc: %d / %d , %f' % (count,i,count/float(i)))
        total.append(count/float(i))
        
def lbp_classifier():
    iset='cpf'
    img_gallery, y_gallery = load_gallery(iset,1)
    lra_train = np.array([img.flatten() for img in img_gallery])
    
    # Test Image
    probe = np.loadtxt('probe.txt',dtype='string',delimiter=' ')
    probe = pd.DataFrame(probe,columns=['path','ori_pose','ori_ill'])
    #label = np.repeat(range(149)*19,6)
    #label = np.repeat(range(149),6) 
    label = range(149)*19 #
    pose = ['041', '050', '080', '130','140', '190']
    light = ['00','01','02','03','04','05','06','08','09','10','11',
        '12','13','14','15','16','17','18','19']
    total = []
    for ipose in pose:
        count = 0
        #probe_pose = probe[probe.ori_pose==ipose].values
        probe_pose = probe[probe.ori_pose==ipose].values
        for i in range(probe_pose.shape[0]):
            if(iset == 'ccbr'):
                name = 'ccbr_probe/'+probe_pose[i,0][:-3]+'jpg'
            else:
                name = 'cpf_probe/'+probe_pose[i,0][:-3]+'bmp'
            img = cv2.imread(name,0)
            feat = img.flatten()
            ilabel = []
            for j in range(149):
                ilabel.append(np.linalg.norm(lra_train[j]-feat))
            ilabel = np.argmin(ilabel)
            if(ilabel == label[i]):
                count = count+1
        print('Current Acc: %d / %d , %f' % (count,i,count/float(i)))
        total.append(count/float(i))        
