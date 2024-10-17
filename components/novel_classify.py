import numpy as np
from collections import Counter
from langchain_core.prompts import ChatPromptTemplate

from components.data import get_novel_data
texts_dic  = get_novel_data()

novel_titles = ['流行暗殺節', '不如帰', 'カインの末裔', '競漕', '芽生', 'サーカスの怪人', '死生に関するいくつかの断想']

novel_find_keyword_prompt_template = '''
下記はとある文学作品についての質問です。
この質問文から文学作品の本文に含まれる可能性が高いキーワードを抽出してください。

# 質問: {query}

結果は以下のJSON形式で出力してください。
# JSON FORMAT
{{"keyword":""}}

<notice>
- 複数のキーワードがあればカンマ(,)で区切ってください。
- キーワードの前後の空白やタブや改行は不要です。
- 質問文を構成するためだけに使われ、文学作品自体に含まれる可能性が低いキーワードは不要です。除外してください。
  (例)質問が「．．．の回数は？」なら「回数」は不要
  (例)質問が「．．．の理由は？」なら「理由」は不要
- 固有名詞があればそれだけを残して他のキーワードは全て除外してください。
  固有名詞とは、人名、地名、動植物の名前、物の名前、建物の名前、行事名などです。
</notice>
'''
novel_find_keyword_prompt = ChatPromptTemplate.from_template(novel_find_keyword_prompt_template)

# キーワードが含まれている文章を抽出
def pred_title_by_counts(answer):
    
    counts=[]
    for k in texts_dic.keys():
        title = texts_dic[k]["title"]
        text = texts_dic[k]["content"]
        text = title + " " + text
        n_all = 0
        keywords = answer["keyword"].split(",")
        for keyword in keywords:
            n_all += text.count(keyword)
        counts.append(n_all)
    pred_title = novel_titles[np.argmax(counts)]
    
    return pred_title


def find_most_common(docs):

    titles = [doc.metadata["title"] for doc in docs]

    count = Counter(titles)
    most_common = count.most_common(1)
    title = most_common[0][0]

    title = title.replace("小説\u3000","")
    assert title in novel_titles
    
    # 同点のものはどちらかしか返らないことに注意
    return title

def match_title(query):
    for title in novel_titles:
        if title in query:
            return title
    return "該当なし"

# 多数決を行う関数
def majority_vote(lst):
    return max(set(lst), key=lst.count)