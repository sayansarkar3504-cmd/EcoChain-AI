import json
from .vendor_agent import VendorComplianceAgent
from .security_agent import SecurityRiskAgent
from .insight_agent import BusinessInsightAgent

class OrchestratorAgent:
    def __init__(self):
        self.vendor_agent = VendorComplianceAgent()
        self.security_agent = SecurityRiskAgent()
        self.insight_agent = BusinessInsightAgent()

    def handle_request(self, user_request: str, invoice_path: str = None) -> dict:
        """
        Main entry point for ADK Orchestrator Agent.
        Delegates work to specialized agents and combines final results.
        """
        # 1. Security Check & Masking
        security_result = self.security_agent.process_request(user_request)
        if security_result["status"] == "REJECTED":
            return {"error": security_result["reason"]}
        
        safe_request = security_result["data"]
        
        vendor_name = self._extract_vendor_name(safe_request)
        if not vendor_name:
             return {"error": "Could not identify a vendor name in the request."}

        # 2. Vendor Analysis
        vendor_result_json = self.vendor_agent.analyze_vendor(vendor_name)
        vendor_result = json.loads(vendor_result_json)
        
        if "error" in vendor_result:
            return {"error": vendor_result["error"]}
            
        # Optional: Invoice analysis if provided
        if invoice_path:
            invoice_data = self.vendor_agent.analyze_invoice(invoice_path)
            vendor_result["invoice_analysis"] = invoice_data
            
        # 3. Business Insights
        insights = self.insight_agent.generate_insights(vendor_result)
        
        # 4. Final Security Validation on Output
        final_validation = self.security_agent.validate_output(insights)
        if final_validation["status"] == "BLOCKED":
            return {"error": final_validation["reason"]}
            
        return {
            "vendor_data": vendor_result,
            "business_insights": final_validation["data"]
        }

    def _extract_vendor_name(self, request: str) -> str:
        """
        Naive extraction logic for the prototype.
        Looks for 'Analyze vendor [Name]' or just returns the request if it's short.
        """
        req_lower = request.lower()
        if "analyze vendor" in req_lower:
            parts = req_lower.split("analyze vendor")
            return parts[1].strip()
        # Fallback: assume the request itself is the vendor name if it's just a few words
        if len(request.split()) <= 3:
            return request.strip()
        return None

if __name__ == "__main__":
    orchestrator = OrchestratorAgent()
    result = orchestrator.handle_request("Analyze vendor GlobalTech Supplies")
    print(json.dumps(result, indent=2))
