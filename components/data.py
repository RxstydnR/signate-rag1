import os
import re
import glob
import pickle
from components.preprocess import remove_parts
from langchain_core.documents import Document
from langchain_text_splitters import CharacterTextSplitter

def extract_and_replace_headings(text):
    # 中見出しを抽出して置換する
    pattern = r'(.*?)［＃「(.*?)」は中見出し］'
    replaced_text = re.sub(pattern, r'<章：\2>', text)
    
    # 漢数字のリスト
    kanji_numbers = "一二三四五六七八九十"
    
    # 行ごとに処理
    lines = replaced_text.split('\n')
    processed_lines = []
    
    for line in lines:
        # パターン1: 行が漢数字のみの場合
        pattern1 = f'^([{kanji_numbers}]+)$'
        # パターン2: 行が（漢数字）の場合
        pattern2 = f'^（([{kanji_numbers}]+)）$'
        
        match1 = re.match(pattern1, line.strip())
        match2 = re.match(pattern2, line.strip())
        
        if match1:
            processed_line = f'<章：{match1.group(1)}>'
        elif match2:
            processed_line = f'<章：{match2.group(1)}>'
        else:
            processed_line = line
        
        processed_lines.append(processed_line)
    
    return '\n'.join(processed_lines)

def replace_symbols(text):
    # 置換処理
    text = text.replace("｜", "")
    text = re.sub(r"※［＃.*?］", r"", text)
    text = re.sub(r"［＃.*?］", r"", text)
    text = re.sub(r"《.*?》", r"", text)
    # text = re.sub(r"(..)／＼", r"\1\1", text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def process_text(text):
    # 中見出しの抽出と置換を行う
    text = extract_and_replace_headings(text)
    # その他のシンボルの置換を行う
    text = replace_symbols(text)
    return text

def extract_chapter_titles(text):
    """
    テキストから <章：...> 形式の章タイトルを抽出する関数
    
    :param text: 入力テキスト
    :return: 抽出された章タイトルのリスト
    """
    pattern = r'<章：([^>]+)>'
    titles = re.findall(pattern, text)
    return titles

def process_chapter(text):
    """
    テキストを処理し、章タイトルを抽出して結果を表示する関数
    
    :param text: 入力テキスト
    """
    titles = extract_chapter_titles(text)
    if titles:
        assert len(titles)==1,"複数の見出しが見つかっています。"
        return titles[0]
    else:
        # print("章タイトルが見つかりませんでした。")
        return None

def get_novel_data():
    files = sorted(glob.glob("../data/novels/utf-8/*.txt"))
    texts_dic = {}
    for file in files:
        texts = []
        with open(file, 'r') as f:
            
            title = next(f).strip()
            author = next(f).strip()
            
            while True:
                try:
                    line = next(f)
                    if "中見出し" in line:
                        line = "/////"+line # 章区切り
                    texts.append(line)
                except:
                    break

            texts_dic[os.path.basename(file)] = {
                "title":title,
                "author":author,
                "content": "".join(texts)
            }
    
    for k in texts_dic.keys():
        title = texts_dic[k]["title"]
        text = texts_dic[k]["content"]
        text = remove_parts(text)
        
        if k in ["1.txt"]:
            texts = text.split("　　　　　　　　　")[1:]
        elif k in ["3.txt","4.txt"]:
            texts = text.split("　　　　　")[1:]
        elif k in ["2.txt","6.txt","7.txt"]:
            texts = text.split("/////")[1:]
        elif k in ["5.txt"]:
            texts = [text]
        else:
            raise NotImplementedError
        
        texts[0] = f"題名: {title}\n"+texts[0]
        texts = [process_text(text) for text in texts]
        texts_dic[k]["texts"] = texts
    
    return texts_dic

def get_novel_docs(texts_dic,chunk_size = 512, chunk_overlap = 128):
    documents_dic = {}
    for k,v in texts_dic.items():

        # print(f"\n{k}")
        
        title,author = texts_dic[k]["title"],texts_dic[k]["author"]
        chunks = texts_dic[k]["texts"]

        # splitter = RecursiveCharacterTextSplitter(separators=["。"],chunk_size=chunk_size,chunk_overlap=chunk_overlap,length_function=len)
        splitter = CharacterTextSplitter(separator="。",chunk_size=chunk_size,chunk_overlap=chunk_overlap)
        
        count=0
        docs=[]
        for chunk in chunks:
            chapter = process_chapter(chunk)
            if chapter:
                chapter_add = f"[章：{chapter}] "
            else:
                chapter_add = ""
                
            texts = splitter.split_text(chunk)

            for text in texts:
                text = chapter_add + text
            
                doc = Document(
                    page_content = text,
                    metadata = {"title":title, "author":author, "chapter":chapter,"position":str(count).zfill(4)}
                )
                docs.append(doc)
                count+=1

        # final_texts = [doc.page_content for doc in docs]
        documents_dic[k] = docs
    return documents_dic

def get_novel_summary():
    # 小説のサマリー
    with open('novel_summary.pkl', 'rb') as f:
        novels_dic = pickle.load(f)
    return novels_dic