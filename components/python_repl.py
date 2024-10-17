from langchain_core.prompts import ChatPromptTemplate
from langchain_experimental.tools.python.tool import PythonAstREPLTool

python_tool_description = """
A Python shell. Use this to execute python commands. Input should be a valid python command. 
For example, if you want to see the output of a value, you should print it out with `print(...)`.
Note that the variable name of the novel text is 'novel_text'.
"""

python_prompt_template = """
'python_repl'はpythonを使って与えられた小説の内容をテキスト分析できるツールです。
今回、分析する小説は変数名'novel_text'です。そのため'novel_text'を分析するpythonコードを書く必要があります。
例えば、`novel_text.count('吉田')`などです。

以下の順序で条件を確認し、最初に該当する分析を実行してください：

1. A (最優先): 質問に「ひらがな」「カタカナ」「ローマ字」のいずれかの単語が含まれている場合、または「～のみの単語」という表現がある場合、どんな質問であっても例外なく、小説内から正規表現で「ひらがな」、「カタカナ」、「ローマ字」を抽出するコードのみを書いてください。以下の形式でコードを生成してください：

   import re
   hiragana = re.findall(r'[ぁ-ん]+', novel_text)
   katakana = re.findall(r'[ァ-ン]+', novel_text)
   romaji = re.findall(r'[a-zA-Z]+', novel_text)

2. B (次点): もしAに該当しない場合、かつ「小説内のxxxに該当する単語は何種類ですか」などに類する質問が入力された場合、あなたが思いつく限りの対象を網羅的にたくさん挙げ、それに該当する単語を全て抽出するコードを書いてください。

   import re
   colors = re.findall(r'(?:赤|青|緑|黄|紫|オレンジ|ピンク|白|黒|灰色)', novel_text)
   unique_colors = set(colors)
   print("色の種類:", len(unique_colors))
   print("色:", unique_colors)

3. C (最後の選択肢): その他の分析を行ってください。

# ユーザーの質問:{query}
"""
python_prompt = ChatPromptTemplate.from_template(python_prompt_template)


def create_python_repl_llm(local_val,llm):

    repl_tool = PythonAstREPLTool(
        name = 'python_repl_ast',
        locals={"novel_text":local_val},
        description=python_tool_description,
        verbose = False,
        return_direct=True
    )
    llm_bind = llm.bind_tools([repl_tool],tool_choice="python_repl_ast")
    python_repl_runnable = python_prompt | llm_bind
    return repl_tool,python_repl_runnable

import json
def get_python_repl_executed_results(res,repl_tool):
    tool_query = json.loads(
        res.additional_kwargs["tool_calls"][0]["function"]["arguments"]
    )
    python_code = tool_query["query"]
    return repl_tool.invoke(python_code)