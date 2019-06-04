import io
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.utils import shuffle
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.callbacks import EarlyStopping
from keras.callbacks import ModelCheckpoint
from normalization import *
import matplotlib.pyplot as plt

from sklearn import svm, datasets
from sklearn.metrics import confusion_matrix

if __name__ == '__main__':
    #### normalization & standardization #######################
    print('standardization & normalization of the Data set + features selection')
    n = main()
    n.df = shuffle(n.df)
    print(tabulate(n.df[:30], headers='keys', tablefmt='psql'))
    x, y = n.getNormalizeXY()

    # Create a test/train split.  40% test
    # Split into train/test
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.40, random_state=42)

    x2, y2 = n.getNormalizeXY()
    x_train2, x_test2, y_train2, y_test2 = train_test_split(
        x2, y2, test_size=0.40, random_state=42)


    print(y.shape[1])

    # Create neural net
    model = Sequential()
    model.add(Dense(10, input_dim=x.shape[1], kernel_initializer='normal', activation='relu'))
    model.add(Dense(50, input_dim=x.shape[1], kernel_initializer='normal', activation='relu'))
    model.add(Dense(10, input_dim=x.shape[1], kernel_initializer='normal', activation='relu'))
    model.add(Dense(1, kernel_initializer='normal'))
    model.add(Dense(y.shape[1],activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    monitor = EarlyStopping(monitor='val_loss', min_delta=1e-3, patience=5, verbose=1, mode='auto')
    checkpointer = ModelCheckpoint(filepath = "best_weights.hdf5" , verbose = 0, save_best_only=True)
    model.fit(x_train,y_train,validation_data=(x_test,y_test),callbacks=[monitor,checkpointer],verbose=2,epochs=1000)
    model.load_weights('best_weights.hdf5')

    # Measure accuracy
    pred = model.predict(x_test2)
    pred = np.argmax(pred,axis=1)
    y_eval = np.argmax(y_test2,axis=1)
    score = metrics.accuracy_score(y_eval, pred)
    print("Validation score: {}".format(score))

    pred = model.predict(x_test2)
    pred = np.argmax(pred,axis=1)
    y_test2 = np.argmax(y_test2,axis=1)

    # Compute confusion matrix
    cm = confusion_matrix(y_test2, pred)
    np.set_printoptions(precision=2)
    print('Confusion matrix, without normalization')
    print(cm)
    plt.figure()
    plot_confusion_matrix(cm, ['normal', 'other'])

    # Normalize the confusion matrix by row (i.e by the number of samples
    # in each class)
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    print('Normalized confusion matrix')
    print(cm_normalized)
    plt.figure()
    plot_confusion_matrix(cm_normalized, ['normal', 'other'], title='Normalized confusion matrix')

    plt.show()