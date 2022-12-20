# ml-graphology

## About
Graphology is a method of identifying, evaluating, and understanding human personality traits through the strokes and patterns revealed by handwriting.
Although human intervention in handwriting analysis has been effective, it is costly and prone to error. The project is a small attempt on developing a program that can predict the personality traits with the aid of machine learning without human intervention.

The details of the project is contained in the dissertation report `Psychological Analysis based on Handwriting Pattern with ML.pdf` provided in this repository.

Support Vector Machines (SVM) are used to classify the following handwriting features.
1. Top margin
2. Pen pressure
3. Baseline angle
4. Letter size
5. Line spacing
6. Word spacing
7. Slant angle

## Project Structure
1. `extract_routine.py` extracts all the features by calling `extract.py` and stores the raw feature values in a file `raw_feature_list`.
2. `raw_feature_list` is read by `feature_routine.py` and generates a file `feature_list` containing discrete feature values which can be used for training the classifiers.
3. Combinations of these features is used to train eight SVM classifiers to predict eight personality traits of a handwriting image input. `train_predict.py` trains the SVM classifiers and predicts input handwriting image.

## Training Data
For my own educational purpose, I am using the handwriting samples provided by https://fki.tic.heia-fr.ch/databases/iam-handwriting-database for non-profit usage.

The images obtained from the above non-profit source need to be cropped and resized to have similar resolutions of 850 pixels width and ~850 pixels length so that they can be used in the program. Images modification is not in the scope of this project. You can use photoshop or any method of your choice to modify the images en masse.

If you want a copy of my prepared data, you may contact me via https://www.linkedin.com/in/malem-mutum-506aa1167/.
As there is limit to the size of a commit in Github, I cannot put the data in this repository.