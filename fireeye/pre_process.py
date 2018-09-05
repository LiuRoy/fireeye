# -*- coding: utf-8 -*-
"""预处理数据"""
import re
import json


stop_words = {
    "a", "able", "about", "above", "according",
    "accordingly", "across", "actually", "after", "afterwards",
    "again", "against", "ain't", "all", "allow",
    "allows", "almost", "alone", "along", "already",
    "also", "although", "always", "am", "among",
    "amongst", "an", "and", "another", "any",
    "anybody", "anyhow", "anyone", "anything", "anyway",
    "anyways", "anywhere", "apart", "appear", "appreciate",
    "appropriate", "are", "aren't", "around", "as",
    "aside", "ask", "asking", "associated", "at",
    "available", "away", "awfully", "be", "became",
    "because", "become", "becomes", "becoming", "been",
    "before", "beforehand", "behind", "being", "believe",
    "below", "beside", "besides", "best", "better",
    "between", "beyond", "both", "brief", "but",
    "by", "c'mon", "c's", "came", "can",
    "can't", "cannot", "cant", "cause", "causes",
    "certain", "certainly", "changes", "clearly", "co",
    "com", "come", "comes", "concerning", "consequently",
    "consider", "considering", "contain", "containing", "contains",
    "corresponding", "could", "couldn't", "course", "currently",
    "definitely", "described", "despite", "did", "didn't",
    "different", "do", "does", "doesn't", "doing",
    "don't", "done", "down", "downwards", "during",
    "each", "edu", "eg", "eight", "either",
    "else", "elsewhere", "enough", "entirely", "especially",
    "et", "etc", "even", "ever", "every",
    "everybody", "everyone", "everything", "everywhere", "ex",
    "exactly", "example", "except", "far", "few",
    "fifth", "first", "five", "followed", "following",
    "follows", "for", "former", "formerly", "forth",
    "four", "from", "further", "furthermore", "get",
    "gets", "getting", "given", "gives", "go",
    "goes", "going", "gone", "got", "gotten",
    "greetings", "had", "hadn't", "happens", "hardly",
    "has", "hasn't", "have", "haven't", "having",
    "he", "he's", "hello", "help", "hence",
    "her", "here", "here's", "hereafter", "hereby",
    "herein", "hereupon", "hers", "herself", "hi",
    "him", "himself", "his", "hither", "hopefully",
    "how", "howbeit", "however", "i'd", "i'll",
    "i'm", "i've", "ie", "if", "ignored",
    "immediate", "in", "inasmuch", "inc", "indeed",
    "indicate", "indicated", "indicates", "inner", "insofar",
    "instead", "into", "inward", "is", "isn't",
    "it", "it'd", "it'll", "it's", "its",
    "itself", "just", "keep", "keeps", "kept",
    "know", "known", "knows", "last", "lately",
    "later", "latter", "latterly", "least", "less",
    "lest", "let", "let's", "like", "liked",
    "likely", "little", "look", "looking", "looks",
    "ltd", "mainly", "many", "may", "maybe",
    "me", "mean", "meanwhile", "merely", "might",
    "more", "moreover", "most", "mostly", "much",
    "must", "my", "myself", "name", "namely",
    "nd", "near", "nearly", "necessary", "need",
    "needs", "neither", "never", "nevertheless", "new",
    "next", "nine", "no", "nobody", "non",
    "none", "noone", "nor", "normally", "not",
    "nothing", "novel", "now", "nowhere", "obviously",
    "of", "off", "often", "oh", "ok",
    "okay", "old", "on", "once", "one",
    "ones", "only", "onto", "or", "other",
    "others", "otherwise", "ought", "our", "ours",
    "ourselves", "out", "outside", "over", "overall",
    "own", "particular", "particularly", "per", "perhaps",
    "placed", "please", "plus", "possible", "presumably",
    "probably", "provides", "que", "quite", "qv",
    "rather", "rd", "re", "really", "reasonably",
    "regarding", "regardless", "regards", "relatively", "respectively",
    "right", "said", "same", "saw", "say",
    "saying", "says", "second", "secondly", "see",
    "seeing", "seem", "seemed", "seeming", "seems",
    "seen", "self", "selves", "sensible", "sent",
    "serious", "seriously", "seven", "several", "shall",
    "she", "should", "shouldn't", "since", "six",
    "so", "some", "somebody", "somehow", "someone",
    "something", "sometime", "sometimes", "somewhat", "somewhere",
    "soon", "sorry", "specified", "specify", "specifying",
    "still", "sub", "such", "sup", "sure",
    "t's", "take", "taken", "tell", "tends",
    "th", "than", "thank", "thanks", "thanx",
    "that", "that's", "thats", "the", "their",
    "theirs", "them", "themselves", "then", "thence",
    "there", "there's", "thereafter", "thereby", "therefore",
    "therein", "theres", "thereupon", "these", "they",
    "they'd", "they'll", "they're", "they've", "think",
    "third", "this", "thorough", "thoroughly", "those",
    "though", "three", "through", "throughout", "thru",
    "thus", "to", "together", "too", "took",
    "toward", "towards", "tried", "tries", "truly",
    "try", "trying", "twice", "two", "un",
    "under", "unfortunately", "unless", "unlikely", "until",
    "unto", "up", "upon", "us", "use",
    "used", "useful", "uses", "using", "usually",
    "value", "various", "very", "via", "viz",
    "vs", "want", "wants", "was", "wasn't",
    "way", "we", "we'd", "we'll", "we're",
    "we've", "welcome", "well", "went", "were",
    "weren't", "what", "what's", "whatever", "when",
    "whence", "whenever", "where", "where's", "whereafter",
    "whereas", "whereby", "wherein", "whereupon", "wherever",
    "whether", "which", "while", "whither", "who",
    "who's", "whoever", "whole", "whom", "whose",
    "why", "will", "willing", "wish", "with",
    "within", "without", "won't", "wonder", "would",
    "wouldn't", "yes", "yet", "you", "you'd",
    "you'll", "you're", "you've", "your", "yours",
    "yourself", "yourselves", "zero", "mine", "re", "ll"
}
emoji_pattern = re.compile('[\U0001F300-\U0001F64F\U0001F680-\U0001F6FF\u2600-\u2B55]+')


def split_sentence(sentence):
    sentence = sentence.lower()
    sentence = emoji_pattern.sub(' ', sentence)
    sentence = sentence.replace(",", " ").replace("|", " ").replace("#", " ").\
        replace("@", " ").replace("~", " ").replace("'", " ").replace("\"", " "). \
        replace("\\", " ").replace("/", " ").replace("_", " ").replace("-", " "). \
        replace("[", " ").replace("]", " ").replace("+", " ").replace("*", " "). \
        replace("{", " ").replace("}", " ").replace(";", " ").replace(":", " "). \
        replace("`", " ").replace("=", " ").replace("【", " ").replace("】", " "). \
        replace("(", " ").replace(")", " ").replace(".", " ").replace("’", " "). \
        replace("?", " ")
    words = sentence.split(' ')

    word_set = set()
    for word in words:
        if not word:
            continue

        if len(word) == 1 or len(word) > 30:
            continue

        if word in stop_words:
            continue

        word_set.add(word)
    return word_set


def main():
    with open('result.txt', 'r') as r_file:
        video_kind_map = json.load(r_file)

    video_info_map = {}
    with open('videos1.txt', 'r') as v_file:
        for item in json.load(v_file):
            video_info_map[item['id']] = item
    with open('videos.txt', 'r') as v_file:
        for item in json.load(v_file):
            video_info_map[item['id']] = item

    data_list = []
    for video_id, video_kind in video_kind_map.items():
        if video_id not in video_info_map:
            continue

        video = video_info_map[video_id]
        word_set = split_sentence(video['title'])
        for tag in video.get('tag', []):
            word_set |= split_sentence(tag)

        data_list.append({
            'id': video_id,
            'word': list(word_set),
            'kind': video_kind
        })

    with open('data.txt', 'w') as d_file:
        json.dump(data_list, d_file)

if __name__ == '__main__':
    main()
