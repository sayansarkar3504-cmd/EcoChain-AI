from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

class BusinessInsightAgent:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")

        if self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception:
                self.client = None
        else:
            self.client = None

    def generate_insights(self, vendor_data: dict) -> str:
        """
        Generates business insights.
        Uses Gemini if available, otherwise returns a premium demo report.
        """

        # =====================================================
        # DEMO MODE (NO GEMINI API REQUIRED)
        # =====================================================
        if not self.client:
            compliance = vendor_data.get("compliance_score", 92)
            carbon = vendor_data.get("carbon_score", 84)
            risk = vendor_data.get("risk", "LOW")

            return f"""
# 🌍 Executive Sustainability Report

## 📊 Vendor Performance Summary
- Compliance Score: **{compliance}%**
- Sustainability Score: **{carbon}%**
- Risk Level: **{risk}**

## 💰 Cost Saving Opportunities
- Reduce logistics expenses by **8-12%**
- Consolidate procurement contracts
- Introduce predictive inventory planning

## 📈 ROI Analysis
- Estimated Annual Savings: **$250,000**
- Expected ROI: **18-24%**
- Sustainability Investment Payback: **12-14 months**

## ♻ Sustainability Recommendations
1. Increase renewable energy sourcing
2. Improve supplier carbon reporting
3. Implement quarterly ESG audits
4. Automate invoice compliance validation

## 🎯 Strategic Recommendation
This vendor demonstrates strong compliance and sustainability performance.
Recommended for long-term partnership and preferred supplier status.

### Overall Assessment
🟢 APPROVED VENDOR
"""
        
        # =====================================================
        # GEMINI MODE
        # =====================================================
        prompt = f"""
        You are a Senior Enterprise Sustainability Consultant.

        Analyze this vendor information:

        {vendor_data}

        Generate:

        1. Vendor Ranking
        2. Cost Saving Opportunities
        3. ROI Analysis
        4. Sustainability Recommendations
        5. Executive Summary

        Format in professional markdown.
        """

        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.4
                )
            )

            return response.text

        except Exception as e:
            return f"""
# ⚠ AI Service Unavailable

Gemini could not generate insights.

Error:
{str(e)}

## Fallback Recommendation
- Continue monitoring vendor compliance
- Perform quarterly sustainability reviews
- Maintain ESG documentation
- Optimize procurement workflows
"""


if __name__ == "__main__":
    agent = BusinessInsightAgent()

    sample_data = {
        "vendor": "GlobalTech Supplies",
        "compliance_score": 96,
        "carbon_score": 88,
        "risk": "LOW"
    }

    print(agent.generate_insights(sample_data))