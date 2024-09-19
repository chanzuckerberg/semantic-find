# Given a text file, we want to generate a useful set of ngrams to embed into the
# database.

import nltk
from nltk.tokenize import sent_tokenize
from typing import Optional

class NGramIterator:
    """
    Creates various scales of n-gram (sentences and clusters of n adjacent sentences) from a list of paragraphs.
    For example, given the following paragraphs:

    [
        "p1s1. p1s2. p1s3.",
        "p2s1. p2s2. p2s3.",
    ]

    The iterator will yield the following n-grams (note that it exhausts each single sentence in a paragraph, then
    loops back through the paragraph to create clusters before moving to the next paragraph):

    - p1s1.
    - p1s2.
    - p1s3.
    - p1s1. p1s2. # This is a cluster of sentence 1 and 2
    - p1s2. p1s3. # This is a cluster of sentence 2 and 3
    - p2s1. # This is the next paragraph, we've exhausted the first paragraph's sentences and clusters
    - p2s2.
    - p2s3.
    - p2s1. p2s2.
    - p2s2. p2s3.

    NOTE: The return type has been changed to a tuple of (fragment, paragraph index) so you know where the fragment
    came from.

    This can be used to create embeddable text fragments at multiple scales of context and detail for use in a
    database.

    TODO: Make `n` a list where 1==sentence iterator, 2==cluster of 2 sentences, rather than hardcoding
    """

    class Scale:
        SENTENCE = 0
        CLUSTER = 1

    def __init__(self, paragraphs: list[str]):
        self.paragraphs = paragraphs

        nltk.download('punkt', quiet=True)
        
        self.paragraph_index = 0
        self.item_index = 0
        self.scale = NGramIterator.Scale.SENTENCE
        self.working_sentences: Optional[list[str]] = None
        self.n = 2

    def __iter__(self):
        return self

    def __next__(self):
        if self.paragraph_index >= len(self.paragraphs):
            raise StopIteration

        # print(f"Paragraph index: {self.paragraph_index}, item index: {self.item_index}, scale: {self.scale}")
        
        if self.working_sentences is None:
            paragraph = self.paragraphs[self.paragraph_index]
            self.working_sentences = sent_tokenize(paragraph)

        if self.scale == NGramIterator.Scale.SENTENCE:
            ret = self.working_sentences[self.item_index]
            self.item_index += 1
            # After we've gone through all the sentences in the paragraph, we reset
            # the item index and move through the clusters
            if self.item_index >= len(self.working_sentences):
                self.item_index = 0
                self.scale = NGramIterator.Scale.CLUSTER
            return (ret, self.paragraph_index)
        elif self.scale == NGramIterator.Scale.CLUSTER:
            if self.item_index + self.n > len(self.working_sentences):
                self.paragraph_index += 1
                self.item_index = 0
                self.working_sentences = None
                self.scale = NGramIterator.Scale.SENTENCE
                return self.__next__()
            
            ret = ' '.join(s.strip(" \t\n") for s in self.working_sentences[self.item_index:self.item_index+self.n])
            self.item_index += 1
            return (ret, self.paragraph_index)

if __name__ == "__main__":
    print("DEMO: NGramIterator")

    paragraphs = [
        "p1 s1. p1 s2. p1 s3.",
        "p2 s1. p2 s2. p2 s3.",
    ]

    print("Creating n-grams from the following corpus:")
    print("\n\n".join(paragraphs))

    print("Generated n-grams:")

    ngram_iterator = NGramIterator(paragraphs)
    for ngram in ngram_iterator:
        print(f"- {ngram}")