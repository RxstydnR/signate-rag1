from langchain_core.prompts import ChatPromptTemplate
from components.data import get_novel_data,get_novel_summary
texts_dic  = get_novel_data()
novels_dic = get_novel_summary()


summary_answer_prompt_template = """
あなたは、ある文学作品に関するユーザーの質問に対して、回答するアシスタントです。
与えられたユーザーの質問に対して、文学作品のサマリを基に回答できる場合は回答してください。

# 入力情報
- 小説のタイトル：{title}
- 小説の要約：{summary}
- ユーザーの質問：{question}

<note>
- 厳密な回答が要約文内に含まれていない場合は、「回答不可」と言ってください。
例えば、直接的な理由や目的を回答できていない場合です。
- 質問：平家物語で平清盛が権力を確立できた主な理由は何ですか？
- 正解：後白河法皇との政治的同盟と、軍事力の強化
- 不正解：清盛の個人的な才能と野心（これは直接的な理由になっていない）
</note>

# 以下のJson形式で回答
{{
"answer":""  \\適切な回答を作成する（ユーザーの質問に対するシンプルな回答 、もしくは「回答不可」という単語のみ）
"reason":""　\\なぜそれが正確な回答かの根拠を述べる
}}

# 出力
あなたの回答：
"""

summary_answer_prompt = ChatPromptTemplate.from_template(summary_answer_prompt_template)