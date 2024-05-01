from pydantic import BaseModel
from transformers import pipeline
from langchain_groq import ChatGroq
import os
import logging
import aiohttp
from bs4 import BeautifulSoup
import requests
import re

# Configure Logging Same again Update Logging and Error Handling As APP Usage Grows 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BaseTool(BaseModel):
    name: str
    description: str

    def _run(self, input: str) -> str:
        raise NotImplementedError("Subclasses must implement this method")

class GPT(BaseTool):
    name: str = "GPT"
    description: str = "A tool for generating text using OpenAI's GPT-3.5 Turbo model."

    def _run(self, prompt: str) -> str:
        groq_api_key = os.getenv('GROQ_API_KEY', 'your-default-api-key')
        if groq_api_key == 'your-default-api-key':
            logging.error("GROQ API Key is missing. Please set it in your environment variables.")
            raise ValueError("API Key is missing")
        groq_chat = ChatGroq(api_key=groq_api_key, model_name='gpt-3.5-turbo')
        response = groq_chat.complete(prompt=prompt, max_tokens=150, temperature=0.7)
        return response['choices'][0]['text'].strip()

# Example usage for GPT tool
#gpt_tool = GPT(name="GPT", description="A tool for generating text using OpenAI's GPT-3.5 Turbo model.")
#try:
    #response = gpt_tool._run("Generate some text based on this prompt.")
    #print(response)
#except Exception as e:
    #print(f"Failed to generate text: {str(e)}")

class DataAnalysis(BaseTool):
    name: str = "DataAnalysis"
    description: str = "Performs detailed analysis on data to extract insights and identify trends."

    def _run(self, metric_values: list) -> str:
        if not metric_values:
            return 'No data provided for analysis.'
        
        average = sum(metric_values) / len(metric_values)
        return f'Analysis complete. Average of metrics: {average:.2f}'

# Example usage for DataAnalysis tool
#data_analysis_tool = DataAnalysis(name="DataAnalysis", description="Performs detailed analysis on data to extract insights and identify trends.")
#try:
    #result = data_analysis_tool._run([10, 20, 30, 40, 50])
    #print(result)
#except Exception as e:
    #print(f"Failed to perform data analysis: {str(e)}")

class DatabaseTool(BaseTool):
    name: str = "DatabaseTool"
    description: str = "Asynchronously scrapes web and accesses datasets related to Maori land claims."

    async def scrape_data(self, url: str, session: aiohttp.ClientSession) -> str:
        async with session.get(url) as response:
            data = await response.text()
            soup = BeautifulSoup(data, 'html.parser')
            return ' '.join(item.get_text() for item in soup.find_all(class_='data-class-name'))

    async def _run(self, query: str) -> str:
        url = f"https://www.data.govt.nz/={query}"
        async with aiohttp.ClientSession() as session:
            scraped_data = await self.scrape_data(url, session)
            
            api_url = "https://www.xn--morilandcourt-wqb.govt.nz/"
            params = {'query': query}
            response = await session.get(api_url, params=params)
            if response.status == 200:
                api_data = await response.json()
            else:
                api_data = "Failed to retrieve data"

            result = f"Result from DatabaseTool: {scraped_data} | {api_data}"
            return result

# Example usage for DatabaseTool tool
#database_tool = DatabaseTool(name="DatabaseTool", description="Asynchronously scrapes web and accesses datasets related to Maori land claims.")
#try:
    #result = await database_tool._run("your_query_here")
    #print(result)
#except Exception as e:
    #print(f"Failed to access database: {str(e)}")

class LegalTool(BaseTool):
    name: str = "LegalTool"
    description: str = "Accesses legal databases for information on laws and precedents relevant to Maori land claims."

    def _run(self, legal_query: str) -> str:
        api_url = "https://www.xn--morilandcourt-wqb.govt.nz/"
        api_key = os.getenv('LEGAL_API_KEY')
        headers = {'Authorization': f'Bearer {api_key}'}
        params = {'query': legal_query, 'jurisdiction': 'New Zealand'}
        try:
            response = requests.get(api_url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                legal_data = response.json()
                result = f"Legal documents retrieved: {legal_data['documents']}"
            else:
                result = f"Failed to retrieve legal documents, status code: {response.status_code}"
        except requests.RequestException as e:
            result = f"Error accessing legal database: {str(e)}"

        return result

# Example usage for LegalTool tool
#legal_tool = LegalTool(name="LegalTool", description="Accesses legal databases for information on laws and precedents relevant to Maori land claims.")
#try:
    #result = legal_tool._run("legal_query_here")
    #print(result)
#except Exception as e:
    #print(f"Failed to access legal database: {str(e)}")

print('All Tools Loaded')
