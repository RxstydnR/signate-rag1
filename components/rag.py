from langchain_core.prompts import ChatPromptTemplate

# 小説ver
# これらの小説の内容は小説内での記載順にソートされています。
rag_prompt_template = """
あなたはある小説に関する質問応答タスクのためのアシスタントです。

以下の小説の内容を基に質問に回答してください。
答えがわからない場合は、わからないとだけ言ってください。
また、質問が小説の内容に反しているかもと思ったら、質問そのものが小説に矛盾していると回答してください。

回答時は、回答となぜその回答だと思ったのか、また根拠と確信度も合わせて回答してください。
小説の内容は上から下まで隅々まで注視して読んでください。

質問: {question} 
小説の内容: {context} 
あなたの回答:"
"""
# プロンプトテンプレートの設定
rag_prompt = ChatPromptTemplate.from_template(rag_prompt_template)