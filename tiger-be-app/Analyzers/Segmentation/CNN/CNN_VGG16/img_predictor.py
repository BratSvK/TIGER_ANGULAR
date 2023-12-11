import numpy as np
import keras.utils as image
from keras.models import load_model
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix

base_dir_tumor = 'data/tumor_data'
train_dir = base_dir_tumor + '/train'
test_dir = base_dir_tumor + '/test'
val_dir = base_dir_tumor + '/val'

base_dir_stroma = 'data/stroma_data'
train_dir_s = base_dir_stroma + '/train'
test_dir_s = base_dir_stroma + '/test'
val_dir_s = base_dir_stroma + '/val'

base_dir_others = 'data/others_data'
train_dir_o = base_dir_others + '/train'
test_dir_o = base_dir_others + '/test'
val_dir_o = base_dir_others + '/val'

base_dir_clusters = 'Analyzers/Segmentation/CNN/CNN_VGG16/data/segment_clusters'
clusters_train_dir = base_dir_clusters + '/train'
clusters_test_dir = base_dir_clusters + '/test'

def predict_binary():
    print("Here i am going to predict")
    img = image.load_img(f"{test_dir}/tumor/TCGA-AO-A0J6-01Z-00-DX1.D0C003CE-E112-4375-953D-78404C9D62DA_[42567, 11629, 42873, 11918].png",
                         target_size=(224, 224))
    img = np.asarray(img)
    plt.imshow(img)
    plt.show()
    img = np.expand_dims(img, axis=0)
    smodel = load_model(f"{base_dir_clusters}/VGG_Classifier.h5")
    output = smodel.predict(img)

    # Convert probabilities to class labels
    y_pred = output.argmax(axis=1)
    if y_pred > 0:
        print("tumor")
    else:
        print('no tumor')


def predict_multiple(path):
    img = image.load_img(path, target_size=(224, 224))
    img = np.asarray(img)
    #plt.imshow(img)
    #plt.show()
    img = np.expand_dims(img, axis=0)
    img = img / 255.0  # Normalize pixel values to [0, 1]
    smodel = load_model(f"{base_dir_clusters}/VGG_Classifier.h5")
    output = smodel.predict(img)
    # Map the predicted classes to 1, 2, or 3 clusters
    pred_cluster = np.argmax(output) + 1
    return pred_cluster
    #print(f"Predicted cluster: {pred_cluster}")



def create_confuison_matrix(base_model_path, train_gen_data, batch_size):
    print("Confusion matrix")
    # Get all ground truth labels
    y_true = train_gen_data.classes
    saved_model = load_model(f"{base_model_path}/VGG_Classifier_With_Validation.h5")
    y_pred_prob  = saved_model.predict(train_gen_data, batch_size=batch_size)
    # Convert probabilities to class labels
    y_pred = y_pred_prob.argmax(axis=1)

    # Create confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    print(cm)