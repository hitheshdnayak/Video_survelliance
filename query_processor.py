# import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import tkinter as tk
from tkinter import scrolledtext
import cv2
import numpy as np


class QueryProcessor:
    # def __init__(self):
        # try:
        #     # nltk.download('punkt')
        #     # nltk.download('averaged_perceptron_tagger')
        # except Exception as e:
            # print("An error occurred while downloading NLTK resources:", e)
        

    # Function to tokenize prompts, perform POS tagging, and extract nouns and adjectives
    def process_user_prompt(self, prompt):
        # Tokenize the prompt
        tokens = word_tokenize(prompt)
        
        # Perform POS tagging
        pos_tags = pos_tag(tokens)
        
        # Extract nouns and adjectives
        nouns = [word for word, pos in pos_tags if pos.startswith('NN')]
        adjectives = [word for word, pos in pos_tags if pos.startswith('JJ')]
        
        return nouns, adjectives

    # Function to generate queries based on the identified objects and adjectives
    def generate_queries(self, nouns, adjectives):
        queries = [(noun, adjective) for noun in nouns for adjective in adjectives]
        return queries

    # Function to calculate cosine similarity
    def cosine_similarity(self, noun_list, object_list):
        similarities = {}
        for noun in noun_list:
            max_similarity = 0
            closest_object = ""
            for obj in object_list:
                vectorizer = CountVectorizer().fit_transform([noun, obj])
                cosine_similarity_matrix = cosine_similarity(vectorizer)
                similarity_score = cosine_similarity_matrix[0, 1]
                if similarity_score > max_similarity:
                    max_similarity = similarity_score
                    closest_object = obj
            similarities[noun] = closest_object
        return similarities

def process_and_display(query):
    query_processor = QueryProcessor()
    nouns, adjectives = query_processor.process_user_prompt(query)
    # queries = query_processor.generate_queries(nouns, adjectives)
    closest_objects = query_processor.cosine_similarity(nouns, adjectives)
    for noun, adjective in zip(nouns, adjectives):
        if noun in closest_objects:
            closest_objects[noun] = [adjective]  # Adjust the dictionary to contain a list of adjectives
    return closest_objects

