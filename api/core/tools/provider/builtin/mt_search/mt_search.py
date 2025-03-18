from typing import Any

from core.tools.errors import ToolProviderCredentialValidationError
from .tools.bing_search import BingSearchTool
from core.tools.provider.builtin_tool_provider import BuiltinToolProviderController


class GoogleZhtProvider(BuiltinToolProviderController):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            BingSearchTool().fork_tool_runtime(
                runtime={
                    "credentials": credentials,
                }
            ).invoke(
                user_id="",
                tool_parameters={"query": "test"},
            )
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
