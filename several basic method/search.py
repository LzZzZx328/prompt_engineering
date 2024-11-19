import functools, operator, requests, os, json
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS


def internet_search(query: str):
    with DDGS() as ddgs:
        ddgs_gen = ddgs.text(
            query,
            max_results=5,#限制返回的最大结果数为5个
            region=None,
            safesearch="moderate",
            timelimit="y",# 限制返回的结果为最近一年的内容
            backend="api",
        )
        if ddgs_gen:
            return [r for r in ddgs_gen]
    return "No results found."


def process_content(url: str, threhold: int = 1000) -> list:
    # 这个函数从指定的URL获取网页内容，并将其处理成段落。
    # current_paragraph 负责累积当前段落的内容， candidate 则是当前待处理的段落。
    response = requests.get(url)#获取网页内容
    soup = BeautifulSoup(response.content, 'html.parser')#解析网页内容，并提取文本
    text = soup.get_text()

    #text.split("\n")：将网页文本按照换行符 \n 拆分成多个段落
    #paragraph.strip()：去掉每一段的前后空白
    candidate_paragraphs = (paragraph.strip() for paragraph in text.split("\n"))
    paragraphs = []
    current_paragraph = ""

    for candidate in candidate_paragraphs:
        if len(candidate) > 0:
            if len(current_paragraph) + len(candidate) <= threhold:
                current_paragraph += candidate + " "
            else:
                while len(candidate) > threhold:
                    if len(current_paragraph) > 0:
                        paragraphs.append(current_paragraph.strip() + "\n")
                        current_paragraph = ""
                    paragraphs.append(candidate[:threhold].strip() + "\n")
                    # 将候选段落的前 threhold 个字符添加到 paragraphs 中
                    candidate = candidate[threhold:]#更新候选段落，去掉已经处理的部分
                if len(current_paragraph) + len(candidate) > threhold:
                    paragraphs.append(current_paragraph.strip() + "\n")
                    current_paragraph = candidate + " "
                else:
                    current_paragraph += candidate + " "

    if current_paragraph:#说明还有最后一个段落未被添加
        paragraphs.append(current_paragraph.strip() + "\n")

    return paragraphs
