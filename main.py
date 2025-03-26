import google.generativeai as genai
from typing import List, Dict
import json
import os
import asyncio

class IndustryResearchAgent:
    def __init__(self, model):
        self.model = model
    
    async def research_company(self, company_name: str) -> Dict:
        prompt = f"""
        Provide a comprehensive analysis of {company_name} including:
        1. Industry sector and main business areas
        2. Key products and services
        3. Strategic focus areas
        4. Current technological infrastructure
        5. Main operational challenges
        
        Return your response in this exact JSON format:
        {{
            "industry_sector": "description here",
            "products_and_services": "description here",
            "strategic_focus": "description here",
            "tech_infrastructure": "description here",
            "operational_challenges": "description here"
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start != -1 and end != -1:
                json_str = response_text[start:end]
                return json.loads(json_str)
            else:
                return {
                    "industry_sector": response_text,
                    "products_and_services": "",
                    "strategic_focus": "",
                    "tech_infrastructure": "",
                    "operational_challenges": ""
                }
        except Exception as e:
            print(f"Error in research_company: {str(e)}")
            return {
                "industry_sector": "Error processing response",
                "products_and_services": "",
                "strategic_focus": "",
                "tech_infrastructure": "",
                "operational_challenges": ""
            }

class UseCaseGenerationAgent:
    def __init__(self, model):
        self.model = model
    
    async def generate_use_cases(self, company_analysis: Dict) -> List[Dict]:
        prompt = f"""
        Based on this company analysis:
        {json.dumps(company_analysis, indent=2)}
        
        Generate 5 specific AI/ML use cases that could benefit this company.
        
        Return your response in this exact JSON format:
        [
            {{
                "title": "Use Case Title",
                "description": "Detailed description",
                "benefits": "Expected benefits",
                "complexity": "High/Medium/Low",
                "roi_impact": "Potential ROI impact",
                "technologies": "Required AI/ML technologies"
            }}
        ]
        """
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text
            start = response_text.find('[')
            end = response_text.rfind(']') + 1
            if start != -1 and end != -1:
                json_str = response_text[start:end]
                return json.loads(json_str)
            else:
                return [{
                    "title": "Error processing response",
                    "description": response_text,
                    "benefits": "",
                    "complexity": "",
                    "roi_impact": "",
                    "technologies": ""
                }]
        except Exception as e:
            print(f"Error in generate_use_cases: {str(e)}")
            return [{
                "title": "Error processing response",
                "description": "Failed to generate use cases",
                "benefits": "",
                "complexity": "",
                "roi_impact": "",
                "technologies": ""
            }]

class ResourceAssetAgent:
    def __init__(self, model):
        self.model = model
        
    async def collect_resources(self, use_cases: List[Dict]) -> Dict:
        resources = {}
        for use_case in use_cases:
            prompt = f"""
            For this AI/ML use case:
            {json.dumps(use_case, indent=2)}
            
            Find relevant resources and return them in this exact JSON format:
            {{
                "github_repositories": ["repo1 with link", "repo2 with link"],
                "datasets": ["dataset1 with link", "dataset2 with link"],
                "research_papers": ["paper1 with link", "paper2 with link"]
            }}
            """
            
            try:
                response = self.model.generate_content(prompt)
                response_text = response.text
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                if start != -1 and end != -1:
                    json_str = response_text[start:end]
                    resources[use_case['title']] = json.loads(json_str)
                else:
                    resources[use_case['title']] = {
                        "github_repositories": [],
                        "datasets": [],
                        "research_papers": []
                    }
            except Exception as e:
                print(f"Error collecting resources for {use_case['title']}: {str(e)}")
                resources[use_case['title']] = {
                    "github_repositories": [],
                    "datasets": [],
                    "research_papers": []
                }
        
        return resources

class AIUseCaseGenerator:
    def __init__(self, google_api_key: str):
        genai.configure(api_key=google_api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
        
        self.research_agent = IndustryResearchAgent(self.model)
        self.use_case_agent = UseCaseGenerationAgent(self.model)
        self.resource_agent = ResourceAssetAgent(self.model)
        
    async def generate_proposal(self, company_name: str) -> Dict:
        try:
            company_analysis = await self.research_agent.research_company(company_name)
            use_cases = await self.use_case_agent.generate_use_cases(company_analysis)
            resources = await self.resource_agent.collect_resources(use_cases)
            
            proposal = {
                "company_analysis": company_analysis,
                "use_cases": use_cases,
                "resources": resources
            }
            
            return proposal
            
        except Exception as e:
            print(f"Error generating proposal: {str(e)}")
            raise

async def main():
    try:
        google_api_key = os.getenv('google_api_key')
        generator = AIUseCaseGenerator(google_api_key)
        company_name = "Seagate"
        proposal = await generator.generate_proposal(company_name)
        print(json.dumps(proposal, indent=2))
    except Exception as e:
        print(f"Error in main: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
