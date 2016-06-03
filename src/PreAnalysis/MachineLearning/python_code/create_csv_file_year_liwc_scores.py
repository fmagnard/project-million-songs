# -*- coding: utf-8 -*-

import time
import pandas as pd
import sqlite3
from nltk.corpus import stopwords
import numpy as np
import re


def liwc_score(text,nb_words,liwc_path):

    with open(liwc_path) as lexicon:
        return np.sum([len(re.findall(word[:-1], text)) for word in lexicon])*1.0/nb_words
             

    

if __name__=='__main__':
    
    start_time=time.time()
    
    
    
    ''' 1. Get LIWC lexicons '''
    liwc_file_pos_affect='../LIWC_lexicons/positive_affect'
    #words_in_liwc_file_pos_affect=set(pd.read_csv(liwc_file_pos_affect, header=None, delimiter=r"\s+")[0].tolist())#set for more efficiency
    
    liwc_file_neg_affect='../LIWC_lexicons/negative_affect'
    #words_in_liwc_file_neg_affect=set(pd.read_csv(liwc_file_neg_affect, header=None, delimiter=r"\s+")[0].tolist())
    
    liwc_file_anger='../LIWC_lexicons/anger'
    #words_in_liwc_file_anger=set(pd.read_csv(liwc_file_anger, header=None, delimiter=r"\s+")[0].tolist())
   
    liwc_file_anxiety='../LIWC_lexicons/anxiety'
    #words_in_liwc_file_anxiety=set(pd.read_csv(liwc_file_anxiety, header=None, delimiter=r"\s+")[0].tolist())
    
    liwc_file_sadness='../LIWC_lexicons/sadness'
    #words_in_liwc_file_sadness=set(pd.read_csv(liwc_file_sadness, header=None, delimiter=r"\s+")[0].tolist())
   
    liwc_file_swear='../LIWC_lexicons/swear'
    #words_in_liwc_file_swear=set(pd.read_csv(liwc_file_swear, header=None, delimiter=r"\s+")[0].tolist())
    
    ''' 2. Harvest data from million song database '''
    track_ids=[]
    years=[]
    durations=[]
    titles=[]
    lyrics_words_counts=[]
    
    stops = set(stopwords.words('english'))
    
    features_csv_file='../../ConvertToCSV/Outputs/features.tsv'
    features_df=pd.read_csv(features_csv_file, delimiter='\t')
    features_df=features_df[features_df['year']!=0]#we only consider songs with available year
    nb_selected_songs=len(features_df['year'].values)
    track_ids=features_df['track_id'].values
    titles=features_df['title'].values
    years=features_df['year'].values
    durations=features_df['duration'].values
    
    
    conn2 = sqlite3.connect('mxm_dataset.db')
    c2 = conn2.cursor()
    
    
    
    for track_id in track_ids:
        
        track_id=track_id[2:len(track_id)-1]
        words_counts=[]
            
        for selection2 in c2.execute('SELECT word,count FROM lyrics where track_id=\''+track_id+'\';'):
            '''if not selection2[0] in stops:#we remove stop words
            words_counts.append((selection2[0],selection2[1]))'''
            words_counts.append((selection2[0],selection2[1]))
            
        lyrics_words_counts.append(words_counts)
            
    conn2.close()        
    
    
    
    ''' 3. Compute LIWC scores for each song '''
    
    liwc_anger_scores=[] 
    liwc_anxiety_scores=[]
    liwc_neg_affect_scores=[]
    liwc_pos_affect_scores=[]
    liwc_sadness_scores=[]
    liwc_swear_scores=[]
    
    lyrics_availabilities=[]    
    
    
    for l_w_c in lyrics_words_counts:
        if l_w_c != []:
            l_words,l_counts=zip(*l_w_c)
            nb_words=0
            for count in l_counts:
                nb_words+=count
        
            text=''
    
            for i in range(len(l_words)):
                for k in range(l_counts[i]):
                    text=text+l_words[i]
                    
            lyrics_availabilities.append(True)
            liwc_anger_scores.append(liwc_score(text,nb_words,liwc_file_anger))
            liwc_anxiety_scores.append(liwc_score(text,nb_words,liwc_file_anxiety))
            liwc_neg_affect_scores.append(liwc_score(text,nb_words,liwc_file_neg_affect))
            liwc_pos_affect_scores.append(liwc_score(text,nb_words,liwc_file_pos_affect))
            liwc_sadness_scores.append(liwc_score(text,nb_words,liwc_file_sadness))
            liwc_swear_scores.append(liwc_score(text,nb_words,liwc_file_swear))
        else:
            lyrics_availabilities.append(False)
            liwc_anger_scores.append(-1.0)
            liwc_anxiety_scores.append(-1.0)
            liwc_neg_affect_scores.append(-1.0)
            liwc_pos_affect_scores.append(-1.0)
            liwc_sadness_scores.append(-1.0)
            liwc_swear_scores.append(-1.0)
        
            
        
    
    ''' 4. Store data for visualisation '''
    
    music_year_liwc_scores_dic={'track_id':track_ids,'year':years,'lyrics_availabe':lyrics_availabilities,
                                'anger_score':liwc_anger_scores,'anxiety_score':liwc_anxiety_scores,
                                'neg_affect_score':liwc_neg_affect_scores,'pos_affect_score':liwc_pos_affect_scores,
                                'sadness_score':liwc_sadness_scores,'swear_score':liwc_swear_scores}
    music_year_liwc_scores_df=pd.DataFrame(music_year_liwc_scores_dic)
    columns=['track_id','year','lyrics_availabe','anger_score','anxiety_score','neg_affect_score','pos_affect_score','sadness_score','swear_score']
    music_year_liwc_scores_df=music_year_liwc_scores_df[columns]
    music_year_liwc_scores_df=music_year_liwc_scores_df[music_year_liwc_scores_df.lyrics_availabe == True]
    music_year_liwc_scores_df = music_year_liwc_scores_df.drop('lyrics_availabe', 1)
    
    
    music_year_liwc_scores_df.to_csv("../csv_database/full_music_year_liwc_scores.csv",sep=',') 
    
    
    elapsed_time=time.time()-start_time
    print 'execution time = %f sec' % elapsed_time

