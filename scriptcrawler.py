# coding=utf-8

import os
import sys
import json
from tqdm import tqdm
import requests
from zhconv import convert
from bs4 import BeautifulSoup

import filter

class ScriptCrawler:
    
    def __init__(self, input_dir):
        self.title_list = ['阳光岁月', '我们好好爱', '鲜族兄弟', 
             '在婚姻的调色板上', '瞪眼等着好事来', '家庭保卫战']
        self.check_path(input_dir)
        
    def check_path(self, input_dir):
        
        check_flag = True
        
        if os.path.isfile(os.path.join(input_dir, 'Urls.json')):
            self.urls_path = os.path.join(input_dir, 'Urls.json')
        else:
            print("Urls.json not found. Please make sure 'Urls.json' in the input directory.")
            check_flag = False
        
        if os.path.isfile(os.path.join(input_dir, 'Label.json')):
            self.label_path = os.path.join(input_dir, 'Label.json')
        else:
            print("Label.json not found. Please make sure 'Label.json' in the input directory.")
            check_flag = False
        
        if not check_flag:
            sys.exit()

    def get_dialogue(self):
        script_urls = self.load_script_url()
        scripts = self.crawl_script_from_url(script_urls)
        sentences = self.filter_script(scripts)
        sentences = self.convert_to_zhtw(sentences)
        mpdd = self.create_dataset(sentences)
        return mpdd
    
    def load_script_url(self):
        print("Load script urls...")
        with open(self.urls_path, 'r', encoding='utf8') as f:
            script_url = json.load(f)
        return script_url

    def get_request(self, url, times):
        times = 0
        while times < 5:
            try:
                req = requests.get(url, stream=True)
                if req != None and req.status_code == requests.codes.ok:
                    return req
            except:
                pass
            times += 1
        sys.exit("Crawled data fail over 5 times!\nPlease check the network connection or try later.")
    
    def crawl_script_from_url(self, script_urls):
        print("Collect script content...")
        scripts = dict([(key, []) for key in self.title_list])
        for title, url_list in script_urls.items():
            print(" -- crawl data from script '{}'".format(title))
            for url in tqdm(url_list):
                s_req = self.get_request(url, 0)
                soup = BeautifulSoup(s_req.content, 'html.parser',from_encoding="GBK")
                s_text = soup.find(id='contain_4').get_text('\n', '<BR>')
                scripts[title].append(s_text)
        return scripts

    def filter_script(self, scripts):
        print("Filter sentences from scripts...")
        sentences = {}
        for t_idx, title in enumerate(scripts):
            sentences[title] = getattr(filter, 'filter_'+str(t_idx))(scripts[title])
        return sentences
        
    def convert_to_zhtw(self, sentences):
        print("Convert sentences to Traditional Chinese...")
        sentences_tw = {}
        for title, sentence_list in sentences.items():
            title_tw = convert(title, 'zh-tw')
            sentences_tw[title_tw] = []
            for speaker, content in sentence_list:
                speaker = convert(speaker, 'zh-tw')
                content = convert(content, 'zh-tw')
                sentences_tw[title_tw].append([speaker, content])
        return sentences_tw

    def create_dataset(self, sentences):
        print("Create MPDD file...")
        
        mpdd = {}
        
        with open(self.label_path, 'r', encoding='utf8') as f:
            label_data = json.load(f)
        
        for title, dialogues in label_data.items():
            mpdd[title] = {}
            sentence_list = sentences[title]
            
            for idx, dialogue in dialogues.items():
                sent_list = []
                for sent in dialogue:
                    selected_sent = sentence_list[sent["sent_id"]]
                    listener_list = [{'name': listener[0], 'relation': listener[1]}
                        for listener in sent["listener"]]
                    sent_list.append({
                                        "speaker": selected_sent[0],
                                        "utterance": selected_sent[1],
                                        "target_listener": listener_list,
                                        "emotion": sent["emotion"]
                                    })
                                        
                mpdd[title][idx] = sent_list

        return mpdd
