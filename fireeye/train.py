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
    for i, arr in enumerate(train_matrix):
        if train_category[i] == 1:
            p1_num += arr
            p1_denom += sum(arr)
        else:
            p0_num += arr
            p0_denom += sum(arr)
    p1_vect = log(p1_num / p1_denom)
    p0_vect = log(p0_num / p0_denom)
    return p0_vect, p1_vect, p_sex


def classify(vec_2_classify, p0_vec, p1_vec, p_class_1):
    p1 = sum(vec_2_classify * p1_vec) + log(p_class_1)
    p0 = sum(vec_2_classify * p0_vec) + log(1.0 - p_class_1)
    if p1 - p0 > 10:
        return 1
    else:
        return 0


def main():
    list_posts, list_classes = load_data_set()
    vocab_set = create_vocab_set(list_posts)
    vocab_list = list(vocab_set)
    vocab_index_map = {}
    for index, item in enumerate(vocab_list):
        vocab_index_map[item] = index

    train_mat = []
    for posting_doc in list_posts[:4000]:
        train_mat.append(word_set_2_vec(vocab_index_map, posting_doc))
    p0_v, p1_v, p_sex = train(array(train_mat), array(list_classes[:4000]))
    with open('prob.txt', 'w') as f:
        json.dump({
            'p0_v': list(p0_v),
            'p1_v': list(p1_v),
            'p_sex': p_sex,
            'vocab_map': vocab_index_map,
        }, f)


def test():
    list_posts, list_classes = load_data_set()
    with open('prob.txt', 'r') as f:
        prob = json.load(f)
    p0_v = array(prob['p0_v'])
    p1_v = array(prob['p1_v'])
    p_sex = prob['p_sex']
    vocab_index_map = prob['vocab_map']

    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    for index, posting_doc in enumerate(list_posts[4000:]):
        this_doc = array(word_set_2_vec(vocab_index_map, posting_doc))
        result = classify(this_doc, p0_v, p1_v, p_sex)
        if result == 1 and list_classes[4000 + index] == 1:
            count1 += 1
        if result == 0 and list_classes[4000 + index] == 1:
            count2 += 1
        if result == 1 and list_classes[4000 + index] == 0:
            count3 += 1
        if result == 0 and list_classes[4000 + index] == 0:
            count4 += 1
    print(count1, count2, count3, count4)

if __name__ == '__main__':
    test()
