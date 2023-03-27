import pickle
import os
import numpy as np

from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input

PATH_TO_BASE_DIRECTORY = 'utils'
PATH_TO_IMAGE_DIRECTORY = 'static/uploads'

def init_all_captions():
    # load and return all_captions
    return pickle.load(open(os.path.join(PATH_TO_BASE_DIRECTORY, 'all_captions.pkl'), 'rb'))

def init_feature_model():
    # load and return feature_model
    return pickle.load(open(os.path.join(PATH_TO_BASE_DIRECTORY, 'feature_model.pkl'), 'rb'))

def init_model():
    # load and return the model
    return pickle.load(open(os.path.join(PATH_TO_BASE_DIRECTORY, 'trained_model_30k_10e_32b'), 'rb'))

def init_tokenizer():
    # return the tokenized text
    return pickle.load(open(os.path.join(PATH_TO_BASE_DIRECTORY, 'tokenizer.pkl'), 'rb'))

def get_vocab_size(tokenizer):
    # return the vocab_size
    return len(tokenizer.word_index) + 1

def get_max_length(all_captions):
    # get maximum length of the caption available
    return max(len(caption.split()) for caption in all_captions)

def load_features(img_name, feature_model):
    # load the image from file
    img_path = PATH_TO_IMAGE_DIRECTORY + '/' + img_name
    image = load_img(img_path, target_size=(224, 224))
    # convert image pixels to numpy array
    image = img_to_array(image)
    # reshape data for model
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    # preprocess image for vgg
    image = preprocess_input(image)
    # extract features
    return feature_model.predict(image, verbose=0)

def idx_to_word(integer, tokenizer):
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None

# generate caption for an image
def predict_caption(model, image, tokenizer, max_length):
    # add start tag for generation process
    in_text = 'startseq'
    # iterate over the max length of sequence
    for i in range(max_length):
        # encode input sequence
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        # pad the sequence
        sequence = pad_sequences([sequence], max_length)
        # predict next word
        yhat = model.predict([image, sequence], verbose=0)
        # get index with high probability
        yhat = np.argmax(yhat)
        # convert index to word
        word = idx_to_word(yhat, tokenizer)
        # stop if word not found
        if word is None:
            break
        # append word as input for generating next word
        in_text += " " + word
        # stop if we reach end tag
        if word == 'endseq':
            break
      
    return in_text

def generate_caption(image_name):
    # load the image
    feature_model = init_feature_model()
    feature = load_features(image_name, feature_model)

    # initialize model
    all_captions = init_all_captions()
    model = init_model()
    tokenizer = init_tokenizer()
    max_length = get_max_length(all_captions)

    # predict and return the caption
    return predict_caption(model, feature, tokenizer, max_length).replace('startseq ', '').replace(' endseq', '')