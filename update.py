import os
import sys
import time
import yaml

default_content = """
### To be continued...... <!-- {docsify-ignore-all} -->

- 欢迎分享！
- 欢迎分享！
- 欢迎分享！
"""


def get_markdown_url(text: str, url: str, count: int = None):
    if count:
        if url:
            return f"[{text}({count})]({url})"
        return f"{text}({count})"
    else:
        if url:
            return f"[{text}]({url})"
        return f"{text}"


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
    pass


def update_recent_posts(data):
    pass


if __name__ == "__main__":
    posts = yaml.load(open("posts.yaml", encoding="utf-8"), Loader=yaml.FullLoader)
    print(posts)

    generate_sidebar(posts)
    generate_readme(posts)
    update_recent_posts(posts)
