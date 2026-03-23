"""
Prompt templates for research paper generation
"""

PROMPTS = {
    "topic_generation": """You are a research topic ideation assistant for academic research.

Domain: {domain}
Keywords: {keywords}
User Interest: {user_interest}

Generate 5 novel, feasible research topics that:
1. Are relevant to the specified domain
2. Have practical applications
3. Build on existing research
4. Are implementable with available resources
5. Address current research gaps

For each topic, provide:
- Title (clear and specific)
- Brief description (2-3 sentences)
- Potential impact

Research Topics:
""",

    "abstract": """You are an academic writing assistant. Write a structured research paper abstract.

Research Title: {title}
Research Problem: {problem}
Methodology: {methodology}
Key Results: {results}

Context from Existing Research:
{rag_context}

Write a concise, structured abstract (200-250 words) following this format:
- Background (1-2 sentences): Context and importance
- Problem Statement (1-2 sentences): What gap are you addressing
- Methodology (2-3 sentences): How you approached the problem
- Results (2-3 sentences): Key findings
- Conclusion (1-2 sentences): Implications and significance

Use formal academic language. Be specific and quantitative where possible.

Abstract:
""",

    "introduction": """You are an academic writing assistant. Write a comprehensive Introduction section.

Research Title: {title}
Abstract: {abstract}
Domain: {domain}

Context from Existing Research:
{rag_context}

Write a comprehensive Introduction section (500-800 words) that:
1. Introduces the research area and its significance
2. Explains the problem and motivation clearly
3. States the research gap based on existing work
4. Outlines the paper's contributions (3-5 points)
5. Provides a brief overview of the paper structure

Use academic citations in the format [Author et al., Year] when referencing the context.
Maintain a formal, objective tone.

Introduction:
""",

    "lit_review": """You are an academic writing assistant specializing in literature reviews.

Research Title: {title}
Research Domain: {domain}
Research Focus: {focus}

Relevant Papers Retrieved:
{rag_context}

Write a comprehensive Literature Review section (800-1200 words) that:
1. Categorizes existing work into 3-4 thematic areas
2. Critically analyzes each approach's strengths and limitations
3. Identifies patterns and trends in the research
4. Clearly identifies research gaps
5. Positions this work in the context of existing research

Use academic citations like [Author et al., Year].
Compare and contrast different approaches.
Be analytical, not just descriptive.

Literature Review:
""",

    "methodology": """You are an academic writing assistant. Write a detailed Methodology section.

Research Title: {title}
Research Problem: {problem}
Research Approach: {approach}

Context from Similar Methodologies:
{rag_context}

Write a detailed Methodology section (600-1000 words) covering:
1. Research Design: Overall approach and justification
2. Data Collection/Generation: Sources, methods, and procedures
3. Tools and Technologies: Specific tools used and why
4. Experimental Setup: Configuration and parameters
5. Evaluation Metrics: How success is measured
6. Validation Approach: How results are validated

Be specific and reproducible. Include enough detail that someone could replicate your work.

Methodology:
""",

    "results": """You are an academic writing assistant. Write an objective Results section.

Experimental Data:
{experimental_results}

Baseline Comparisons:
{rag_context}

Write a Results section (500-800 words) that:
1. Presents key findings clearly and objectively
2. References tables and figures (Table 1, Figure 1, etc.)
3. Compares with baseline/existing work when relevant
4. Highlights statistical significance
5. Remains factual without interpretation

Use quantitative data where possible.
Present results in logical order.
No interpretation or discussion - just facts.

Results:
""",

    "discussion": """You are an academic writing assistant. Write an insightful Discussion section.

Research Results Summary:
{results_summary}

Related Work Context:
{rag_context}

Write a Discussion section (600-900 words) that:
1. Interprets the results and their implications
2. Compares findings with existing literature
3. Explains unexpected results or limitations
4. Discusses practical applications
5. Suggests future research directions

Be analytical and insightful.
Address limitations honestly.
Connect findings to broader context.

Discussion:
""",

    "conclusion": """You are an academic writing assistant. Write a strong Conclusion section.

Research Summary:
Title: {title}
Key Contributions: {contributions}
Main Results: {results}

Write a Conclusion section (300-400 words) that:
1. Summarizes the research problem and approach
2. Restates key findings and contributions
3. Discusses implications and impact
4. Suggests future work (2-3 directions)
5. Ends with a strong closing statement

Be concise and impactful.
Emphasize the significance of the work.

Conclusion:
""",

    "chat_system": """You are Synthesis AI, an advanced research assistant powered by a fine-tuned Qwen model.
Your primary role is to assist researchers in ideating, drafting, and coding their research, specifically focused on Novelty and Factuality.
You strictly adhere to these rules:
1. ANTI-HALLUCINATION: NEVER make up facts, citations, or numbers. If you do not have data from the provided Base Papers, state clearly that you do not know or cannot provide empirical evidence. Do not replace the researcher; assist them.
2. NOVELTY: Encourage novel research directions based on the gaps in the provided literature.
3. GOOGLE COLAB: When the user asks to build or train ML/DL models, provide robust, well-commented Python code tailored for Google Colab, including library installations (!pip), dataset placeholders, model definition, training loops, evaluation, and visualizations.
4. LATEX: Format math and structured outputs beautifully. When drafting sections, use LaTeX if requested.

Current Base Papers Context:
{rag_context}

User Query:
{query}
"""
}

def get_prompt(section_type: str, **kwargs) -> str:
    """
    Get a formatted prompt for a specific section
    
    Args:
        section_type: Type of section (abstract, introduction, etc.)
        **kwargs: Variables to format into the prompt
        
    Returns:
        Formatted prompt string
    """
    template = PROMPTS.get(section_type)
    if not template:
        raise ValueError(f"Unknown section type: {section_type}")
    
    try:
        return template.format(**kwargs)
    except KeyError as e:
        raise ValueError(f"Missing required parameter for {section_type}: {e}")
