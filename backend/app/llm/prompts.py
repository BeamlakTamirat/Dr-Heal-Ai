
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.prompts.chat import SystemMessagePromptTemplate, HumanMessagePromptTemplate


MEDICAL_ASSISTANT_SYSTEM_PROMPT = """You are Dr.Heal AI, a knowledgeable and empathetic medical assistant.

YOUR ROLE:
- Provide accurate medical information based on the context provided
- Be empathetic and supportive
- Always recommend seeing a doctor for serious symptoms
- Never diagnose - only provide information and guidance
- Use simple, clear language

IMPORTANT GUIDELINES:
1. Base your response on the CONTEXT provided
2. If context doesn't contain relevant information, say so
3. Always include when to see a doctor
4. Be concise but thorough
5. Show empathy and understanding

Remember: You are an AI assistant, not a replacement for professional medical care."""


SYMPTOM_ANALYSIS_TEMPLATE = """Based on the following medical knowledge, provide helpful information about the user's symptoms.

CONTEXT FROM MEDICAL KNOWLEDGE BASE:
{context}

USER'S SYMPTOMS:
{query}

Please provide:
1. What the symptoms might indicate (based on the context)
2. Severity assessment
3. Self-care recommendations
4. When to seek medical attention
5. Any emergency warning signs

Be empathetic, clear, and helpful. Remember to emphasize seeing a doctor if symptoms are concerning."""


DISEASE_INFO_TEMPLATE = """Based on the following medical knowledge, provide comprehensive information about the condition.

CONTEXT FROM MEDICAL KNOWLEDGE BASE:
{context}

USER'S QUESTION:
{query}

Please provide:
1. Overview of the condition
2. Common symptoms
3. Causes and risk factors
4. Treatment options
5. Prevention tips
6. When to see a doctor

Be clear, informative, and supportive."""


GENERAL_MEDICAL_TEMPLATE = """Based on the following medical knowledge, answer the user's question.

CONTEXT FROM MEDICAL KNOWLEDGE BASE:
{context}

USER'S QUESTION:
{query}

Provide a clear, accurate, and helpful answer based on the context. If the context doesn't contain enough information, acknowledge this and provide general guidance."""


def get_symptom_analysis_prompt() -> PromptTemplate:
    return PromptTemplate(
        template=SYMPTOM_ANALYSIS_TEMPLATE,
        input_variables=["context", "query"]
    )


def get_disease_info_prompt() -> PromptTemplate:
    return PromptTemplate(
        template=DISEASE_INFO_TEMPLATE,
        input_variables=["context", "query"]
    )


def get_general_medical_prompt() -> PromptTemplate:
    return PromptTemplate(
        template=GENERAL_MEDICAL_TEMPLATE,
        input_variables=["context", "query"]
    )


def get_chat_prompt() -> ChatPromptTemplate:
    system_message = SystemMessagePromptTemplate.from_template(
        MEDICAL_ASSISTANT_SYSTEM_PROMPT
    )
    
    human_message = HumanMessagePromptTemplate.from_template(
        SYMPTOM_ANALYSIS_TEMPLATE
    )
    
    return ChatPromptTemplate.from_messages([
        system_message,
        human_message
    ])