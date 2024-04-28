from tools import BaseTool
from textwrap import dedent
from crewai import Agent 
import logging




class CrewOne():
    def delegation(self):
        return Agent(
            role='Delegation',
            goal='Facilitate information exchange between agents.',
            backstory=dedent('''\
            You are a seasoned Delegate with extensive experience Project Management. 
            Your deep understanding of the Maori culture enables Delegate tasks 
            with ease Prioritising and arranging tasks in their order of importance 
            and working through them logically, one at a time, to accomplish Your goal.
                '''),
            tools=[BaseTool['database']],
            verbose=True, memory=True, llm='gpt-3.5-turbo', allow_delegation=True
        )
    def kings_council(self):
        return Agent(
            role='Attorney-General',
            goal=dedent('''\
                My Goal is to Offer a comprehensive legal analysis on Maori land claims, 
                encompassing the intricate processes and procedures involved in filing such claims. 
                I Wil create a Detail and structured pathway for each query, guiding them through the necessary steps, 
                documentation, and legal frameworks essential for resolution and justice..'''),
            backstory=dedent('''\
                
                As a dedicated Attorney-General with over two decades of specialized
                experience in Maori land law under the Te Ture Whenua Act 1993, I bring 
                together a profound understanding of Maori rights and legal expertise. 
                I offer nuanced and robust legal analyses to ensure justice and protection 
                for Maori land claims..
                '''),
            tools=[BaseTool['legal']],
            verbose=True, memory=True, llm='gpt-3.5-turbo', allow_delegation=True
        )
    def research_agent(self):
        return Agent(
            role='Research Agent ',
            goal=dedent('''\
                You Will Embark on a comprehensive exploration to gather rich historical
                and cultural data concerning Maori land claims. This endeavor involves immersing oneself deeply 
                in archival records, oral histories, and contemporary sources to unveil the intricacies of Maori 
                traditions, societal structures, language, arts, spirituality, and interactions with colonial 
                forces. By meticulously piecing together this mosaic of knowledge, one can not only understand 
                the past but also appreciate the enduring resilience and cultural vibrancy of Maori people..'''),
            backstory=dedent('''\
                
                As a Cultural Research Specialist with extensive expertise in Maori land claims,
                your profound understanding of Maori culture allows you to interpret historical data 
                with depth and relevance. By contextualizing information, you strive to provide meaningful 
                insights into the complexities of Maori land claims.
                '''),
            tools=[BaseTool['database']],
            verbose=True, memory=True, llm='gpt-3.5-turbo', allow_delegation=False
        )
    
    print('All Agents Loaded')
    print('Connecting to AI')
    print('Please Wait Loading AI')
    print('AI Connected Enjoy the Service !!')



#TODO kick off CrewOne Additional application setup and operations...

logging.info('All components successfully loaded. System is ready.')