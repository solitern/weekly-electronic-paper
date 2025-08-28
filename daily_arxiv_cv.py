import arxiv
import openai
import datetime
from src.config import *


# 初始化OpenAI客户端
client = openai.OpenAI(base_url=BASE_URL, api_key=API_KEY)


# 函数：调用LLM API
def call_llm(prompt):
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"LLM API error: {str(e)}")


# 函数：获取最近days天的论文
def get_recent_cv_papers(days=2):
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=days)
    end_date = today

    client = arxiv.Client()
    search = arxiv.Search(
        query="cat:cs.CV OR cat:cs.LG OR cat:cs.AI",
        max_results=100,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending
    )

    papers = []
    for result in client.results(search):
        published_date = result.published.date()
        if start_date <= published_date < end_date:
            papers.append({
                "title": result.title,
                "abstract": result.summary,
                "pdf_url": result.pdf_url,
                "authors": ", ".join(author.name for author in result.authors),
                "published": result.published.strftime("%Y-%m-%d")
            })
        else:
            break
    return papers


# 函数：打分
def score_paper(title, abstract):
    prompt = f"""
    你是计算机视觉领域的专家。评估这篇论文的重要性（针对研究生学习）。
    标题: {title}
    摘要: {abstract}
    输出格式: 只输出一个数字分数 (0-10)，10分表示极重要（如创新方法、热门主题），0分表示无关。
    评估标准：
    - 10分：论文提出创新方法或研究热门主题，对研究生学习有极大的重要性。
    - 8 - 9分：论文研究具有较高价值，方法较新颖，对相关领域学习有重要指导意义。
    - 6 - 7分：论文研究有一定价值，能为研究生学习提供一定的参考和启示。
    - 3 - 5分：论文研究价值一般，与研究生学习有一定相关性，但重要性有限。
    - 1 - 2分：论文与研究生学习的相关性很低，对学习帮助不大。
    - 0分：论文与计算机视觉领域及研究生学习无关。
    """
    try:
        score_str = call_llm(prompt).strip()
        return float(score_str) if score_str.isdigit() else 0.0
    except:
        return 0.0


# 函数：分析
def analyze_paper(title, abstract, pdf_url, authors, published):
    prompt = f"""
    你是计算机视觉领域的专家。为研究生总结这篇论文。
    标题: {title}
    摘要: {abstract}
    PDF: {pdf_url}
    输出Markdown格式(不要以代码块形式输出):
    **作者:** {authors}
    **发布日期:** {published}
    **摘要:** 简短摘要
    **关键点:** 3-5个 bullet points 的创新点、方法、结果
    **为什么重要:** 1-2句解释对CV领域的意义
    **建议:** 是否值得深入阅读，为什么
    """
    return call_llm(prompt)


# 主逻辑
def main(top_n=5):
    papers = get_recent_cv_papers(days=2)
    if not papers:
        print("No new papers today.")
        return

    scored_papers = []
    for paper in papers:
        score = score_paper(paper["title"], paper["abstract"])
        scored_papers.append((score, paper))

    scored_papers.sort(reverse=True, key=lambda x: x[0])
    top_papers = scored_papers[:top_n]

    md_content = "# Daily Computer Vision Papers\n\n"
    for score, paper in top_papers:
        md_content += f"### [{paper['title']}]({paper['pdf_url']})\n**Score:** {score}/10\n"
        analysis = analyze_paper(paper["title"], paper["abstract"], paper["pdf_url"], paper["authors"],
                                 paper["published"])
        md_content += analysis + "\n\n---\n"

    md_file_path = "daily_cv_papers.md"
    with open(md_file_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Generated Markdown file with {len(top_papers)} papers.")

    # 发送邮件
    # send_email(md_file_path)


if __name__ == "__main__":
    main()