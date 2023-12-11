from keras.applications import VGG16
from keras.callbacks import EarlyStopping
from keras.optimizers import Adam, RMSprop, SGD, Adagrad
from matplotlib import pyplot as plt
import tensorflow as tf

from bayes_search import bayes_search, BATCH_SIZE, random_search
from imageService import train_dir, test_dir, base_dir_tumor, clusters_train_dir, clusters_test_dir, base_dir_clusters, \
    val_dir, train_dir_s, val_dir_s, test_dir_s, base_dir_stroma, train_dir_o, val_dir_o, test_dir_o, base_dir_others
from imageService import get_tf_img_batches_iterator


DEFAULT_IMG_SHAPE = 224
EPOCH_NUMBER = 100

lr = 0.001
drop = 0.4
batch = 64
solver = 'adam'

# Define VGG19 base model

# Create CNN model with VGG19 base
def create_model(base_model, dropout, optimizer):
    # Freeze layers
    for layer in base_model.layers:
        layer.trainable = False

    last_layer = base_model.get_layer('block5_pool')
    last_output = last_layer.output
    x = tf.keras.layers.GlobalMaxPooling2D()(last_output)
    x = tf.keras.layers.Dense(512, activation='relu')(x)
    x = tf.keras.layers.Dropout(dropout)(x)
    x = tf.keras.layers.Dense(2, activation='sigmoid')(x)

    model = tf.keras.Model(base_model.input, x)

    if optimizer == 'adam':
        opt = Adam()
    elif optimizer == 'sgd':
        opt = SGD()
    elif optimizer == 'adagrad':
        opt = Adagrad()
    elif optimizer == 'rmsprop':
        opt = RMSprop()
    else:
        raise ValueError('Invalid optimizer')

    model.compile(optimizer=opt, loss=tf.keras.losses.sparse_categorical_crossentropy, metrics=['acc'])
    return model

def start_classification_of_segments_binary_tumor():
    print(f"Zacinam klasifikaciu TUMOR")
    train_data_gen = get_tf_img_batches_iterator(BATCH_SIZE, train_dir, DEFAULT_IMG_SHAPE)
    val_data_gen = get_tf_img_batches_iterator(BATCH_SIZE, val_dir, DEFAULT_IMG_SHAPE)
    test_data_gen = get_tf_img_batches_iterator(BATCH_SIZE, test_dir, DEFAULT_IMG_SHAPE)

    best_params = bayes_search(train_data_gen, val_data_gen)
    base_model = VGG16(weights='imagenet', include_top=False, input_shape=(DEFAULT_IMG_SHAPE, DEFAULT_IMG_SHAPE, 3))
    model = create_model(base_model,
                         dropout=best_params['dropout'],
                         optimizer=best_params['solver'])
    total_train = train_data_gen.n
    total_val = val_data_gen.n
    es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=5)

    # nechat es nech stopne skor na zaklade val sady
    vgg_classifier = model.fit(train_data_gen,
                               steps_per_epoch=(total_train // best_params['batch_size']),
                               epochs=EPOCH_NUMBER,
                               validation_data=val_data_gen,
                               validation_steps=(total_val // best_params['batch_size']),
                               callbacks=[es],
                               batch_size=best_params['batch_size'],
                               verbose=1,
                               workers=4)
    result = model.evaluate(test_data_gen, batch_size=best_params['batch_size'])
    print("test_loss, test accuracy", result)
    model_json = model.to_json()
    with open(f"{base_dir_tumor}/VGG_Classifier_With_Validation.json", "w") as json_file:
        json_file.write(model_json)
    model.save(f"{base_dir_tumor}/VGG_Classifier_With_Validation.h5")
    print("Saved model to disk")
    model.save_weights(f"{base_dir_tumor}/VGG_Weights_With_Validation.h5")


def start_classification_of_segments_binary_stroma():
    print(f"Zacinam klasifikaciu STROMA")
    train_data_gen = get_tf_img_batches_iterator(BATCH_SIZE, train_dir_s, DEFAULT_IMG_SHAPE)
    val_data_gen = get_tf_img_batches_iterator(BATCH_SIZE, val_dir_s, DEFAULT_IMG_SHAPE)
    test_data_gen = get_tf_img_batches_iterator(BATCH_SIZE, test_dir_s, DEFAULT_IMG_SHAPE)

    best_params = bayes_search(train_data_gen, val_data_gen)
    base_model = VGG16(weights='imagenet', include_top=False, input_shape=(DEFAULT_IMG_SHAPE, DEFAULT_IMG_SHAPE, 3))
    model = create_model(base_model,
                         dropout=best_params['dropout'],
                         optimizer=best_params['solver'])
    total_train = train_data_gen.n
    total_val = val_data_gen.n
    es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=5)

    # nechat es nech stopne skor na zaklade val sady
    vgg_classifier = model.fit(train_data_gen,
                               steps_per_epoch=(total_train // best_params['batch_size']),
                               epochs=EPOCH_NUMBER,
                               validation_data=val_data_gen,
                               validation_steps=(total_val // best_params['batch_size']),
                               callbacks=[es],
                               batch_size=best_params['batch_size'],
                               verbose=1,
                               workers=4)
    result = model.evaluate(test_data_gen, batch_size=best_params['batch_size'])
    print("test_loss, test accuracy", result)
    model_json = model.to_json()
    with open(f"{base_dir_stroma}/VGG_Classifier_With_Validation.json", "w") as json_file:
        json_file.write(model_json)
    model.save(f"{base_dir_stroma}/VGG_Classifier_With_Validation.h5")
    print("Saved model to disk")
    model.save_weights(f"{base_dir_stroma}/VGG_Weights_With_Validation.h5")


def start_classification_of_segments_binary_others():
    print(f"Zacinam klasifikaciu STROMA")
    train_data_gen = get_tf_img_batches_iterator(BATCH_SIZE, train_dir_o, DEFAULT_IMG_SHAPE)
    val_data_gen = get_tf_img_batches_iterator(BATCH_SIZE, val_dir_o, DEFAULT_IMG_SHAPE)
    test_data_gen = get_tf_img_batches_iterator(BATCH_SIZE, test_dir_o, DEFAULT_IMG_SHAPE)

    best_params = bayes_search(train_data_gen, val_data_gen)
    base_model = VGG16(weights='imagenet', include_top=False, input_shape=(DEFAULT_IMG_SHAPE, DEFAULT_IMG_SHAPE, 3))
    model = create_model(base_model,
                         dropout=best_params['dropout'],
                         optimizer=best_params['solver'])
    total_train = train_data_gen.n
    total_val = val_data_gen.n
    es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=5)

    # nechat es nech stopne skor na zaklade val sady
    vgg_classifier = model.fit(train_data_gen,
                               steps_per_epoch=(total_train // best_params['batch_size']),
                               epochs=EPOCH_NUMBER,
                               validation_data=val_data_gen,
                               validation_steps=(total_val // best_params['batch_size']),
                               callbacks=[es],
                               batch_size=best_params['batch_size'],
                               verbose=1,
                               workers=4)
    result = model.evaluate(test_data_gen, batch_size=best_params['batch_size'])
    print("test_loss, test accuracy", result)
    model_json = model.to_json()
    with open(f"{base_dir_others}/VGG_Classifier_With_Validation.json", "w") as json_file:
        json_file.write(model_json)
    model.save(f"{base_dir_others}/VGG_Classifier_With_Validation.h5")
    print("Saved model to disk")
    model.save_weights(f"{base_dir_others}/VGG_Weights_With_Validation.h5")

def start_classification_of_segments_binary_random():
    print(f"Zacinam klasifikaciu")
    train_data_gen = get_tf_img_batches_iterator(BATCH_SIZE, train_dir, DEFAULT_IMG_SHAPE)
    test_data_gen = get_tf_img_batches_iterator(BATCH_SIZE, test_dir, DEFAULT_IMG_SHAPE)

    best_params = random_search(train_data_gen, test_data_gen)

    base_model = VGG16(weights='imagenet', include_top=False, input_shape=(DEFAULT_IMG_SHAPE, DEFAULT_IMG_SHAPE, 3))
    model = create_model(base_model,
                         dropout=best_params['dropout'],
                         optimizer=best_params['solver'])
    total_train = train_data_gen.n
    es = EarlyStopping(monitor='loss', mode='min', verbose=1, patience=5)
    vgg_classifier = model.fit(train_data_gen,
                               steps_per_epoch=(total_train // best_params['batch_size']),
                               epochs=EPOCH_NUMBER,
                               batch_size=best_params['batch_size'],
                               verbose=1)

    result = model.evaluate(test_data_gen, batch_size=best_params['batch_size'])
    print("test_loss, test accuracy", result)
    model_json = model.to_json()
    with open(f"{base_dir_tumor}/VGG_Classifier_R.json", "w") as json_file:
        json_file.write(model_json)
    model.save(f"{base_dir_tumor}/VGG_Classifier_R.h5")
    print("Saved model to disk")
    model.save_weights(f"{base_dir_tumor}/VGG_Weights_R.h5")


def start_classification_of_number_clusters():
    print(f"Zacinam klasifikaciu")
    train_data_gen = get_tf_img_batches_iterator(BATCH_SIZE, clusters_train_dir, DEFAULT_IMG_SHAPE)
    test_data_gen = get_tf_img_batches_iterator(BATCH_SIZE, clusters_test_dir, DEFAULT_IMG_SHAPE)

    # Load the VGG16 model without the top layers
    pre_trained_model = VGG16(include_top=False, input_shape=(DEFAULT_IMG_SHAPE, DEFAULT_IMG_SHAPE, 3))

    # VGG-16, is already trained on huge data
    for layer in pre_trained_model.layers:
        print(layer.name)
        layer.trainable = False

    last_layer = pre_trained_model.get_layer('block5_pool')
    last_output = last_layer.output
    x = tf.keras.layers.GlobalMaxPooling2D()(last_output)
    x = tf.keras.layers.Dense(512, activation='relu')(x)
    x = tf.keras.layers.Dropout(0.5)(x)
    # multi classification
    x = tf.keras.layers.Dense(3, activation='softmax')(x)

    model = tf.keras.Model(pre_trained_model.input, x)
    model.compile(optimizer='adam', loss=tf.keras.losses.categorical_crossentropy, metrics=['acc'])
    model.summary()
    total_train = train_data_gen.n

    vgg_classifier = model.fit(train_data_gen,
                               steps_per_epoch=(total_train // BATCH_SIZE),
                               epochs=10,
                               batch_size=BATCH_SIZE,
                               verbose=1)

    result = model.evaluate(test_data_gen, batch_size=BATCH_SIZE)
    print("test_loss, test accuracy", result)

    plt.plot(vgg_classifier.history["acc"])
    plt.plot(vgg_classifier.history['val_acc'])
    plt.plot(vgg_classifier.history['loss'])
    plt.plot(vgg_classifier.history['val_loss'])
    plt.title("model accuracy")
    plt.ylabel("Accuracy")
    plt.xlabel("Epoch")
    plt.legend(["Accuracy", "Validation Accuracy", "loss", "Validation Loss"])
    plt.show()

    model_json = model.to_json()
    with open(f"{base_dir_clusters}/VGG_Classifier.json", "w") as json_file:
        json_file.write(model_json)
    model.save(f"{base_dir_clusters}/VGG_Classifier.h5")

    print("Saved model to disk")
    model.save_weights(f"{base_dir_clusters}/VGG_Weights.h5")



