# flake8: noqa: E501
import json
from typing import Any, Dict, List


class HTMLTweetsVisualizer:
    """
    Class responsible for generating an HTML file to visualize the parsed data.

    :param json_content: The content of the JSON file.
    :param html_file_path: The path where the HTML file will be saved.
    :param username: The username associated with the tweets.
    """

    def __init__(self, json_file_path: str, html_file_path: str, username: str):
        self.json_content = self._json_loader(json_file_path)
        self.html_file_path = html_file_path
        self.username = username

    @staticmethod
    def _json_loader(json_file_path: str) -> List[Dict[str, Any]]:
        """
        Reads and loads JSON data from a specified file path.

        :param json_file_path: The path of the JSON file.

        :returns: The content of the JSON file.
        """
        with open(json_file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def generate(self) -> str:
        """
        Generates an HTML string that represents the parsed data.

        :returns: The generated HTML string.
        """

        html = f"<html>\n<head>\n<title>@{self.username} archived tweets</title>\n"
        html += "<style>\n"
        html += "body { font-family: monospace; background-color: #f5f8fa; color: #1c1e21; margin: 0; padding: 20px; }\n"
        html += ".container { display: flex; flex-wrap: wrap; gap: 20px; }\n"
        html += ".tweet { flex: 0 1 calc(33.33% - 20px); background-color: #fff; border: 1px solid #e1e8ed; border-radius: 10px; padding: 15px; overflow-wrap: break-word; margin: auto; }\n"
        html += ".tweet strong { font-weight: bold; }\n"
        html += ".tweet a { color: #ef5552; text-decoration: none; }\n"
        html += ".content { color: #ef5552; }\n"
        html += ".tweet a:hover { text-decoration: underline; }\n"
        html += "h1, h3 { text-align: center; }\n"
        html += "iframe { width: 600px; height: 600px; }\n"
        html += "</style>\n"
        html += "</head>\n<body>\n"
        html += f"<h1>@{self.username} archived tweets</h1>\n"
        html += '<div class="container">\n'

        for tweet in self.json_content:
            html += '<div class="tweet">\n'

            # TODO: JSON Issue
            # if (
            #     (
            #         tweet["archived_mimetype"] != "application/json"
            #         and not tweet["parsed_tweet_text_mimetype_json"]
            #     )
            #     and not tweet["available_tweet_text"]
            # ) or (
            #     (
            #         tweet["archived_mimetype"] == "application/json"
            #         and not tweet["parsed_tweet_text_mimetype_json"]
            #     )
            #     and not tweet["available_tweet_text"]
            # ):
            if (
                tweet["archived_mimetype"] != "application/json"
                and not tweet["available_tweet_text"]
            ):
                html += f'<iframe src="{tweet["parsed_archived_tweet_url"]}" frameborder="0" scrolling="auto"></iframe>\n'

            html += f'<p><a href="{tweet["original_tweet_url"]}" target="_blank"><strong>Original Tweet↗</strong></a> · \n'
            html += f'<a href="{tweet["parsed_tweet_url"]}" target="_blank"><strong>Parsed Tweet↗</strong></a> · \n'
            html += f'<a href="{tweet["archived_tweet_url"]}" target="_blank"><strong>Archived Tweet↗</strong></a> · \n'
            html += f'<a href="{tweet["parsed_archived_tweet_url"]}" target="_blank"><strong>Parsed Archived Tweet↗</strong></a></p>\n'

            if tweet["available_tweet_text"]:
                html += "<br>\n"
                html += f'<p><strong class="content">Available Tweet Content:</strong> {tweet["available_tweet_text"]}</p>\n'
                html += f'<p><strong class="content">Available Tweet Is Retweet:</strong> {tweet["available_tweet_is_RT"]}</p>\n'
                html += f'<p><strong class="content">Available Tweet Username:</strong> {tweet["available_tweet_info"]}</p>\n'

            # TODO: JSON Issue
            # if (
            #     tweet["archived_mimetype"] == "application/json"
            #     and tweet["parsed_tweet_text_mimetype_json"]
            # ) and not tweet["available_tweet_text"]:
            #     html += f'<p><strong class="content">Parsed Tweet Text (application/json):</strong> {tweet["parsed_tweet_text_mimetype_json"]}</p>\n'

            html += "<br>\n"
            html += f'<p><strong>Archived URL Key:</strong> {tweet["archived_urlkey"]}</p>\n'
            html += f'<p><strong>Archived Timestamp:</strong> {tweet["archived_timestamp"]}</p>\n'
            html += f'<p><strong>Archived mimetype:</strong> {tweet["archived_mimetype"]}</p>\n'
            html += f'<p><strong>Archived Statuscode:</strong> {tweet["archived_statuscode"]}</p>\n'
            html += (
                f'<p><strong>Archived Digest:</strong> {tweet["archived_digest"]}</p>\n'
            )
            html += (
                f'<p><strong>Archived Length:</strong> {tweet["archived_length"]}</p>\n'
            )
            html += "</div>\n"

        html += "</div>\n"
        html += '<h3>generated by <a href="https://github.com/claromes/waybacktweets" target="_blank">Wayback Tweets↗</a></h3>\n'
        html += "</body>\n</html>"

        return html

    def save(self, html_content: str) -> None:
        """
        Saves the generated HTML string to a file.

        :param html_content: The HTML string to be saved.
        """
        with open(self.html_file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
