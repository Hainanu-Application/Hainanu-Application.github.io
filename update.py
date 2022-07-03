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


def generate_sidebar(data):

    sidebar_path = os.path.join(os.path.dirname(__file__), "docs", "_sidebar.md")
    sidebar_f = open(sidebar_path, "w")

    for topic_item in data:
        new_content = ""
        topic_title = topic_item["title"]
        topic_url = topic_item["url"]
        topic_count = 0 if topic_item["count"] else None

        for subtopic_item in topic_item["links"]:
            subtopic_title = subtopic_item["title"]
            subtopic_url = subtopic_item["url"]
            subtopic_count = 0 if subtopic_item["count"] else None

            for subsubtopic_item in subtopic_item["links"]:
                subsubtopic_title = subsubtopic_item["title"]
                subsubtopic_url = subsubtopic_item["url"]
                if subtopic_count is not None:
                    subtopic_count += 1

            if subtopic_count:
                new_content += f" - [{subtopic_title}({subtopic_count})]({subtopic_url})\n"
            else:
                new_content += f" - [{subtopic_title}]({subtopic_url})\n"

            if topic_count is not None and subtopic_count is not None:
                topic_count += subtopic_count

        if topic_count:
            new_content += f"- [{topic_title}({topic_count})]({topic_url})\n"
        else:
            new_content += f"- [{topic_title}]({topic_url})\n"

        sidebar_f.write(f"{new_content}\n")


def generate_readme():
    pass


def update_recent_posts():
    pass


if __name__ == "__main__":
    posts = yaml.load(open("posts.yaml", encoding="utf-8"), Loader=yaml.FullLoader)
    print(posts)

    generate_sidebar(posts)
    generate_readme()
    update_recent_posts()
