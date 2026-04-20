from typing import Any

from mcp_server.tools.users.base import BaseUserServiceTool


class GetUserByIdTool(BaseUserServiceTool):

    @property
    def name(self) -> str:
        return "get_user_by_id"

    @property
    def description(self) -> str:
        return "Tool to get a user by id"

    @property
    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "ID of the user to retrieve"
                }
            },
            "required": ["id"]  
        }

    async def execute(self, arguments: dict[str, Any]) -> str:
        user_id = arguments.get("id")
        
        if user_id is None:
            raise ValueError("User ID is required")
        
        return await self._user_client.get_user(user_id)