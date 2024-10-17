import unicodedata
from langchain_core.prompts import ChatPromptTemplate

from components.preprocess import remove_parts,replace_symbols,refine_text
from components.data import get_novel_data,get_novel_summary
texts_dic  = get_novel_data()
novels_dic = get_novel_summary()


def get_novel_info(index,len_example=1000):
    assert index>0
    novel_key = f"{index}.txt"
    title  = texts_dic[novel_key]["title"]
    author = texts_dic[novel_key]["author"]

    example_text = texts_dic[novel_key]["content"]
    example_text = remove_parts(example_text)
    example_text = replace_symbols(example_text)
    example_text = example_text[:len_example]

    summary = novels_dic[novel_key]["summary"]

    return title,author,summary,example_text


hyde_prompt_template = """
あなたは小説を分析・理解することに特化したAIアシスタントです。
与えられた質問に基づいて、その小説の一部となりうる仮想的な文章を生成することが今回のタスクです。
この文章は、小説から関連情報を検索するクエリとして使用されます。

# 入力情報
- 小説のタイトル：{title}
- 著者：{author}
- 小説の要約：{summary}
- 小説の冒頭：{example}
- ユーザーの質問：{question}

# 指示
与えられた小説の文体、トーン、テーマを考慮し、以下の要素を含む短い文章（1段落）を作成してください。
- 与えられた質問やトピックに関連する内容
- 著者の文体を模倣した表現
- 実際の小説で使用されそうなキーワードやフレーズ

# 出力
小説の一部（2〜3段落程度）：
"""

hyde_prompt = ChatPromptTemplate.from_template(hyde_prompt_template)