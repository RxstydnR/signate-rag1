import re
import unicodedata


def refine_text(text):
    """
    全角文字を半角文字に変換する関数
    
    Args:
    text (str): 変換したい文字列
    
    Returns:
    str: 半角に変換された文字列
    """
    text_ = ''.join([unicodedata.normalize('NFKC', char) for char in text])
    text_ = text_.replace("回答:","").replace(" ","")
    return text_


def remove_parts(text):
    # 不要な箇所を削除
    text = text.split("底本：")[0]
    text = text.split("-------------------------------------------------------")[-1]
    return text


def replace_symbols(text):
    
    # 置換処理
    text = text.replace("｜", "")
    text = re.sub(r"※［＃.*?］", r"", text)
    text = re.sub(r"［＃.*?］", r"", text)
    text = re.sub(r"《.*?》", r"", text)
    # text = re.sub(r"(..)／＼", r"\1\1", text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()