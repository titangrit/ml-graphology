# ml-graphology
Graphology is defined as the analysis of the physical characteristics and patterns of the handwriting of an individual to understand his or her psychological state at the time of writing.

The proposed methodology extracts seven handwriting features, namely:
1. top margin, 
2. pen pressure,
3. baseline angle,
4. letter size,
5. line spacing,
6. word spacing and
7. slant angle.

`extract_routine.py` extracts all the features by calling `extract.py` and stores the raw features value in `raw_feature_list`.
`raw_feature_list` is read by `feature_routine.py` and generates `feature_list` containing discrete feature values which can be used for training a classifier.

Combinations of these features is used to train eight SVM classifiers to predict eight personality traits of the writer.
`train_predict.py` trains the SVM classifiers and predicts new handwriting samples.