import os
import json
import sys
import random
import pathlib
sys.path.append(f"{pathlib.Path(__file__).resolve().parent.parent}")

from ProPyCore.procore import Procore
from dotenv import load_dotenv
from datetime import datetime, timedelta

if os.getenv("CLIENT_ID") is None:
    load_dotenv()

def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )

if __name__ == "__main__":
    connection = Procore(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri=os.getenv("REDIRECT_URI"),
        oauth_url=os.getenv("OAUTH_URL"),
        base_url=os.getenv("BASE_URL")
    )

    company = connection.companies.find(identifier="Rogers-O`Brien Construction")
    project = connection.projects.find(
        company_id=company["id"],
        identifier="Sandbox Test Project"
    )
    print(company["id"])
    print(project["id"])

    # Example 1
    # ---------
    print("Example 1")
    dcs = connection.direct_costs.get(
        company_id=company["id"],
        project_id=project["id"]
    )
    print(f"Number of Direct Cost Items: {len(dcs)}")
    print(json.dumps(dcs[0], indent=4))
    
    # Example 2
    # ---------
    print("Example 2")
    direct_cost_id=dcs[0]["id"]
    print(direct_cost_id)
    dc = connection.direct_costs.show(
        company_id=company["id"],
        project_id=project["id"],
        direct_cost_id=direct_cost_id
    )

    print(f"Number of Direct Cost Items: {len(dcs)}")
    print(json.dumps(dc, indent=4))

    # Example 3
    # ---------
    print("Example 3")
    dc_find = connection.direct_costs.find(
        company_id=company["id"],
        project_id=project["id"],
        identifier=direct_cost_id
    )

    print(json.dumps(dc_find, indent=4))

    # Example 3
    # ---------
    print("Example 3")
    try:
        dc_not_found = connection.direct_costs.find(
            company_id=company["id"],
            project_id=project["id"],
            identifier=1
        )

        print(json.dumps(dc_not_found, indent=4))
    except Exception as e:
        print(f"Error: {e}")

    # Example 4
    # ---------
    print("Example 4")
    # Example of creating a Direct Cost item
    # Generate a random date between two dates
    start_date = datetime.strptime('2024-01-01', '%Y-%m-%d')
    end_date = datetime.strptime('2024-12-31', '%Y-%m-%d')
    random_day = random_date(start_date, end_date).date()
    direct_cost_data = {
        "description": f"Invoice for {random_day.strftime('%B %d, %Y')}",
        "direct_cost_date": random_day.strftime('%Y-%m-%d'),
        "employee_id": 8780450,
        "invoice_number": f"Invoice {random_day.strftime('%Y-%m-%d')}",
        "origin_data": f"OD-{''.join(random.choices('0123456789', k=10))}",
        "origin_id": f"px-{''.join(random.choices('0123456789', k=4))}",
        "payment_date": f"{(start_date + timedelta(days=10)).strftime('%Y-%m-%d')}",
        "received_date": f"{(start_date + timedelta(days=10)).strftime('%Y-%m-%d')}",
        "status": "approved",
        "terms": "Net 50",
        "vendor_id": 5181441,
        "direct_cost_type": "invoice"
    }

    line_items = [
        {
            "manual_amount": 1000,
            "wbs_code_id": 1989,
            "description": "100' of Copper Piping",
            "direct_cost_id": 81753,
            "origin_data": "OD-2398273424",
            "origin_id": "px-1990",
            "quantity": 82.0201,
            "ref": "PQRS5678",
            "unit_cost": 12.03,
            "uom": "cubic feet"
        }
    ]

    attachments = ["./dummy/direct_costs_module.pdf"]

    created_direct_cost = connection.direct_costs.create(
        company_id=company["id"],
        project_id=project["id"],
        direct_cost_data=direct_cost_data,
        line_items=line_items,
        attachments=attachments
    )
