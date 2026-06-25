from .database import execute_query
import json

def get_vendor(vendor_name: str) -> str:
    """
    Retrieves the details of a specific vendor from the database.
    """
    query = "SELECT * FROM vendors WHERE name = %s"
    result = execute_query(query, (vendor_name,))
    if not result:
        return json.dumps({"error": f"Vendor '{vendor_name}' not found."})
    return json.dumps(result[0])

def get_vendor_history(vendor_name: str) -> str:
    """
    Retrieves the history (audit logs related to the vendor) or details of a specific vendor.
    """
    # For prototype, history might just mean returning vendor details and any past invoices
    query_vendor = "SELECT id, name FROM vendors WHERE name = %s"
    vendor_res = execute_query(query_vendor, (vendor_name,))
    if not vendor_res:
         return json.dumps({"error": f"Vendor '{vendor_name}' not found."})
    
    vendor_id = vendor_res[0]["id"]
    query_invoices = "SELECT * FROM invoices WHERE vendor_id = %s"
    invoices = execute_query(query_invoices, (vendor_id,))
    
    return json.dumps({
        "vendor": vendor_res[0],
        "history": invoices if invoices else []
    })

def get_invoice_data(vendor_id: int) -> str:
    """
    Retrieves all invoice records for a specific vendor ID.
    """
    query = "SELECT * FROM invoices WHERE vendor_id = %s"
    result = execute_query(query, (vendor_id,))
    if result is None:
        return json.dumps({"error": "Failed to fetch invoices."})
    return json.dumps(result)

def calculate_risk_score(vendor_id: int) -> str:
    """
    Queries the database for the vendor's carbon and compliance scores and calculates risk.
    """
    query = "SELECT carbon_score, compliance_status FROM vendors WHERE id = %s"
    result = execute_query(query, (vendor_id,))
    if not result:
        return json.dumps({"error": "Vendor not found."})
    
    score_data = result[0]
    carbon_score = score_data.get("carbon_score")
    compliance_status = score_data.get("compliance_status")
    
    risk = "LOW"
    if compliance_status != "Compliant":
        risk = "HIGH"
    elif carbon_score and carbon_score < 70:
        risk = "MEDIUM"
        
    return json.dumps({
        "vendor_id": vendor_id,
        "carbon_score": carbon_score,
        "compliance_status": compliance_status,
        "calculated_risk": risk
    })

def log_agent_action(agent_name: str, action: str) -> str:
    """
    Logs an agent's action to the audit_logs table.
    """
    query = "INSERT INTO audit_logs (agent_name, action) VALUES (%s, %s)"
    rows_affected = execute_query(query, (agent_name, action), fetch=False)
    if rows_affected:
        return json.dumps({"status": "success", "message": "Action logged successfully."})
    return json.dumps({"error": "Failed to log action."})
