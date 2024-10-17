import re
from langchain_core.prompts import ChatPromptTemplate

from components.data import get_novel_data
texts_dic  = get_novel_data()

def func_count_string_all_text(keyword,text):
    text = "".join([texts_dic[k]["content"] for k in texts_dic.keys()])
    # カウント（正規表現）
    count_keyword = len(re.findall(keyword, text))
    context = f"keyword:{keyword}, 出現回数: {count_keyword}回登場"
    return context


make_keyword_human_prompt = """
下記の質問を、出現回数をカウントしたいキーワードをkeywordとして設定してください。
「ええ…」など繰り返し回数を問わない場合は、正規表現を用いてkeywordを「ええ+」としてください。
# 質問: {question}
# キーワード(のみ。括弧は不要): 
"""
make_keyword_prompt = ChatPromptTemplate([
    ("user", make_keyword_human_prompt),
])