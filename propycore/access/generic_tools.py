from .base import Base

import sys
import pathlib
sys.path.append(f"{pathlib.Path(__file__).resolve().parent.parent}")

from propycore.exceptions import NotFoundItemError

from exceptions import *

class GenericTool(Base):
    """
    Access and working with generic tool endpoints
    """
    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)

        self.endpoint = "/rest/v1.0/companies"

    def get_tools(self, company_id, per_page=100):
        """
        Gets all the available generic tools

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        per_page : int, default 100
            number of generic tools to find per page

        Returns
        -------
        tools : dict
            available generic tools
        """
        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        # List of generic tools is likely less than 100, but this could lead to errors in the future
        params = {
            "page": 1,
            "per_page": per_page
        }

        tools = self.get_request(
            api_url=f"{self.endpoint}/{company_id}/generic_tools",
            additional_headers=headers,
            params=params
        )

        return tools
    
    def find_tool(self, company_id, identifier):
        """
        Finds a tools based on the identifier: id or title

        Parameters
        ----------
        company_id : int
            company id that the project is under
        identifier : int or str
            project id number or company name
        
        Returns
        -------
        tool : dict
            tool-specific dictionary
        """
        if isinstance(identifier, int):
            key = "id"
        else:
            key = "title"

        for tool in self.get_tools(company_id=company_id):
            if tool[key] == identifier:
                return tool

        raise NotFoundItemError(f"Could not find tool {identifier}")
    
    def get_tool_items(self, company_id, project_id, tool_id):
        """
        Gets all the available items for a specific tool

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project
        tool_id : int
            unique identifier for the generic tool

        Returns
        -------
        items : dict
            available tool item data
        """
        n_items = 1
        page = 1
        items = []
        while n_items > 0:
            params = {
                "view": "extended",
                "sort": "created_at",
                "page": page,
                "per_page": 10000,
                "filters[recycle_bin]": False
            }

            headers = {
                "Procore-Company-Id": f"{company_id}"
            }

            item_info = self.get_request(
                api_url=f"/rest/v1.0/projects/{project_id}/generic_tools/{tool_id}/generic_tool_items",
                additional_headers=headers,
                params=params
            )

            n_items = len(item_info)
            items.append(item_info)

            page += 1 

        if len(items) > 0:
            return items
        else:
            raise NotFoundItemError(f"No items are available in Project {project_id} for tool {tool_id}")

    def create_tool_item(self, company_id, project_id, tool_id, data):
        """
        Create new item for a specific tool

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project
        tool_id : int
            unique identifier for the generic tool
        data : dict
            request body data for the new item

        Returns
        -------
        item_info : dict
            new item data
        """

        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        try:
            item_info = self.post_request(
                api_url=f"/rest/v1.0/projects/{project_id}/generic_tools/{tool_id}/generic_tool_items",
                additional_headers=headers,
                data=data
            )
        except ProcoreException as e:
            raise WrongParamsError(e)
        
        return item_info
    
    def get_tool_statuses(self, company_id, project_id, tool_id):
        """
        Gets all the available statuses for a specific tool

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project
        tool_id : int
            unique identifier for the generic tool

        Returns
        -------
        items : dict
            available tool item data
        """

        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        status_info = self.get_request(
            api_url=f"/rest/v1.0/projects/{project_id}/generic_tools/{tool_id}/generic_tool_items/available_statuses",
            additional_headers=headers
        )
        
        return status_info