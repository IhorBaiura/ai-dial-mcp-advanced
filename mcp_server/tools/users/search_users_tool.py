from typing import Any

from mcp_server.models.user_info import UserSearchRequest
from mcp_server.tools.users.base import BaseUserServiceTool


class SearchUsersTool(BaseUserServiceTool):

    @property
    def name(self) -> str:
        return "search_users"

    @property
    def description(self) -> str:
        return "Tool to search users by name, surname, email or gender"

    @property
    def input_schema(self) -> dict[str, Any]:
        return UserSearchRequest.model_json_schema()

    async def execute(self, arguments: dict[str, Any]) -> str:
        user_search_request = UserSearchRequest.model_validate(arguments)
        return await self._user_client.search_users(**user_search_request.model_dump())