# ml-graphology

## About
Graphology is a method of identifying, evaluating, and understanding human personality traits through the strokes and patterns revealed by handwriting.
Although human intervention in handwriting analysis has been effective, it is costly and prone to error. The project is a small attempt on developing a program that can predict the personality traits with the aid of machine learning without human intervention.

The details of the project is contained in the dissertation report `Psychological Analysis based on Handwriting Pattern with ML.pdf` provided in this repository.

Support Vector Machines (SVM) are used to classify the following handwriting features into a few selected personality traits.
1. Top margin
2. Pen pressure
3. Baseline angle
4. Letter size
5. Line spacing
6. Word spacing
7. Slant angle

## Project Structure
1. The `extract_routine.py` reads the handwriting images from a folder named `images` in the same directory and extracts all the features by calling `extract.py`. The extracted raw feature values are stored in a file `raw_feature_list`.
2. The `raw_feature_list` is read by `feature_routine.py` and mapped into discrete values. The discrete values are put into a file `feature_list`.
3. The `label_routine.py` generates the personality traits of the handwriting features into a file `label_list` by reading the `feature_list`. This is where principles of graphology comes into picture. The `label_list` is used for training the classifiers.
4. Combinations of the selected handwriting features are used to train eight SVM classifiers to predict eight personality traits of a handwriting image input. `train_predict.py` trains the SVM classifiers by reading the `label_list` and predicts input handwriting image.

## Training Data
For my own educational purpose, I am using the handwriting samples provided by https://fki.tic.heia-fr.ch/databases/iam-handwriting-database for non-profit usage.

The images obtained from the above non-profit source need to be cropped and resized to have similar resolutions of 850 pixels width and ~850 pixels length so that they can be used in the program. Images modification is not in the scope of this project. You can use photoshop or any method of your choice to modify the images en masse.

As there is limit to the size of a commit in Github, I cannot put the data in this repository.
The prepared data can be downloaded here https://drive.proton.me/urls/CCFB5R73RG#XUfhPiyr8ZBM
