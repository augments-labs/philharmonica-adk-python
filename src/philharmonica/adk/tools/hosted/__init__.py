"""Cross-provider hosted-tool classes.

Each class represents a capability the LLM provider executes
server-side (web search, code execution, file search, image
generation, URL context). The framework forwards typed config to
each provider's wire format via the matching converter's
``isinstance`` dispatch — when a provider does not support a
variant, the converter raises :class:`UnsupportedHostedToolError`
rather than silently dropping.

Public exports:

- :class:`HostedTool` — the abstract base every concrete hosted
  tool inherits from.
- :class:`UnsupportedHostedToolError` — raised by a provider's
  converter when it does not support the hosted-tool variant.
- :class:`WebSearchTool` — Anthropic + OpenAI Responses + Gemini.
- :class:`CodeExecutionTool` — OpenAI Responses + Gemini.
- :class:`FileSearchTool` — OpenAI Responses only.
- :class:`ImageGenerationTool` — OpenAI Responses only.
- :class:`URLContextTool` — Gemini only.
- :class:`HostedMCPTool` — OpenAI Responses only (provider-side MCP).
- :class:`ComputerTool` — OpenAI Responses only (hybrid: the provider
  declares the tool, the developer's :class:`Computer` callable
  executes each action locally).
- :class:`Computer` / :class:`SafetyCheck` — typed protocol + safety
  payload supporting :class:`ComputerTool`.
"""

from philharmonica.adk.tools.hosted.code_execution_tool import CodeExecutionTool
from philharmonica.adk.tools.hosted.computer_tool import (
    Computer,
    ComputerTool,
    SafetyCheck,
)
from philharmonica.adk.tools.hosted.exceptions import UnsupportedHostedToolError
from philharmonica.adk.tools.hosted.file_search_tool import FileSearchTool
from philharmonica.adk.tools.hosted.hosted_tool import HostedTool
from philharmonica.adk.tools.hosted.image_generation_tool import ImageGenerationTool
from philharmonica.adk.tools.hosted.mcp_tool import HostedMCPTool
from philharmonica.adk.tools.hosted.url_context_tool import URLContextTool
from philharmonica.adk.tools.hosted.web_search_tool import WebSearchTool

__all__ = [
    "CodeExecutionTool",
    "Computer",
    "ComputerTool",
    "FileSearchTool",
    "HostedMCPTool",
    "HostedTool",
    "ImageGenerationTool",
    "SafetyCheck",
    "URLContextTool",
    "UnsupportedHostedToolError",
    "WebSearchTool",
]
