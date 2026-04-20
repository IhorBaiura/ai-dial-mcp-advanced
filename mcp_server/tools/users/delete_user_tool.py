from typing import Any

from mcp_server.tools.users.base import BaseUserServiceTool


class DeleteUserTool(BaseUserServiceTool):

    @property
    def name(self) -> str:
        return "delete_user"

    @property
    def description(self) -> str:
        return "Tool to delete a user by id"

    @property
    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "ID of the user to delete"
                }
            },
            "required": ["id"]
        }

    async def execute(self, arguments: dict[str, Any]) -> str:
        user_id = arguments.get("id")

        if user_id is None:
            raise ValueError("User ID is required")
        
        return await self._user_client.delete_user(user_id)
    