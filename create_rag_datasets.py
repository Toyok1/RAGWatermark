import json
import os

def walk_directory(directory):
    l = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                l.append(os.path.join(root, file))
    return l

for f in walk_directory("./distribution_same_topic_cyber_words"):
    n_articles = []
    w_article = ""
    with open(f, 'r', encoding='utf-8') as file:
        data = json.load(file)
        n_articles.append(data['original_doc'])
        n_articles.append(data['articles']['gpt4o']['article'])
        n_articles.append(data['articles']['claude3.5sonnet']['article'])
        n_articles.append(data['articles']['llama3.1-405b']['article'])
        n_articles.append(data['articles']['qwen1.5-110b']['article'])
        w_article = data['articles']['watermarked']['article']
    with open("./clean_dataset_cyber_words.txt", 'a', encoding='utf-8') as file:
        for a in n_articles:
            file.write(a.replace("\n", " ") + "\n")
    with open("./watermarked_dataset_cyber_words.txt", 'a', encoding='utf-8') as file:
        '''for a in n_articles:
            file.write(a.replace("\n", " ") + "\n")'''
        file.write(w_article.replace("\n", " ") + "\n")

