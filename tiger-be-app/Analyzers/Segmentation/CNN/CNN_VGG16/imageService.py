import os
from keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt

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

base_dir_clusters = 'data/stroma_data'
clusters_train_dir = base_dir_clusters + '/train'
clusters_test_dir = base_dir_clusters + '/test'


def get_number_of_images(img_dir):
    return len(os.listdir(img_dir))


def get_tf_img_batches_iterator(batch_size, img_dir, shape):
    image_gen_train = ImageDataGenerator(rescale=1./255)
    train_data_gen = image_gen_train.flow_from_directory(batch_size=batch_size,
                                                         directory=img_dir,
                                                         shuffle=True,
                                                         target_size=(shape, shape),
                                                         class_mode='binary')
    return train_data_gen


def show_image(img):
    # Show the image
    plt.imshow(img)
    plt.show()

