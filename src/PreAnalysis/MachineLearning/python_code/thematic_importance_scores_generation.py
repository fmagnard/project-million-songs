# -*- coding: utf-8 -*-


'''Computes an importance score for several themes'''

import time
import sys
import pandas as pd
import re
import sqlite3
import numpy as np
import math
from stemming.porter2 import stem

def number_of_thematic_words_in_lyrics(text,thematic_words_path):

    with open(thematic_words_path) as lexicon:
        return np.sum([len(re.findall(word[:-1], text)) for word in lexicon])*1.0
           

if __name__=='__main__':
    
    start_time=time.time()
    
    ''' Filepaths of the thematic words '''
    thematic_words_filepaths={'love':'../thematic_words/love.txt',
    'happiness':'../thematic_words/happiness.txt',
    'peace':'../thematic_words/peace.txt',
    'sadness':'../thematic_words/sadness.txt',
    'war':'../thematic_words/war.txt'}
                         
    
    '''  '''
    
    
    features_df=pd.read_csv('../../ConvertToCSV/Outputs/features.tsv',delimiter='\t',encoding='ascii')
    
    features_df_without_missing_year=features_df[features_df['year']!=0]
    trackID_year_df=features_df_without_missing_year[['track_id','year']]
    track_ids=trackID_year_df['track_id'].values
    years=trackID_year_df['year'].values
    nb_music_with_year=len(track_ids)
    unique_years=trackID_year_df['year'].unique()
    
    
    number_songs_with_theme_content={'love':0.0,'happiness':0.0,'peace':0.0,'sadness':0.0,'war':0.0}
    number_songs_with_lyrics=0.0
    love_importances=[]   
    
    
        
        
    
    years_with_lyrics=[]
    track_id_with_lyrics=[]
    track_occurancies={}
    track_love_importance_scores={}
    for theme in thematic_words_filepaths:
        track_occurancies[theme]=[]
        track_love_importance_scores[theme]=[]
    
            
    print('Launching bdd')
    conn2 = sqlite3.connect('mxm_dataset.db')
    c2 = conn2.cursor()
    
    count_index = 0
    interval = 0
    print('Starting '+str(nb_music_with_year))
    t = time.time()
    for index in range(nb_music_with_year):
        count_index += 1
        interval +=1
        if interval == 100:
            interval = 0
            print(str(count_index) + ' in ' + str(time.time()-t))
            
        
        t_id=track_ids[index]
        year=years[index]
        words=''   
        t_id=t_id[1:]
        
        for selection2 in c2.execute('SELECT word,count FROM lyrics where track_id='+t_id+';'):
            word=selection2[0]
            count=selection2[1]
            
            if type(word) is str:
                for i in range(count):
                    words=words+stem(word)+' '
        
        if words!='':
            years_with_lyrics.append(year)
            track_id_with_lyrics.append(t_id)
            
            number_songs_with_lyrics+=1
            for theme in thematic_words_filepaths:    
                occurancy=number_of_thematic_words_in_lyrics(words,thematic_words_filepaths[theme])
                track_occurancies[theme].append(occurancy)
                if occurancy>0:
                    number_songs_with_theme_content[theme]+=1
            
    conn2.close()
    
    print('Almost done')
    theme_importances_per_song_dic={'track_id':track_id_with_lyrics,'year':years_with_lyrics}
        
    for j in range(len(years_with_lyrics)):
        year=years_with_lyrics[j]
        
        nb_song=number_songs_with_lyrics
        for theme in thematic_words_filepaths: 
            oc=track_occurancies[theme][j]
            
            
            nb_song_with_love_content=number_songs_with_theme_content[theme]
            
            if nb_song_with_love_content>0:
                importance_score=oc*math.log(nb_song/nb_song_with_love_content)
            else:
                importance_score=0.0
            track_love_importance_scores[theme].append(importance_score)
            
            score_name=theme+'_importance'
            theme_importances_per_song_dic[score_name]=track_love_importance_scores[theme]
    theme_importances_per_song_df=pd.DataFrame(theme_importances_per_song_dic)
    theme_importances_per_song_df=theme_importances_per_song_df[['track_id','love_importance','happiness_importance','peace_importance','sadness_importance','war_importance','year']]
    
    theme_importances_per_song_df.to_csv('../csv_database/thematic_importance_scores.csv',sep=",")
    
    elapsed_time=time.time()-start_time
    print('elapsed time = '+str(elapsed_time)+' sec')
    
    
