from haystack.nodes import AnswerParser, PromptNode, PromptTemplate
from haystack.agents import Agent, Tool
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv(".env")

# Get the API key
openai_api_key = os.getenv("OPENAI-API")
chosen_model = os.getenv("OPENAI-MODEL")

# Define the tools that the agent has access to
# The agent has access to the following tools:
sql_agent_prompt = PromptTemplate(
            name="sql-agent-prompt", 
            prompt_text="You are a helpful and knowledgeable agent who has access to an SQL database which has a table called 'absenteeism'"
                        " that has the following Columns: ID;Reason_for_absence;Month_of_absence;Day_of_the_week;Seasons;Transportation_expense;Distance_from_Residence_to_Work;Service_time;Age;Work_load_Average/day_;Hit_target;Disciplinary_failure;Education;Son;Social_drinker;Social_smoker;Pet;Weight;Height;Body_mass_index;Absenteeism_time_in_hours"
                        "Your task is to assess whether a query can be resolved with the tools you have at hand, and if yes, generate an SQL query to resolve it."
                        "The generated SQL query should be stripped down to just the query with no syntax highlighting."
                        "You have access to the following tools:\n\n"
                        "{tool_names_with_descriptions}\n\n"
                        "To answer questions, you'll need to go through multiple steps involving step-by-step thinking and "
                        "selecting appropriate tools and their inputs; tools will respond with observations."
                        "When you are ready wity an answer, respond with the `Final Answer:`\n\n"
                        "If the query is unrelated and cannot be answered by any of the tools, your final answer should say 'Cannot be answered with available databases'\n\n"
                        "Use the following format:\n\n"
                        "Question: the question to be answered\n"
                        "Thought: Reason if you have the final answer. If yes, answer the query. If not, continue using the tools to resolve the query.\n"
                        "Tool: pick one of {tool_names} \n"
                        "Tool Input: the input for the tool.\n"
                        "Observation: The full result the tool responds with\n"
                        "...\n"
                        "Final Answer: the final answer to the query. This should be the full result of the SQL query that you came up with.\n\n"
                        "Thought, Tool, Tool Input, and Observation steps can be repeated multiple times, but sometimes we can find an answer in the first pass\n"
                        "---\n\n"
                        "Question: {query}\n"
                        "Thought: Let's think step-by-step, I first need to\n"
                        "{transcript}",
        )
# Define a prompt node that uses the GPT-4 model
prompt_node = PromptNode(model_name_or_path=chosen_model, 
                         api_key=openai_api_key, 
                         stop_words=["Observation:"], 
                         max_length=1000)

# Define the agent
agent = Agent(prompt_node=prompt_node, 
              prompt_template=sql_agent_prompt)

