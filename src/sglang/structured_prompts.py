"""
Structured Prompts Module
Template-based prompt engineering for consistent LLM outputs
"""


class StructuredPrompts:
    """SGLang-style structured prompts"""
    
    @staticmethod
    def document_analysis_prompt(chunk: str, query: str) -> str:
        """Structured prompt for document analysis"""
        return f"""TASK: Document Relevance Analysis
QUERY: {query}
DOCUMENT: {chunk}

ANALYSIS:
1. Relevance Score (1-10): 
2. Key Information: 
3. Reasoning: 

FORMAT: SCORE:|score| INFO:|key_info| REASON:|reasoning|"""

    @staticmethod
    def structured_rag_prompt(query: str, context: str) -> str:
        """SGLang-style structured RAG prompt"""
        return f"""SYSTEM: You are a helpful AI assistant providing structured, accurate responses.

TASK: Answer the user's question using the provided context.

QUERY: {query}

CONTEXT:
{context}

RESPONSE FORMAT:
1. DIRECT ANSWER: [Provide a clear, direct answer]
2. SUPPORTING EVIDENCE: [Quote relevant parts from context]
3. CONFIDENCE LEVEL: [High/Medium/Low based on context quality]

ANSWER:"""

    @staticmethod
    def multi_perspective_prompt(query: str, context: str, perspective: str) -> str:
        """Generate prompt for specific perspective analysis"""
        perspective_instructions = {
            "technical": "Focus on technical implementation, architecture, and specifications.",
            "business": "Focus on business impact, costs, benefits, and strategic considerations.", 
            "user": "Focus on user experience, usability, and practical applications."
        }
        
        instruction = perspective_instructions.get(perspective, "Provide a general analysis.")
        
        return f"""PERSPECTIVE: {perspective.upper()} ANALYSIS

INSTRUCTION: {instruction}

QUERY: {query}

CONTEXT: {context}

ANALYSIS FROM {perspective.upper()} PERSPECTIVE:"""

    @staticmethod
    def synthesis_prompt(query: str, perspectives: dict) -> str:
        """Synthesize multiple perspectives into comprehensive answer"""
        perspective_text = "\n\n".join([
            f"{name.upper()} PERSPECTIVE:\n{content}" 
            for name, content in perspectives.items()
        ])
        
        return f"""TASK: Synthesize multiple perspectives into a comprehensive answer

QUERY: {query}

DIFFERENT PERSPECTIVES:
{perspective_text}

INSTRUCTIONS:
1. Combine insights from all perspectives
2. Identify common themes and differences
3. Provide a balanced, comprehensive answer
4. Highlight any conflicting viewpoints

SYNTHESIZED RESPONSE:"""

    @staticmethod
    def evaluation_prompt(query: str, answer: str, context: str) -> str:
        """Prompt for evaluating answer quality"""
        return f"""TASK: Evaluate the quality of this RAG response

QUERY: {query}

GENERATED ANSWER: {answer}

SOURCE CONTEXT: {context}

EVALUATION CRITERIA:
1. ACCURACY: How well does the answer match the context?
2. COMPLETENESS: Does it fully address the query?
3. CLARITY: Is it clear and well-structured?
4. RELEVANCE: How relevant is the response to the query?

EVALUATION:
- Accuracy Score (1-10):
- Completeness Score (1-10): 
- Clarity Score (1-10):
- Relevance Score (1-10):
- Overall Score (1-10):
- Comments:"""
