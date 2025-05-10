"""
LSTM Init
=========

**Created**: 2024-02-20

- Umberto Griffo (umberto.griffo@mail.com): Initial model
- Samy Chehade (samy.chehade@elsys-design): Usage in initial program and description
- Florian Dupeyron (florian.dupeyron@elsys-design.com): Porting to VERITY-AI

Le modèle que l'on cherche à implémenter sert à répondre à la question suivante : 
- Est-ce qu'un moteur va rencontrer un problème dans son fonctionnement au bout d'un certain nombre de cycles de fonctionnement ?

Ce nombre de cycles de fonctionnement sera noté w1. On est donc dans un cas de classification binaire, car il n'y a que deux réponses possibles à cette question : oui ou non. 
"""

import keras
import pandas as pd
import numpy  as np
import os

from sklearn import preprocessing
from sklearn.metrics import confusion_matrix, recall_score, precision_score
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, LSTM

from pathlib import Path


import logging
import verity.api as vapi

vapi.init()

log = logging.getLogger("My Method")
cwd = (Path(__file__) / "..").resolve()


# Initialize seed
np.random.seed(1234)
PYTHONHASHSEED=0

# Load dataset
# TODO: Use Dataset API

dataset_path = (vapi._CTX.storage.datasets_folder / "lstm_reactor_data").resolve()

train_df = pd.read_csv(str(dataset_path / "PM_train.txt"), sep=" ", header=None)
train_df.drop(train_df.columns[[26, 27]], axis=1, inplace=True) 

# on supprime les colonnes 26 et 27 
# les doubles brackets servent à faire passer une liste d'indices de colonnes
# le inplace permet d'appliquer les modifications directement sur le DataFrame 

train_df.columns = ['id', 'cycle', 'setting1', 'setting2', 'setting3', 's1', 's2', 's3',
                     's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11', 's12', 's13', 's14',
                     's15', 's16', 's17', 's18', 's19', 's20', 's21']

train_df = train_df.sort_values(['id','cycle'])

print(train_df.head())

# read test data - It is the aircraft engine operating data without failure events recorded.
test_df = pd.read_csv(str(dataset_path / "PM_test.txt"), sep=" ", header=None)
test_df.drop(test_df.columns[[26, 27]], axis=1, inplace=True)
test_df.columns = ['id', 'cycle', 'setting1', 'setting2', 'setting3', 's1', 's2', 's3',
                     's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11', 's12', 's13', 's14',
                     's15', 's16', 's17', 's18', 's19', 's20', 's21']

print(test_df.head())

# Data Labeling - generate column RUL(Remaining Usefull Life or Time to Failure)
rul = pd.DataFrame(train_df.groupby('id')['cycle'].max()).reset_index() # On crée un Df avec pour chaque id son nombre de cycles total
rul.columns = ['id', 'max']

print(rul.head())

train_df = train_df.merge(rul, on=['id'], how='left') # 'left' pour garder toutes les colonnes du dataframe de gauche

train_df['RUL'] = train_df['max'] - train_df['cycle'] # la colonne RUL comporte donc le nombre de cycles restants pour chaque cycle
train_df.drop('max', axis=1, inplace=True)


# generate label columns for training data
# we will only make use of "label1" for binary classification, 
# while trying to answer the question: is a specific engine going to fail within w1 cycles?
w1 = 30
w0 = 15
train_df['label1'] = np.where(train_df['RUL'] <= w1, 1, 0 ) # on crée la colonne label 1 et on met les labels correspondants 1 si RUL <= w1 sinon 0
train_df['label2'] = train_df['label1']
train_df.loc[train_df['RUL'] <= w0, 'label2'] = 2


# MinMax normalization (from 0 to 1) Etape très importante du deep learning pour éviter des problèmes d'overflow ou de vanishing gradients 
train_df['cycle_norm'] = train_df['cycle']
cols_normalize = train_df.columns.difference(['id','cycle','RUL','label1','label2']) # on prend les colonnes des données capteurs seulement avec aussi la colonne cycle_norm
min_max_scaler = preprocessing.MinMaxScaler()
norm_train_df = pd.DataFrame(min_max_scaler.fit_transform(train_df[cols_normalize]), 
                             columns=cols_normalize, 
                             index=train_df.index)
join_df = train_df[train_df.columns.difference(cols_normalize)].join(norm_train_df) # on remplace avec les nouvelles données capteurs normalisées de 0 à 1 dans notre dataframe initial
train_df = join_df.reindex(columns = train_df.columns)

subset = train_df.iloc[190:195]
print(subset)


# read ground truth data - It contains the information of true remaining cycles for each engine in the testing data.
truth_df = pd.read_csv(str(dataset_path / "PM_truth.txt"), sep=" ", header=None)
truth_df.drop(truth_df.columns[[1]], axis=1, inplace=True)

print(truth_df.head())

# MinMax normalization (from 0 to 1)
test_df['cycle_norm'] = test_df['cycle']
norm_test_df = pd.DataFrame(min_max_scaler.transform(test_df[cols_normalize]), 
                            columns=cols_normalize, 
                            index=test_df.index)
test_join_df = test_df[test_df.columns.difference(cols_normalize)].join(norm_test_df)
test_df = test_join_df.reindex(columns = test_df.columns)
test_df = test_df.reset_index(drop=True)

# We use the ground truth dataset to generate labels for the test data.
# generate column max for test data
rul = pd.DataFrame(test_df.groupby('id')['cycle'].max()).reset_index()
rul.columns = ['id', 'max']
truth_df.columns = ['more']
truth_df['id'] = truth_df.index + 1
truth_df['max'] = rul['max'] + truth_df['more'] # on ajoute les cycles qui manque dans le fichier PM_test.txt
truth_df.drop('more', axis=1, inplace=True)

# generate RUL for test data
test_df = test_df.merge(truth_df, on=['id'], how='left')
test_df['RUL'] = test_df['max'] - test_df['cycle']
test_df.drop('max', axis=1, inplace=True)

# generate label columns w0 and w1 for test data
test_df['label1'] = np.where(test_df['RUL'] <= w1, 1, 0 )
test_df['label2'] = test_df['label1']
test_df.loc[test_df['RUL'] <= w0, 'label2'] = 2

subset = test_df.iloc[26:32]
print(subset)

##########

# pick a large window size of 50 cycles
sequence_length = 50

##########

# function to reshape features into (samples, time steps, features) 
def gen_sequence(id_df, seq_length, seq_cols):
    """ Only sequences that meet the window-length are considered, no padding is used. This means for testing
    we need to drop those which are below the window-length. An alternative would be to pad sequences so that
    we can use shorter ones """
    # for one id I put all the rows in a single matrix
    data_matrix = id_df[seq_cols].values
    num_elements = data_matrix.shape[0] # Matrice 2D lignes = nombre de cycles par id et colonnes = nombre de features
    # Iterate over two lists in parallel.
    # For example id1 have 192 rows and sequence_length is equal to 50
    # so zip iterate over two following list of numbers (0,142),(50,192)
    # 0 50 -> from row 0 to row 50
    # 1 51 -> from row 1 to row 51
    # 2 52 -> from row 2 to row 52
    # ...
    # 111 191 -> from row 111 to 191
    for start, stop in zip(range(0, num_elements-seq_length), range(seq_length, num_elements)):
        yield data_matrix[start:stop, : ]


# pick the feature columns 
sensor_cols = ['s' + str(i) for i in range(1,22)]
sequence_cols = ['setting1', 'setting2', 'setting3', 'cycle_norm']
sequence_cols.extend(sensor_cols)

# generator for the sequences
seq_gen = (list(gen_sequence(train_df[train_df['id']==id], sequence_length, sequence_cols)) 
           for id in train_df['id'].unique())

# generate sequences and convert to numpy array
seq_array = np.concatenate(list(seq_gen)).astype(np.float32)
print(seq_array.shape)

# matrice 3D avec :
# - 1 dimension pour le nombre total de séquences générées
# - 1 dimension pour le nombre de cycles par séquence
# - 1 dimension pour le nombre de variables par séquence


# function to generate labels
def gen_labels(id_df, seq_length, label):
    # For one id I put all the labels in a single matrix.
    # For example:
    # [[1]
    # [4]
    # [1]
    # [5]
    # [9]
    # ...
    # [200]] 
    data_matrix = id_df[label].values
    num_elements = data_matrix.shape[0]
    # I have to remove the first seq_length labels
    # because for one id the first sequence of seq_length size have as target
    # the last label (the previus ones are discarded).
    # All the next id's sequences will have associated step by step one label as target. 
    return data_matrix[seq_length:num_elements, :]


# generate labels
label_gen = [gen_labels(train_df[train_df['id']==id], sequence_length, ['label1']) 
             for id in train_df['id'].unique()]
label_array = np.concatenate(label_gen).astype(np.float32)
print(label_array.shape)


# Next, we build a deep network. 
# The first layer is an LSTM layer with 100 units followed by another LSTM layer with 50 units. 
# Dropout is also applied after each LSTM layer to control overfitting. 
# Final layer is a Dense output layer with single unit and sigmoid activation since this is a binary classification problem.
# build the network
nb_features = seq_array.shape[2]
nb_out = label_array.shape[1]

model = Sequential()

# chaque model.add correspond à une couche
# Couche 1  
model.add(LSTM(
         input_shape=(sequence_length, nb_features),
         units=100,
         return_sequences=True))
model.add(Dropout(0.2))

model.add(LSTM(
          units=50,
          return_sequences=False))
model.add(Dropout(0.2))

model.add(Dense(units=nb_out, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

print(model.summary())

# fit the network

with vapi.model_package("lstm_init", exchange_format="keras", target="agnostic") as vpkg:
    history = model.fit(
        seq_array,
        label_array,
        epochs=100,
        batch_size=200,
        validation_split=0.05,
        verbose=2,

        callbacks = [
            keras.callbacks.EarlyStopping(monitor='val_loss', min_delta=0, patience=10, verbose=0, mode='min'),
            keras.callbacks.ModelCheckpoint(str(vpkg.model_file_path), monitor='val_loss', save_best_only=True, mode='min', verbose=0)
        ]
    )

with vapi.metrics_save() as vkpi:
    vkpi.percentage("accuracy", history.history["accuracy"][-1])
    vkpi.percentage("loss",     history.history["loss"][-1])
    vkpi.simple("val_accuracy", history.history["val_accuracy"][-1])
    vkpi.simple("val_loss", history.history["val_loss"][-1])

####################################################

#with vapi.describe_arguments() as vargs:
#    vargs.add_argument("input_model", help="Test input model")
#    vargs.add_flag("optional", help="Test flag")
#
#
#input_model = vapi.argument("input_model")

#model_file, model_info = vapi.model_use("sru_binary_model_pruned_15_97-v0_1")
#
#log.info(f"Use model: {model_info.name}!")
#log.info(f"Model format: {model_info.exchange_format}")
#
#log.info(f"-> Model extracted to: {model_file}")
#
## Try save model back
#with vapi.model_package("test_output_model", model_info.exchange_format, model_info.target) as vpkg:
#    vpkg.model_file_path.write_bytes(model_file.read_bytes())
#
## Done :)
#
