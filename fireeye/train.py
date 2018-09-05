# -*- coding: utf-8 -*-
"""贝叶斯训练数据"""
import json
from numpy import *


def load_data_set():
    with open('data.txt', 'r') as f:
        data = json.load(f)

    posting_list = []
    class_vec = []
    for item in data:
        posting_list.append(item['word'])
        class_vec.append(item['kind'])
    return posting_list, class_vec


def create_vocab_set(data_set):
    vocal_set = set()
    for document in data_set:
        vocal_set |= set(document)
    return vocal_set


def word_set_2_vec(vocab_index_map, input_set):
    return_vec = [0] * len(vocab_index_map)
    for word in input_set:
        if word in vocab_index_map:
            return_vec[vocab_index_map[word]] = 1
    return return_vec


def train(train_matrix, train_category):
    num_train_docs = len(train_matrix)
    num_words = len(train_matrix[0])
    p_sex = sum(train_category) / num_train_docs
    p0_num = ones(num_words)
    p1_num = ones(num_words)
    p0_denom = 2.0
    p1_denom = 2.0
    for i in range(num_train_docs):
        if train_category[i] == 1:
            p1_num += train_matrix[i]
            p1_denom += sum(train_matrix[i])
        else:
            p0_num += train_matrix[i]
            p0_denom += sum(train_matrix[i])
    p1_vect = log(p1_num/p1_denom)
    p0_vect = log(p0_num/p0_denom)
    return p0_vect, p1_vect, p_sex


def classify(vec_2_classify, p0_vec, p1_vec, p_class_1):
    p1 = sum(vec_2_classify * p1_vec) + log(p_class_1)
    p0 = sum(vec_2_classify * p0_vec) + log(1.0 - p_class_1)
    if p1 > p0:
        return 1
    else:
        return 0


def testing():
    list_posts, list_classes = load_data_set()
    vocab_set = create_vocab_set(list_posts)
    vocab_list = list(vocab_set)
    vocab_index_map = {}
    for index, item in enumerate(vocab_list):
        vocab_index_map[item] = index

    print(111111)
    train_mat = []
    for posting_doc in list_posts[:4000]:
        train_mat.append(word_set_2_vec(vocab_index_map, posting_doc))
    print(1111111)
    p0_v, p1_v, p_sex = train(array(train_mat), array(list_classes))
    print(p0_v)
    print(p1_v)
    print(p_sex)

if __name__ == '__main__':
    testing()