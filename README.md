### Emotional Diary  
Its purpose is to provide an opportunty to write, store and analyse people emotions. Just write what you think and the app will give you a hint what emotion you have.  

The desktop part was written using QT framework: https://www.qt.io/  
Machine learning model was trained on the dataset from kaggle: https://www.kaggle.com/datasets/nelgiriyewithana/emotions  

The app currently uses `xboost` model trained on the dataset above. Documents from these dataset was converted to vectors by `TF-IDF` technique. Accuracy on test - 90%.  

To launch this app on your device follow instructions below:
1) download the repo;
2) create venv;
3) download all dependencies by using `pip install -r requirements.txt`;
4) launch the app from a directory where the project is stored (not for inside the project directory) using `python -m emotion_analyser.app.main` command.
> This way of launching the app is needed due to relative paths to python modules.

Here are a few screenshots:  
The main window:  
![main](https://github.com/ivanaleksa/emotional-diary/blob/ivanaleksa-patch-1/main.png)  

The window to create a new note:  
![main](https://github.com/ivanaleksa/emotional-diary/blob/ivanaleksa-patch-1/new_note.png)  

One examples of possible diagrams:  
![main](https://github.com/ivanaleksa/emotional-diary/blob/ivanaleksa-patch-1/statistics.png)
