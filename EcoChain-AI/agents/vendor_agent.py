import pandas as pd
import json
import fitz  # PyMuPDF
import os

class VendorComplianceAgent:
    def __init__(self, data_path="data/vendors.csv"):
        self.data_path = data_path

    def analyze_invoice(self, file_path: str) -> dict:
        """
        Reads a PDF or CSV invoice and extracts text/data.
        """
        if not os.path.exists(file_path):
            return {"error": f"File {file_path} not found"}
            
        ext = file_path.split('.')[-1].lower()
        if ext == 'pdf':
            try:
                doc = fitz.open(file_path)
                text = ""
                for page in doc:
                    text += page.get_text()
                return {"status": "success", "type": "pdf", "extracted_text": text}
            except Exception as e:
                return {"error": f"Failed to parse PDF: {str(e)}"}
        elif ext == 'csv':
            try:
                df = pd.read_csv(file_path)
                return {"status": "success", "type": "csv", "data": df.to_dict(orient="records")}
            except Exception as e:
                return {"error": f"Failed to parse CSV: {str(e)}"}
        else:
            return {"error": "Unsupported file format. Please upload a PDF or CSV."}

    def check_vendor_status(self, vendor_name: str) -> dict:
        """
        Retrieves vendor data from the CSV database.
        """
        try:
            df = pd.read_csv(self.data_path)
            vendor_data = df[df['name'].str.lower() == vendor_name.lower()]
            
            if vendor_data.empty:
                return {"error": f"Vendor '{vendor_name}' not found."}
                
            return vendor_data.iloc[0].to_dict()
        except Exception as e:
            return {"error": str(e)}

    def calculate_compliance_score(self, vendor_info: dict) -> dict:
        """
        Calculates compliance and risk scores.
        """
        base_score = 100
        try:
            carbon_score = int(vendor_info.get('carbon_score', 0))
            status = vendor_info.get('compliance_status', 'Unknown')
            
            if status != 'Compliant':
                base_score -= 30
                risk = "HIGH"
            elif carbon_score < 70:
                base_score -= 10
                risk = "MEDIUM"
            else:
                risk = "LOW"
                
            return {
                "vendor": vendor_info.get('name'),
                "compliance_score": base_score,
                "carbon_score": carbon_score,
                "risk": risk
            }
        except Exception as e:
            return {"error": f"Score calculation failed: {str(e)}"}

    def analyze_vendor(self, vendor_name: str) -> str:
        """
        Main entry point that checks status and calculates score.
        """
        vendor_info = self.check_vendor_status(vendor_name)
        if "error" in vendor_info:
            return json.dumps(vendor_info)
            
        score_data = self.calculate_compliance_score(vendor_info)
        return json.dumps(score_data)

if __name__ == "__main__":
    agent = VendorComplianceAgent("../data/vendors.csv")
    print(agent.analyze_vendor("GlobalTech Supplies"))
