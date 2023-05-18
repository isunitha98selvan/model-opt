"""
Implementation of BPE algorithm
"""
import re

from collections import defaultdict


def get_base_vocab(word_freq):
    vocab = set()
    for key, val in word_freq.items():
        tokens = [t for t in key]
        for t in tokens:
            vocab.add(t)

    vocab.add("<|endoftext|>") # add special token
    return vocab


def compute_pair_freq(word_freq, splits):
    pair_freq = defaultdict(int)
    for word, freq in word_freq.items():
        split = splits[word]
        for i in range(1, len(split)):
            pair_freq[(split[i-1], split[i])] += freq

    return pair_freq


def count_word_freq(corpus):
    word_freq = defaultdict(int)
    for sent in corpus:
        sent = re.sub(r'[^\w\s]', '', sent)
        words = sent.split(" ")
        for word in words:
            word_freq[word.lower()] += 1
    return word_freq


def merge(a, b, splits):
    for word, split in splits.items():
        if a in split and b in split:
            i = split.index(a)
            if i+1<len(word) and split[i+1] == b:
                splits[word] = split[:i] + [a+b] + split[i+2:]
    return splits


def build_vocab(base_vocab, word_freq, splits):
    vocab_size = 50
    vocab = [base_vocab]
    while len(vocab) < vocab_size:
        pair_freq = compute_pair_freq(word_freq, splits)
        pair_freq = sorted(pair_freq.items(), key=lambda item: item[1], reverse=True)
        if len(pair_freq) > 0:
            word = pair_freq[0][0]  # get the best pair
            a = word[0]
            b = word[1]
            splits = merge(a, b, splits)    # merge a and b and recompute the splits
            vocab.append(a + b)
        else:
            break

    return vocab


def main():
    corpus = [
        "This is the byte pair encoding algorithm.",
        "course",
        "this",
        "this is test text"
    ]

    word_freq = count_word_freq(corpus)
    print("word freq: ", word_freq)
    vocab = get_base_vocab(word_freq)
    print("base vocab: ", vocab)
    splits = {word: [c for c in word] for word, freq in word_freq.items()}
    vocab = build_vocab(vocab, word_freq, splits)
    print("vocab: ", vocab)


if __name__ == '__main__':
    main()
