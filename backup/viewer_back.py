from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math
import os
import sys

import tensorflow as tf
import numpy as np


from object_detection.im2txt.inference_utils import caption_generator
from object_detection.im2txt.inference_utils import vocabulary
from object_detection.im2txt import configuration
from object_detection.im2txt import inference_wrapper

checkpoint_path = "object_detection/data_IC/model/train"
vocab_file = "object_detection/data_IC/ImageCaptionData/word_counts.txt"
test_path = "/home/vrlab/human_caption/capTest/000370.jpg"

#a=tf.constant(1111)
#sess2=tf.Session()



def getCaption(path_img):
    print('Input path:''', path_img)

    # Build the inference graph.
    g = tf.Graph()
    with g.as_default():
        model = inference_wrapper.InferenceWrapper()
        restore_fn = model.build_graph_from_config(configuration.ModelConfig(),
                                                   checkpoint_path)
    g.finalize()

    in_file = checkpoint_path + '/checkpoint'
    with open(in_file, 'rb') as ckpt_file:
        line = ckpt_file.readline()

    line_a = line.split('-')
    current_num = line_a[1][:-2]
    print('Now checkpoint:', current_num)

    # Create the vocabulary.
    vocab = vocabulary.Vocabulary(vocab_file)

    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True


    with tf.Session(graph=g, config=config) as sess:
        # Load the model from checkpoint.
        restore_fn(sess)

        # Prepare the caption generator. Here we are implicitly using the default
        # beam search parameters. See caption_generator.py for a description of the
        # available beam search parameters.
        generator = caption_generator.CaptionGenerator(model, vocab)

        caption_total = {}

        filename = path_img

        with tf.gfile.GFile(filename, "r") as f:
            image = f.read()
        captions = generator.beam_search(sess, image)
        # print("********************")
        print("Captions for image %s:" % os.path.basename(filename))

        captions_input = []
        captions_list = []
        for i, caption in enumerate(captions):
            # Ignore begin and end words.
            sentence = [vocab.id_to_word(w) for w in caption.sentence[1:-1]]  # <S> and </S>
            # sentence = " ".join(sentence)
            sentence_fin = ""
            for word in sentence:
                if word == "." or word == "<S>":
                    sentence_fin += "."
                    break
                else:
                    sentence_fin += word + " "

            #print("  %d) %s (p=%f)" % (i, sentence_fin, math.exp(caption.logprob)))
            # print(len(sentence))
            item = [sentence_fin, math.exp(caption.logprob)]
            captions_list.append(sentence_fin)
            captions_input.append(item)

    str_caption = ''
    i = 1
    for oneSentence in captions_list:
        str_caption += 'Caption'
        str_caption += str(i)
        str_caption += ': '
        str_caption += oneSentence
        str_caption += '\n'
        i += 1

    return str_caption
