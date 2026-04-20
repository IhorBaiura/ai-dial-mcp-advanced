from typing import Any, cast

from mcp_server.models.user_info import UserUpdate
from mcp_server.tools.users.base import BaseUserServiceTool


class UpdateUserTool(BaseUserServiceTool):

    @property
    def name(self) -> str:
        return "update_user"

    @property
    def description(self) -> str:
        return "Tool to update a user by id"

    @property
    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "ID of the user to update"
                },
                "new_info": UserUpdate.model_json_schema()
            },
            "required": ["id", "new_info"]
        }

    async def execute(self, arguments: dict[str, Any]) -> str:
        user_id = cast(int, arguments.get("id"))
        new_info_data = arguments.get("new_info")
        user_update = UserUpdate.model_validate(new_info_data)
        return await self._user_client.update_user(user_id, user_update)
