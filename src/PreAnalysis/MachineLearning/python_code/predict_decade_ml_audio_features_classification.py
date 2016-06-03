# -*- coding: utf-8 -*-

import pandas as pd
import time
import numpy as np
from sklearn.ensemble import RandomForestClassifier 
from sklearn import preprocessing
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

if __name__=='__main__':
    
    start_time=time.time()
    
    metadata_tsv_file='../../ConvertToCSV/Outputs/features.tsv'
    metadata_df=pd.read_csv(metadata_tsv_file, delimiter='\t')
    
    audio_features_year_df=metadata_df[['loudness','tempo','duration','mode','time_signature','year']][metadata_df['year']!=0]
    
    audio_features_year_df=audio_features_year_df[['loudness','tempo','duration','year']]
    audio_features_year_df['decade']=audio_features_year_df['year']-(audio_features_year_df['year'] % 10)
    
    audio_features_decade_df=audio_features_year_df.drop('year', 1)
    
    
    
    audio_features_decade_nparray=audio_features_decade_df.values
    
    
    nb_features=shape(audio_features_decade_nparray)[1]-1

    nb_songs=shape(audio_features_decade_nparray)[0]
    
    X=audio_features_decade_nparray[:,0:nb_features]
    #Standardization of data
    normalizer=preprocessing.StandardScaler()
    normalizer.fit_transform(X)
    y=audio_features_decade_nparray[:,nb_features]
    
    unique_decades_in_dataset=np.unique(y)
    X_by_decade={}
    y_by_decade={}
    nb_elements_by_decade={}
    min_nb_elements_by_decade=float('inf')
    min_nb_elements_by_decade_from_1960=float('inf')
    
    for decade in unique_decades_in_dataset:
        X_by_decade[int(decade)]=X[y==decade]
        y_by_decade[int(decade)]=y[y==decade]
        nb_elements_by_decade[int(decade)]=len(y[y==decade])
        if len(y[y==decade])<min_nb_elements_by_decade:
            min_nb_elements_by_decade=len(y[y==decade])
        if decade>=1960:
            if len(y[y==decade])<min_nb_elements_by_decade_from_1960:
                min_nb_elements_by_decade_from_1960=len(y[y==decade])
            
    
    size_train_dataset=9*min_nb_elements_by_decade/10
    size_train_dataset_from_1960=9*min_nb_elements_by_decade_from_1960/10
    
    X_train_by_decade={}
    y_train_by_decade={}    
    X_train_by_decade_from_1960={}
    y_train_by_decade_from_1960={} 
    
    X_test_by_decade={}
    y_test_by_decade={}    
    X_test_by_decade_from_1960={}
    y_test_by_decade_from_1960={} 
    for decade in unique_decades_in_dataset:
        X_train_by_decade[int(decade)]=X_by_decade[int(decade)][0:size_train_dataset,:]
        y_train_by_decade[int(decade)]=y_by_decade[int(decade)][0:size_train_dataset]
        X_test_by_decade[int(decade)]=X_by_decade[int(decade)][size_train_dataset:,:]
        y_test_by_decade[int(decade)]=y_by_decade[int(decade)][size_train_dataset:]
       
        if decade>=1960:
            X_train_by_decade_from_1960[int(decade)]=X_by_decade[int(decade)][0:size_train_dataset_from_1960,:]
            y_train_by_decade_from_1960[int(decade)]=y_by_decade[int(decade)][0:size_train_dataset_from_1960]
            X_test_by_decade_from_1960[int(decade)]=X_by_decade[int(decade)][size_train_dataset:,:]
            y_test_by_decade_from_1960[int(decade)]=y_by_decade[int(decade)][size_train_dataset:]
    
    X_train_all=np.concatenate([X_train_by_decade[el] for el in X_train_by_decade])
    y_train_all=np.concatenate([y_train_by_decade[el] for el in y_train_by_decade])
    X_test_all=np.concatenate([X_test_by_decade[el] for el in X_test_by_decade])
    y_test_all=np.concatenate([y_test_by_decade[el] for el in y_test_by_decade])
    
    X_train_from_1960=np.concatenate([X_train_by_decade_from_1960[el] for el in X_train_by_decade_from_1960])
    y_train_from_1960=np.concatenate([y_train_by_decade_from_1960[el] for el in y_train_by_decade_from_1960])
    X_test_from_1960=np.concatenate([X_test_by_decade_from_1960[el] for el in X_test_by_decade_from_1960])
    y_test_from_1960=np.concatenate([y_test_by_decade_from_1960[el] for el in y_test_by_decade_from_1960])
    
    proportions_train_all={}
    proportions_test_all={}
    
    proportions_train_from_1960={}
    proportions_test_from_1960={}
    
    for decade in unique_decades_in_dataset:
        proportions_train_all[int(decade)]=1.0*len(y_train_all[y_train_all==decade])/len(y_train_all)
        proportions_test_all[int(decade)]=1.0*len(y_test_all[y_test_all==decade])/len(y_test_all)
        if decade>=1960:
            proportions_train_from_1960[int(decade)]=1.0*len(y_train_from_1960[y_train_from_1960==decade])/len(y_train_from_1960)
            proportions_test_from_1960[int(decade)]=1.0*len(y_test_from_1960[y_test_from_1960==decade])/len(y_test_from_1960)
            
    print 'proportions of labels for all decades in train dataset:'
    print proportions_train_all
    print 'proportions of labels for all decades in test dataset:'
    print proportions_test_all
    print 'proportions of labels for decades from 1960 in train dataset:'
    print proportions_train_from_1960
    print 'proportions of labels for decades from 1960 in test dataset:'
    print proportions_test_from_1960
        
    
    
    
    
    nb_trees=130
    forest_all_decades = RandomForestClassifier(n_estimators = nb_trees)
    
    forest_all_decades.fit(X_train_all,y_train_all)

    

    y_predicted_all_decades=forest_all_decades.predict(X_test_all)
    
    print ''
    print 'Using data for all decades: Random Forest classification accuracy score = %f ' % accuracy_score(y_test_all, y_predicted_all_decades)
    print ''
    
    
    print 'Using data for all decades: Random Forest:'
    print(classification_report(y_test_all, y_predicted_all_decades))
    print ''
    print 'Using data for all decades: Random Forest confusion matrix:'
    print confusion_matrix(y_test_all,y_predicted_all_decades)
    
    
    forest_from1960 = RandomForestClassifier(n_estimators = nb_trees)
    
    forest_from1960.fit(X_train_from_1960,y_train_from_1960)

    

    y_predicted_from1960=forest_from1960.predict(X_test_from_1960)
    
    print ''
    print 'Using data from 1960: Random Forest classification accuracy score = %f ' % accuracy_score(y_test_from_1960, y_predicted_from1960)
    print ''
    
    
    print 'Using data from 1960: Random Forest:'
    print(classification_report(y_test_from_1960, y_predicted_from1960))
    print ''
    print 'Using data from 1960: Random Forest confusion matrix:'
    print confusion_matrix(y_test_from_1960,y_predicted_from1960)
    
    
    
    elapsed_time=time.time()-start_time
    print 'elapsed time : %f sec' % elapsed_time
