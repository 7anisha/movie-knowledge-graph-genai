
from langchain import PromptTemplate
from langchain.prompts import PromptTemplate as P
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from genai.prompt_templates import sql2cypher_prompt

llm = ChatOpenAI(temperature=0.0, model="gpt-4o-mini")  # set your model

template = PromptTemplate(input_variables=["question"], template=sql2cypher_prompt)
chain = LLMChain(llm=llm, prompt=template)

def nl_to_cypher(question: str) -> str:
    output = chain.run({"question": question})
    # LLM sometimes returns fenced code or explanation; we try to extract first code block or line
    out = output.strip()
    # basic cleanup: keep only last line if multiple
    if "```" in out:
        out = out.split("```")[-2].strip()
    # ensure ends with newline
    return out
