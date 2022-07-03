import os
import sys
import time
import yaml
import re

DEFAULT_CONTENT = """
### To be continued...... <!-- {docsify-ignore-all} -->

- 欢迎分享！
- 欢迎分享！
- 欢迎分享！
"""

START_COMMENT = "<!-- recent-update-start -->"
END_COMMENT = "<!-- recent-update-end -->"


def get_markdown_url(text: str, url: str, count: int = None, date=None, tag=None):
    dt = "" if date is None else f"[{date}]"
    tg = "" if tag is None else f"[{tag}]"
    ct = "" if count is None or count == 0 else f"({count})"
    if url:
        return f"{dt}{tg}[{text}{ct}]({url})"
    return f"{dt}{tg}{text}{ct}"


def generate_new_readme(start_comment: str, end_comment: str, content: str, readme: str) -> str:
    """Generate a new Readme.md"""
    pattern = f"{start_comment}[\\s\\S]+{end_comment}"
    repl = f"{start_comment}\n{content}\n{end_comment}"
    if re.search(pattern, readme) is None:
        print(f"can not find section in your readme, please check it, it should be {start_comment} and {end_comment}")

    return re.sub(pattern, repl, readme)


def generate_sidebar(data):

    sidebar_path = os.path.join(os.path.dirname(__file__), "docs", "_sidebar.md")
    sidebar_f = open(sidebar_path, "w", encoding="utf-8")

    for topic_item in data:
        new_content = ""
        topic_title = topic_item["title"]
        topic_url = topic_item["url"]
        topic_count = 0 if topic_item.get("count") is not None and topic_item.get("count") else None

        if topic_item.get("links"):
            for subtopic_item in topic_item.get("links"):
                subtopic_title = subtopic_item["title"]
                subtopic_url = subtopic_item["url"]
                subtopic_count = 0 if subtopic_item.get("count") is not None and subtopic_item.get("count") else None

                if subtopic_item.get("links"):
                    for subsubtopic_item in subtopic_item.get("links"):
                        subsubtopic_title = subsubtopic_item["title"]
                        subsubtopic_url = subsubtopic_item["url"]
                        if subtopic_count is not None:
                            subtopic_count += 1

                new_content += f"  - {get_markdown_url(subtopic_title, subtopic_url, subtopic_count)}\n"
                # print(subtopic_title, subtopic_url, subtopic_count)

                if topic_count is not None and subtopic_count is not None:
                    topic_count += subtopic_count

        new_content = f"- {get_markdown_url(topic_title, topic_url, topic_count)}\n" + new_content

        sidebar_f.write(f"{new_content}\n")


def generate_readme(data):
    total_item = []
    for topic_item in data:
        if topic_item.get("links"):
            for subtopic_item in topic_item.get("links"):
                subtopic_title = subtopic_item["title"]
                subtopic_url = subtopic_item["url"]

                if not subtopic_url.endswith("README.md"):
                    continue

                with open(os.path.join("docs", subtopic_url), "r", encoding="utf-8") as f:
                    subtopic_content = f.read()

                new_content = ""
                topic_list = {"none": []}

                if subtopic_item.get("links"):
                    for subsubtopic_item in subtopic_item.get("links"):
                        subsubtopic_title = subsubtopic_item["title"]
                        subsubtopic_url = subsubtopic_item["url"]
                        subsubtopic_date = subsubtopic_item.get("date", "")
                        subsubtopic_tag = subsubtopic_item.get("tag", "none")

                        if subsubtopic_tag not in topic_list:
                            topic_list[subsubtopic_tag] = []

                        _item = {
                            "title": subsubtopic_title,
                            "url": subsubtopic_url,
                            "date": subsubtopic_date,
                            "tag": subsubtopic_tag,
                        }
                        topic_list[subsubtopic_tag].append(_item)
                        total_item.append(_item)

                for tag in topic_list:
                    if tag == "none" or len(topic_list[tag]) == 0:
                        continue
                    new_content += f"### {tag}\n"
                    for topic_item in topic_list[tag]:
                        new_content += f'- {get_markdown_url(topic_item["title"], topic_item["url"])}\n'
                    new_content += "\n"

                if new_content and len(new_content.strip()) > 0:
                    _new_content = generate_new_readme(START_COMMENT, END_COMMENT, new_content, subtopic_content)
                else:
                    _new_content = generate_new_readme(START_COMMENT, END_COMMENT, DEFAULT_CONTENT, subtopic_content)
                with open(os.path.join("docs", subtopic_url), "w", encoding="utf-8") as f:
                    f.write(_new_content)


if __name__ == "__main__":
    posts = yaml.load(open("posts.yaml", encoding="utf-8"), Loader=yaml.FullLoader)
    print(posts)

    generate_sidebar(posts)
    generate_readme(posts)
