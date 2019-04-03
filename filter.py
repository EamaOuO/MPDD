# coding=utf-8

import re
import json

def filter_0(scripts):
    acter_list = ['连国', '连军', '连辉', '张华', '天天', '小蒙', '小雨', '三条', '马全', '明等', '学清', '天强', '周林', '队长', '赵斌', '大友', '向大爷', '向永', '苗苗', '猴子', '小胡', '小四', '小雨', '医生', '大爷', '强哥', '华哥', '妈妈', '老六', '警察', '同事', '大伟', '小吴', '大头', '何扬', '张超', '辉哥', '小慧', '赵编', '陈明', '老大', '小混混', '于海', '女职工', '儿子', '大嫂', '老板', '服务员', '四人', '老婆', '大成', '辉', '学清', '赵', '婆婆', '小兰', '亮子', '大姐', '王', '懂事长', '董事长', '刘主任', '小刘', '雪', '军', '杨雪', '斌']
    acter_dict = {'军':'连军', '雪':'杨雪', '赵':'赵斌', '斌':'赵斌', '王':'学清', '辉':'连辉', '辉哥':'连辉', '懂事长':'董事长'}

    sentence_list = []
    for script in scripts:
        for turn in re.split(r'\n', script):
            person, sent = '', ''
            if '：' in turn:
                turn = re.sub(r'\xa0| ', '', turn)
                turn = re.sub(r'（[^（）]+）', '', turn)
                person, sent = turn.split('：', 1)
                if person not in acter_list:
                    person = keyword_check(person, acter_list)
                if person in acter_dict:
                    person = acter_dict[person]
            if person != '':
                sentence_list.append([person, sent])
    return sentence_list

def filter_1(scripts):
    exclusion =  ['△', '】', '淡入', '字幕', '合唱', '（', '）', '编剧', '笔名', '联系', '场']
    
    sentence_list = []
    for script in scripts:
        act = re.split(r'[0-9]+：', script)[1:]
        for a in act:
            for turn in re.split(r'\n', a):
                person = ''
                turn = re.sub(r'(\u3000)|\xa0| ', '', turn)
                turn = re.sub(r'\(', '（', turn)
                turn = re.sub(r'\)', '）', turn)
                state = ' '.join([s[1:-1] for s in re.findall(r'（[^（）]+）', turn)])
                turn = re.sub(r'（[^（）]+）', '', turn)
                if '：' in turn:
                    person, sent = turn.split('：', 1)
                    if keyword_check(person, exclusion) == '' and sent != '':
                        if keyword_check(state, ['自语', '心声']) == '':
                            sentence_list.append([person, sent])
    return sentence_list

def filter_2(scripts):
    acter_dict = dict([('华', '晓华'), ('秋', '陈小秋'), ('小秋', '陈小秋'), ('波', '韩长波'), 
             ('长波', '韩长波'), ('鸽', '白鸽'), ('军', '马军'), ('生', '医生'), 
             ('员', '警员'), ('雪', '小雪'), ('东', '韩东'), ('林', '韩长林'), 
             ('长林', '韩长林'), ('丽', '徐丽'), ('常', '小常'), ('玉', '美玉'),
             ('子', '母亲'), ('黄凤山', '苗凤山'), ('警察', '警员'), ('一学生', '学生'),
             ('客人问', '客人'), ('客人喊', '客人')])
    exclusion = ['下联', '人物', '[人物', '字幕', '上联', '横批', '[特写', '我先说']
    
    sentence_list = []
    for script in scripts:
        act = re.split(r'[0-9]+、', script)[1:]
        for a in act:
            for turn in re.split(r'\n', a):
                person = ''
                turn = re.sub(r'(\u3000)|\xa0| ', '', turn)
                if '：' in turn:
                    person, sent = turn.split('：', 1)
                    if sent != '' and sent[0] == '“' and sent[-1] == '”':
                        sent = sent[1:-1]
                    
                    if len(person) < 1 or len(person) > 3 or sent == '':
                        person = ''
                    elif keyword_check(person, exclusion) != '':
                        person = ''
                    elif sent == '（朝语，字幕）':
                        person = ''
                if person != '':
                    sentence_list.append([person, sent])
    return sentence_list

def filter_3(scripts):
    exclusion =  ['△', '【', '】', '淡入', '字幕', '合唱', '（', '）',
                  '编剧', '笔名', '联系', '场', '镜头特写', '画外音']
    sentence_list = []       
    for script in scripts:
        act = re.split(r'[0-9]+、', script)[1:]
        for a in act:
            for turn in re.split(r'\n', a):
                person = ''
                turn = re.sub(r'(\u3000)|\xa0| ', '', turn)
                turn = re.sub(r'\(', '（', turn)
                turn = re.sub(r'\)', '）', turn)
                state = ' '.join([s[1:-1] for s in re.findall(r'（[^（）]+）', turn)])
                turn = re.sub(r'（[^（）]+）', '', turn)
                if '：' in turn:
                    person, sent = turn.split('：', 1)
                    if keyword_check(person, exclusion) == '' and sent != '':
                        if (len(person) > 1 and len(person) <4):
                            if keyword_check(state, ['自语', '心声']) == '':
                                sentence_list.append([person, sent])
    return sentence_list

def filter_4(scripts):
    
    acter_list = ['徐春友', '郭章建', '王厚宝', '尚洁', '冬晓丽', '张萌', '刘副院长', '刘院长', '刘远灵', '陈玲', '查才金', '张院长', '吴书记', '赵处长', '服务员', '刘钟', '李文莱', '陈铃', '施威', '小赵', '杨导演', '张主编']
    acter_dict = {'刘院长': '刘副院长', '陈铃': '陈玲'}
    
    sentence_list = []
    for script in scripts:
        act = re.split(r'[0-9]+.', script)[1:]
        for a in act:
            for turn in re.split(r'\n', a):
                person, sent = '', ''
                turn = re.sub(r'(\u3000)|\xa0| ', '', turn)
                turn = re.sub(r'\(', '（', turn)
                turn = re.sub(r'\)', '）', turn)
                turn = re.sub(r'（[^（）]+）', '', turn)
                if '：' in turn:
                    person, sent = turn.split('：', 1)
                    if sent != '' and sent[0] == '“' and sent[-1] == '”':
                        sent = sent[1:-1]
                    if person not in acter_list:
                        person = keyword_check(person, acter_list)
                    if person in acter_dict:
                        person = acter_dict[person]
                    if person != '':
                        sentence_list.append([person, sent])
    return sentence_list

def filter_5(scripts):
    sentence_list = []
    for script in scripts:
        for turn in re.split(r'\n', script):
            person = ''
            turn = re.sub(r'(\u3000)|\xa0| ', '', turn)
            turn = re.sub(r'。+', '。', turn)
            if '：' in turn:
                person, sent = turn.split('：', 1)
                sentence_list.append([person, sent])
    return sentence_list

def keyword_check(str, keyword):
    result = ''
    min_idx = len(str)
    for key in keyword:
        try:
            idx = str.index(key)
            if idx < min_idx:
                result = key
                min_idx = idx
        except:
            pass
    return result
