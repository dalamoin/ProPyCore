import os
import sys
import pathlib
sys.path.append(f"{pathlib.Path(__file__).resolve().parent.parent}")

from propycore.procore import Procore

from dotenv import load_dotenv

if os.getenv("CLIENT_ID") is None:
    load_dotenv()

PATH_TO_TOP = f"{pathlib.Path(__file__).resolve().parent.parent}"

if __name__ == "__main__":
    connection = Procore(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri=os.getenv("REDIRECT_URI"),
        oauth_url=os.getenv("OAUTH_URL"),
        base_url=os.getenv("BASE_URL")
    )

    # Get IDs for company, project, and tool
    company = connection.__companies__.find(identifier="Rogers-O`Brien Construction")
    project = connection.__projects__.find(
        company_id=company["id"],
        identifier="Sandbox Test Project"
    )
    tool = connection.__tools__.find_tool(
        company_id=company["id"],
        identifier="Idea Submission"
    )
    status = connection.__tools__.get_tool_statuses(
        company_id=company["id"],
        tool_id=tool["id"]
    )
    print("Company:", company["id"])
    print("Project:", project["id"])
    print("Tool:", tool["id"])
    print("Statuses:", status)

    # Example 1: delete new idea submission status
    # ---------
    print("Example 1")
    # delete the item
    _ = connection.__tools__.delete_tool_status(
        company_id=company["id"],
        tool_id=tool["id"],
        status_id=1234
    )

    