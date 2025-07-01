"""
Structured Prompts Module
Template-based prompt engineering for consistent LLM outputs
"""

class StructuredPrompts:
    """SGLang-style structured prompts"""

    @staticmethod
    def document_analysis_prompt(chunk: str, query: str) -> str:
        """Structured prompt for document analysis"""
        return f"""TASK: Document Relevance Analysis\nQUERY: {query}\nDOCUMENT: {chunk}\n\nANALYSIS:\n1. Relevance Score (1-10): \n2. Key Information: \n3. Reasoning: \n\nFORMAT: SCORE:|score| INFO:|key_info| REASON:|reasoning|"""

    @staticmethod
    def structured_rag_prompt(query: str, context: str) -> str:
        """SGLang-style structured RAG prompt"""
        return f"""SYSTEM: You are a helpful AI assistant providing structured, accurate responses.\n\nTASK: Answer the user's question using the provided context.\n\nQUERY: {query}\n\nCONTEXT:\n{context}\n\nRESPONSE FORMAT:\n1. DIRECT ANSWER: [Provide a clear, direct answer]\n2. SUPPORTING EVIDENCE: [Quote relevant parts from context]\n3. CONFIDENCE LEVEL: [High/Medium/Low based on context quality]\n\nANSWER:"""

    @staticmethod
    def multi_perspective_prompt(query: str, context: str, perspective: str) -> str:
        """Generate prompt for specific perspective analysis"""
        perspective_instructions = {
            "technical": "Focus on technical implementation, architecture, and specifications.",
            "business": "Focus on business impact, costs, benefits, and strategic considerations.",
            "user": "Focus on user experience, usability, and practical applications.",
        }
        instructions = perspective_instructions.get(perspective, "Provide a general analysis.")
        return f"""SYSTEM: {instructions}\n\nTASK: Analyze the query from a {perspective} perspective.\n\nQUERY: {query}\n\nCONTEXT:\n{context}\n\nRESPONSE FORMAT:\n1. PERSPECTIVE ANALYSIS: [Detailed analysis]\n2. KEY POINTS: [List key points]\n3. RISKS/OPPORTUNITIES: [If any]\n\nANALYSIS:"""

    @staticmethod
    def synthesis_prompt(query: str, perspectives: dict) -> str:
        """Prompt to synthesize multiple perspectives into a single answer"""
        formatted = "\n\n".join([f"{k.upper()} PERSPECTIVE:\n{v}" for k, v in perspectives.items()])
        return f"""SYSTEM: Synthesize the following perspectives into a single, well-rounded answer.\n\nQUERY: {query}\n\nPERSPECTIVES:\n{formatted}\n\nSYNTHESIZED ANSWER:"""
