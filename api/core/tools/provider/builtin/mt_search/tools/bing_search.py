from typing import Any, Union

import requests

from core.tools.entities.tool_entities import ToolInvokeMessage
from core.tools.tool.builtin_tool import BuiltinTool

SERP_API_URL = "https://aigc.sankuai.com/v1/friday/api/search"


class BingSearchTool(BuiltinTool):
    def _parse_response(self, response: dict) -> dict:
        result = {}
        if "results" in response:
            result["url"] = response["results"][0]["link"]
            result["title"] = response["results"][0]["title"]
            result["content"] = response["results"][0]["content"]
        return result

    def _invoke(
        self,
        user_id: str,
        tool_parameters: dict[str, Any],
    ) -> Union[ToolInvokeMessage, list[ToolInvokeMessage]]:

        header= {
            "Authorization": f"Bearer {self.runtime.credentials['serpapi_api_key']}",
            "Content-Type": "application/json",
        }

        json_payload = {
            "api": "bing-search",
            "query": tool_parameters["query"],
            "top_k": 1,
            "is_fast": False
        }
        response = requests.post(url=SERP_API_URL, json=json_payload, headers=header)
        response.raise_for_status()
        valuable_res = self._parse_response(response.json())
        return self.create_json_message(valuable_res)
