#MusicHistory

CSE6242 - TEAM 17 PROJECT
Exploring Large Scale 20th Century Music Features
Historical Patterns and Discoveries

*******
AUTHORS
*******
Auguste BYIRINGIRO, Mathieu LAPEYRE, Flore MAGNARD, Gireg MIORCEC DE KERDANET
Georgia Institute of Technology, CSE 6242, Group 17 Atlanta, GA

************
INTRODUCTION
************
This is the final deliverable of our Project for Data And Visual Analytics.
Output is located at http://cse6242-team17.aerobatic.io at least until the end of the semester.
We hope you will enjoy the results as much as we had fun working on it.
Major dataset (300GB) is The Million Song Dataset: http://labrosa.ee.columbia.edu/millionsong/
Source can be found as a public snapshot on AWS S3
Some processed data are located in /DOC/src/PreAnalysis/[folder]

*****
SETUP
*****
The project output is a webpage where all the results we have computed are already available. There is no particular setup:
- Go to DOC/src/Website/
- Open index.html in your browser
- You may pay attention to the XML Cross Referencing. If so, kindly open Chrome with access to Cross Origin:
	- OSX: open -a Google\ Chrome --args --disable-web-security
	- Linux: google-chrome --disable-web-security

*****
USAGE
*****
/DOC/src/Website
- Simply scroll down and follow the guidelines directly into the website. Let’s discover some interesting stuff!

/DOC/src/PreAnalysis
- The feature extraction is a major part of our project. Kindly refer to the following documentation:

+ PREVIEW
	- display_song.py: Displays a song's feature contained in a h5 file. (src : https://github.com/tbertinmahieux/MSongsDB/blob/master/PythonSrc/display_song.py; dependencies : hdf5_getters.py)
	- h5_example.txt: example of the result of display_song.py.
	- h5_description.txt: example of what a h5 file looks like.

+ CONVERTTOCSV
	- hdf5_getters.py: Provides getters to request values of a song's feature in a given hdf5 file. (src : https://github.com/tbertinmahieux/MSongsDB/blob/master/PythonSrc/hdf5_getters.py ; dependencies : pip install h5py)
	- millionSongDataset.py: Class that enables reading the Million Song Dataset.
	- hdf5_arrays2csv.py: Script that creates, for each feature of type array, a csv file containing the given feature for all songs. Since this would produce files of several Gigabytes, it was never used.
	- hdf5_num_str2csv.py: Script that creates, for each numeric or string feature, a csv file containing the given feature for all songs. The output file is features.csv.
	+ CONVERTER_TO_CSV_GIT: written by Mahieux Bertin but not used here.
	+ OUTPUT
		- features.tsv: contains all numerical and string features of the million songs.

+GETMISSINGYEARS
	- spotify_script.py: makes request to the Spotify API to retrieve more release dates or more precise release dates.
	+ OUTPUT:
		- features.tsv: contains all numerical and string features of the million songs, with, for some songs, previously unknown dates or more precise release dates.

+STATISTICS
	- features_count_per_year.py: Script that counts, for each feature, the number of songs for which we know the feature value.
	- features_mean_per_year.py: Script that computes, for each numerical feature, the mean feature values of all songs.
	- kmeans_global.py: Script that computes k-means clusters of songs with several numerical coordinates. (dependencies: pip install scikit-learn)
	- stats_location.py: computes a rough estimation of whether an artist is located in US or Canada.
	+ INPUT:	
		- unique_mbtags.txt: contains all unique artists musicbrainz tags (genre) (src: http://labrosa.ee.columbia.edu/millionsong/pages/getting-dataset)
		- unique_terms.txt: contains all unique terms in the lyrics (Echo Nest) (src: http://labrosa.ee.columbia.edu/millionsong/pages/getting-dataset)
		- artist_location.txt: contains all unique artist's location (src: http://labrosa.ee.columbia.edu/millionsong/pages/getting-dataset)
	+ OUTPUT:
		- locations_by_artist.txt: output of stats_location.py
		- scatterplot_features.txt: output of kmeans_global.py
		- features_mean_per_year.tsv: output of features_mean_per_year.py
		- features_count_per_year.tsv: output of features_count_per_year.py

+ MACHINELEARNING:
	+ CSV_DATABASE:
		- audio_liwc_features_emotions_thematic_score.csv: output  of groundtruth_emotion_from_genre_generation.py
		- audio_liwc_features_emotions.csv
		- full_music_year_liwc_scores.csv: output of create_csv_file_year_liwc_scores.py
		- thematic_importance_scores.csv: output of thematic_importance_scores_generation.py

	+ GENRE_TAGS:
		+ GENRE_GROUND_TRUTH:
			- msd_tagtraum_cd2c.tsv: contains available music genres

	+ LIWC_LEXICONS(used to generate LIWC scores):
		- anger: lexicon of anger words
		- anxiety: lexicon of anger words
		- positive_affect: lexicon of positive affect words
		- negative_affect: lexicon of negative affect words
		- sadness: lexicon of sadness words
		- swear: lexicon of swear words

	+ PYTHON_CODE:
		- create_csv_file_year_liwc_scores.py: generates LIWC scores (requires mxm_dataset.db available here http://labrosa.ee.columbia.edu/millionsong/sites/default/files/AdditionalFiles/mxm_dataset.db)
		- emotion_classification.py: does emotion classification using lyrics features and audio features.
		- groundtruth_emotion_from_genre_generation.py: generates audio_liwc_features_emotions_thematic_score.csv
		- predict_decade_ml_audio_features_classification.py: does decade classification from audio features
		- predict_year_ml_liwc_score.py: does decade classification from LIWC scores
		- thematic_importance_scores_generation.py: Computes an importance score for several themes. (dependencies: pip install stemming). Also requires mxm_dataset.db

	+ THEMATIC_WORDS (used to generate thematic importance scores):
		- happiness.txt: lexicon with words related to happiness
		- love.txt: lexicon with words related to love
		- peace.txt: lexicon with words related to peace
		- sadness.txt: lexicon with words related to sadness
		- war.txt: lexicon with words related to war