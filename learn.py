import re
import argparse
from cgitb import text
from typing import List
import MeCab
import markovify

def normalization(texts:List[str]) -> List[str]:
    normalized_texts = list(str())
    
    for text in texts:
        normalized_texts.append(re.sub('\'|\"|\(|\)|\[|\]|\r|<br />|\u3000|-|\||https?://[\w!\?/\+\-_~=;\.,\*&@#\$%\(\)\'\[\]]+|@[\\w]{1,15}',' ',text))

    return normalized_texts

def parse_texts(normalized_texts:str) -> str:
    mecab = MeCab.Tagger('-Owakati')
    parsed_texts = str()


    for text in normalized_texts:
        parsed = mecab.parse(text)
        for token in parsed:
            if token == '\n':
                continue
            parsed_texts += token
            if token == '。':
                parsed_texts += '\n' 

    return parsed_texts

def learn_markov(parsed_text:str)->None:
    model = markovify.NewlineText(parsed_text,state_size=5)
    with open('model_data.json', 'w') as f:
        f.write(model.to_json())

def main(dataset_path:str)-> None:
    texts = open(dataset_path,'r').readlines()
    parsed_text = parse_texts(normalization(texts))
    learn_markov(parsed_text)

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--dataset_path', type=str, required=True)
    main(**vars(parser.parse_args()))