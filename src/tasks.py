from textwrap import dedent
from crewai import Task
class MlcTask():
    def delegation_task(self, delegation_handler):  #Delegation Task 
        return Task(
            description=dedent('''\
                
    Perform Facilitate the transfer of findings from the Genealogist to the Cultural Researcher..'''),
                    
expected_output=dedent('''\

Successful integration of genealogical findings into cultural research..'''),
agent=delegation_handler,
async_execution=True)
    
    def research_task(self, research_agent): #Search Task
        return Task(
            description=dedent('''\
                
Explore extensive historical, cultural sources to gain nuanced understanding of the Maori
revealing their deep ties to land intricate traditions, societal systems, the profound 
impacts of colonial oppression. Investigate Maori land courts enduring processes of resilience 
amidst challenges..'''),

expected_output=dedent('''\
    
Craft an in depth report offering historical, cultural insights, delving into the intricate 
tapestry of Maori heritage, societal structures, and the enduring legacy of colonialism,
encapsulating the resilience and richness of their cultural narrative'''),
agent=research_agent,
async_execution=True )
    
    def legal_task(self, kings_council): #Legal Task 
        return Task(
            description=dedent('''\
                
Analyze legal precedents and current laws on Maori land claims in New Zealand..'''),

expected_output=dedent('''\
    
A legal advisory report with strategies and case summaries ..'''),
agent=kings_council,
async_execution=True )