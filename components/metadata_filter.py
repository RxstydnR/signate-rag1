from langchain_core.prompts import ChatPromptTemplate

# Prompt
entity_filter_prompt_template = """あなたはユーザーの質問にする回答に必要な情報収集を選択するエキスパートです。
情報収集の際に、Metadataでフィルタリングする必要があるかを判定し、もし必要ならフィルタリングするエンティティを以下から選択してください。

# エンティティの種類
- PERSON: 人名
- GEONAME: 土地名、地理的名称
- COUNTRY: 国名
- PRODUCT: 製品、アイテム
- ANIMAL: 動物

# 出力形式(以下の有効なJson形式で回答)
{{
"use_filter":"" \\Given a user question, choose to use metadata filter or not. Ouput must be bool.
"entity_filter":""　\\Given a user question, if use filter, choose necessary entities to be used for metadata filtering.
}}

# 例：
- 質問：吉田が病院の食堂で出会った付添婦が勧めた薬の材料は何ですか？
{{
"use_filter":"False"
"entity_filter":"None"
}}

- 質問：吉田が付添婦と出会った場所はどこですか？
{{
"use_filter":"False"
"entity_filter":"None"
}}

- 質問：吉田が肺病患者だということを見破って近付いて来た人は全員で何人でしたか。
{{
"use_filter":"True"
"entity_filter":"PERSON"
}}

- 質問：首縊りの縄が高く売れた場所と購入者を全て挙げよ。
{{
"use_filter":"True"
"entity_filter":"PERSON","GEONAME"
}}

<notice>
ユーザーの質問が「〜に該当するものを全て列挙せよ」という複数個の情報を収集する必要のある問題である場合のみにuse_filterはTrueになります。
</notice>

# ユーザーの質問
- 質問：{question}
- あなたの回答：
"""

entity_filter_prompt = ChatPromptTemplate.from_template(entity_filter_prompt_template)


def has_common_element(list_a, list_b):
    return any(set(list_a).intersection(list_b))

def entiry_filter(docs, filters=[]):
    assert isinstance(filters,list),"filters is not list."
    docs_=[]
    for doc in docs:
        if has_common_element(filters,doc.metadata["entity"]):
            docs_.append(doc)
    return docs_