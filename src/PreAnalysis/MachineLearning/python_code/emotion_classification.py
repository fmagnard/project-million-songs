# -*- coding: utf-8 -*-

import time
import pandas as pd
import numpy as np
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.ensemble import RandomForestClassifier 
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn import preprocessing
from sklearn.utils import shuffle
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.multiclass import OneVsOneClassifier



if __name__=='__main__':
    start_time=time.time()
    audio_liwc_features_emotions_df=pd.read_csv('../csv_database/audio_liwc_features_emotions_thematic_score.csv',delimiter=',')
    
    audio_liwc_features_emotions_df=audio_liwc_features_emotions_df.drop('track_id',1)
    audio_liwc_features_emotions_df=audio_liwc_features_emotions_df.drop('year',1)
    header=['tempo','mode','loudness','key','duration','neg_affect_score','pos_affect_score','sadness_score','swear_score','anger_score','anxiety_score','emotion']
    audio_liwc_features_emotions_df=audio_liwc_features_emotions_df[header]
    audio_liwc_features_emotions_nparray=audio_liwc_features_emotions_df.values
    
    nb_songs=shape(audio_liwc_features_emotions_nparray)[0]
    nb_features=shape(audio_liwc_features_emotions_nparray)[1]
    X=audio_liwc_features_emotions_nparray[:,0:nb_features-1]
    
    #Standardization of data
    normalizer=preprocessing.StandardScaler()
    normalizer.fit_transform(X)
    y=audio_liwc_features_emotions_nparray[:,nb_features-1]
    X, y = shuffle(X, y, random_state=0)
    le = preprocessing.LabelEncoder()
    le.fit(y)
    y=le.transform(y) 
    nb_happy= len(y[le.inverse_transform(y)=='Happy'])
    nb_angry= len(y[le.inverse_transform(y)=='Angry'])
    nb_sad= len(y[le.inverse_transform(y)=='Sad'])
    nb_relax= len(y[le.inverse_transform(y)=='Relax'])
    X_happy=X[le.inverse_transform(y)=='Happy']
    y_happy=y[le.inverse_transform(y)=='Happy']
    X_angry=X[le.inverse_transform(y)=='Angry']
    y_angry=y[le.inverse_transform(y)=='Angry']
    X_sad=X[le.inverse_transform(y)=='Sad']
    y_sad=y[le.inverse_transform(y)=='Sad']
    X_relax=X[le.inverse_transform(y)=='Relax']
    y_relax=y[le.inverse_transform(y)=='Relax']

    size_least_represented_feature= min([nb_happy,nb_angry,nb_sad,nb_relax]) 
    
    #Cross Validation
    
    
    size_train_dataset=9*size_least_represented_feature/10
    X_happy_train=X_happy[0:size_train_dataset,:]
    y_happy_train=y_happy[0:size_train_dataset]
    X_angry_train=X_angry[0:size_train_dataset,:]
    y_angry_train=y_angry[0:size_train_dataset]
    X_sad_train=X_sad[0:size_train_dataset,:]
    y_sad_train=y_sad[0:size_train_dataset]
    X_relax_train=X_relax[0:size_train_dataset,:]
    y_relax_train=y_relax[0:size_train_dataset]
    
    X_train=np.concatenate((X_happy_train,X_angry_train,X_sad_train,X_relax_train))
    y_train=np.concatenate((y_happy_train,y_angry_train,y_sad_train,y_relax_train))
    
    X_happy_test=X_happy[size_train_dataset:,:]
    y_happy_test=y_happy[size_train_dataset:]
    X_angry_test=X_angry[size_train_dataset:,:]
    y_angry_test=y_angry[size_train_dataset:]
    X_sad_test=X_sad[size_train_dataset:,:]
    y_sad_test=y_sad[size_train_dataset:]
    X_relax_test=X_relax[size_train_dataset:,:]
    y_relax_test=y_relax[size_train_dataset:]
    
    X_test=np.concatenate((X_happy_test,X_angry_test,X_sad_test,X_relax_test))
    y_test=np.concatenate((y_happy_test,y_angry_test,y_sad_test,y_relax_test))
    
    

    
        
    proportion_happy_train=1.0*len(y_train[le.inverse_transform(y_train)=='Happy'])/len(y_train)
    proportion_angry_train=1.0*len(y_train[le.inverse_transform(y_train)=='Angry'])/len(y_train)
    proportion_sad_train=1.0*len(y_train[le.inverse_transform(y_train)=='Sad'])/len(y_train)
    proportion_relax_train=1.0*len(y_train[le.inverse_transform(y_train)=='Relax'])/len(y_train)
    
    proportion_happy_test=1.0*len(y_test[le.inverse_transform(y_test)=='Happy'])/len(y_test)
    proportion_angry_test=1.0*len(y_test[le.inverse_transform(y_test)=='Angry'])/len(y_test)
    proportion_sad_test=1.0*len(y_test[le.inverse_transform(y_test)=='Sad'])/len(y_test)
    proportion_relax_test=1.0*len(y_test[le.inverse_transform(y_test)=='Relax'])/len(y_test)
    
    
    
    print 'proportions of happy, angry, sad and relax labels in train dataset:'
    print proportion_happy_train,proportion_angry_train,proportion_sad_train,proportion_relax_train
    print ''
    print 'proportions of happy, angry, sad and relax labels in test dataset:'
    print proportion_happy_test,proportion_angry_test,proportion_sad_test,proportion_relax_test
    
    #Random Forest
    nb_trees=100
    forest_classification = RandomForestClassifier(n_estimators = nb_trees)
    
    forest_classification.fit(X_train,y_train)
    
    y_predicted_rdmf=forest_classification.predict(X_test)
    print ''
    print 'Random Forest classification accuracy score = %f ' % accuracy_score(y_test, y_predicted_rdmf)
    print ''
    
    target_names = [le.inverse_transform([0])[0], le.inverse_transform([1])[0], le.inverse_transform([2])[0],le.inverse_transform([3])[0]]
    
    print 'Random Forest:'
    print(classification_report(y_test, y_predicted_rdmf, target_names=target_names))
    print ''
    print 'Random Forest confusion matrix:'
    print confusion_matrix(y_test,y_predicted_rdmf)
    
    #One versus rest random forest
    
    OvR_forest=OneVsRestClassifier(forest_classification)
    OvR_forest.fit(X_train, y_train)
    y_predicted_OvR_rdmf=OvR_forest.predict(X_test)
    print ''
    print 'OvR Random Forest classification accuracy score = %f ' % accuracy_score(y_test, y_predicted_OvR_rdmf)
    print ''
    
    target_names = [le.inverse_transform([0])[0], le.inverse_transform([1])[0], le.inverse_transform([2])[0],le.inverse_transform([3])[0]]
    
    print 'OvR Random Forest:'
    print(classification_report(y_test, y_predicted_OvR_rdmf, target_names=target_names))
    print ''
    print 'OvR Random Forest confusion matrix:'
    print confusion_matrix(y_test,y_predicted_OvR_rdmf)
    
    #One versus one random forest
    
    OvO_forest=OneVsOneClassifier(forest_classification)
    OvO_forest.fit(X_train, y_train)
    y_predicted_OvO_rdmf=OvO_forest.predict(X_test)
    print ''
    print 'OvO Random Forest classification accuracy score = %f ' % accuracy_score(y_test, y_predicted_OvO_rdmf)
    print ''
    
    target_names = [le.inverse_transform([0])[0], le.inverse_transform([1])[0], le.inverse_transform([2])[0],le.inverse_transform([3])[0]]
    
    print 'OvO Random Forest:'
    print(classification_report(y_test, y_predicted_OvO_rdmf, target_names=target_names))
    print ''
    print 'OvO Random Forest confusion matrix:'
    print confusion_matrix(y_test,y_predicted_OvO_rdmf)
    
    #Gaussian Naive Bayes
    gnb=GaussianNB()
    gnb.fit(X_train, y_train)
    y_predicted_gnb = gnb.predict(X_test)
    print ''
    print 'Gaussian Naive Bayes classification accuracy score = %f ' % accuracy_score(y_test, y_predicted_gnb)
    print ''
    
    target_names = [le.inverse_transform([0])[0], le.inverse_transform([1])[0], le.inverse_transform([2])[0],le.inverse_transform([3])[0]]
    
    print 'Gaussian Naive Bayes:'
    print(classification_report(y_test, y_predicted_gnb, target_names=target_names))
    print ''
    print 'Gaussian Naive Bayes confusion matrix:'
    print confusion_matrix(y_test,y_predicted_gnb)
    
    #Support Vector Machine
    
    csvm = SVC()
    csvm.fit(X_train, y_train) 
    y_predicted_csvm = csvm.predict(X_test)
    
    print ''
    print 'SVM classification accuracy score = %f ' % accuracy_score(y_test, y_predicted_csvm)
    print ''
    
    target_names = [le.inverse_transform([0])[0], le.inverse_transform([1])[0], le.inverse_transform([2])[0],le.inverse_transform([3])[0]]
    
    print 'SVM:'
    print(classification_report(y_test, y_predicted_csvm, target_names=target_names))
    print ''
    print 'SVM confusion matrix:'
    print confusion_matrix(y_test,y_predicted_csvm)
    
    
    elapsed_time=time.time()-start_time
    print 'elapsed time : %f sec' % elapsed_time
