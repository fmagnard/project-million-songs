# -*- coding: utf-8 -*-

import time
import pandas as pd

def map_genre_to_emotion(genre):
    if genre=='Pop':
        return ['Happy','Angry']
            
    elif genre=='Rock':
        return ['Happy','Angry']
        
    elif genre=='Reggae':
        return ['Happy']
        
    elif genre=='Jazz':
        return ['Sad','Relax']
        
    elif genre=='Metal':
        return ['Angry']
        
    elif genre=='Country':
        return ['Happy','Relax','Sad']
        
    elif genre=='RnB':
        return ['Happy']
        
    elif genre=='Electronic':
        return ['Happy','Angry']
        
    elif genre=='Folk':
        return ['Sad','Relax']
   
    elif genre=='Punk':
        return ['Angry']
        
    elif genre=='Rap':
        return ['Angry']
        
    elif genre=='Blues':
        return ['Sad','Relax']
        
    elif genre=='Latin':
        return ['Happy']
        
    elif genre=='New Age':
        return ['Relax']
    else:
        
        raise NameError('this genre does not exist in the dataset')

if __name__=='__main__':
    start_time=time.time()
    
    features_df=pd.read_csv('../../ConvertToCSV/Outputs/features.tsv',delimiter='\t')
    liwc_scores_df=pd.read_csv('../csv_database/full_music_year_liwc_scores.csv',delimiter=',')
    thematic_importance_score_df=pd.read_csv('../csv_database/thematic_importance_scores.csv',delimiter=',')
    thematic_importance_score_df=thematic_importance_score_df.drop('Unnamed: 0',1)
    thematic_importance_score_df=thematic_importance_score_df.drop('year',1)
    genres_df=pd.read_csv('../genre_tags/genre_ground_truth/msd_tagtraum_cd2c.tsv',delimiter='\t')
    genres_df.columns=['track_id','genre']
    liwc_scores_df=liwc_scores_df.drop('Unnamed: 0',1)
    
    selected_features_df=features_df[['track_id','tempo','mode','loudness','key','duration']]
    modify_id = lambda x: x[2:len(x)-1]
    modify_id1= lambda x: x[1:len(x)-1]
    selected_features_df['track_id']=selected_features_df['track_id'].apply(modify_id)
    thematic_importance_score_df['track_id']=thematic_importance_score_df['track_id'].apply(modify_id1)
    audio_liwc_features_df=pd.merge(liwc_scores_df, selected_features_df, how='inner', on=['track_id'])
    audio_liwc_features_genres_df=pd.merge(audio_liwc_features_df, genres_df, how='inner', on=['track_id'])
    audio_liwc_features_genres_thematic_score=pd.merge(audio_liwc_features_genres_df, thematic_importance_score_df, how='inner', on=['track_id'])
    
    new_track_id=[]
    new_year=[]
    new_anger_score=[]
    new_anxiety_score=[]
    new_neg_affect_score=[]
    new_pos_affect_score=[]
    new_sadness_score=[]
    new_swear_score=[]
    new_tempo=[]
    new_mode=[]
    new_loudness=[]
    new_key=[]
    new_duration=[]
    emotions=[]
    new_love_importance=[]
    new_happiness_importance=[]
    new_peace_importance=[]
    new_sadness_importance=[]
    new_war_importance=[]
    
    audio_liwc_features_genres_thematic_score_withoutWorld_df=audio_liwc_features_genres_thematic_score[audio_liwc_features_genres_thematic_score['genre']!='World']
    
    genres=audio_liwc_features_genres_thematic_score_withoutWorld_df['genre'].unique()
    id1=0
    for index, row in audio_liwc_features_genres_thematic_score_withoutWorld_df.iterrows():
        
        related_emotions=map_genre_to_emotion(row['genre'])
        for j in range(len(related_emotions)):
            
            new_track_id.append(row['track_id'])
            new_year.append(row['year'])
            new_anger_score.append(row['anger_score'])
            new_anxiety_score.append(row['anxiety_score'])
            new_neg_affect_score.append(row['neg_affect_score'])
            new_pos_affect_score.append(row['pos_affect_score'])
            new_sadness_score.append(row['sadness_score'])
            new_swear_score.append(row['swear_score'])
            new_tempo.append(row['tempo'])
            new_mode.append(row['mode'])
            new_loudness.append(row['loudness'])
            new_key.append(row['key'])
            new_duration.append(row['duration'])
            emotions.append(related_emotions[j])
            new_love_importance.append(row['love_importance'])
            new_happiness_importance.append(row['happiness_importance'])
            new_peace_importance.append(row['peace_importance'])
            new_sadness_importance.append(row['sadness_importance'])
            new_war_importance.append(row['war_importance'])
        
        id1+=1
        if id1%1000==0:
            print id1
    
    audio_liwc_features_emotions_thematic_score_dic={'track_id':new_track_id,'year':new_year,
    'anger_score':new_anger_score,'anxiety_score':new_anxiety_score,
    'neg_affect_score':new_neg_affect_score,'pos_affect_score':new_pos_affect_score,
    'sadness_score':new_sadness_score,'swear_score':new_swear_score,
    'tempo':new_tempo,'mode':new_mode,'loudness':new_loudness,'key':new_key,
    'duration':new_duration,'emotion':emotions,'love_importance':new_love_importance,
    'happiness_importance':new_peace_importance,'peace_importance':new_peace_importance,
    'sadness_importance':new_sadness_importance,'war_importance':new_war_importance}
    audio_liwc_features_emotions_thematic_score_df=pd.DataFrame(audio_liwc_features_emotions_thematic_score_dic)  
    audio_liwc_features_emotions_thematic_score_df.to_csv('../csv_database/audio_liwc_features_emotions_thematic_score.csv',sep=",",index=False)
    
    print id1
    elapsed_time=time.time()-start_time
    print 'elapsed time = %f sec'% elapsed_time
    

