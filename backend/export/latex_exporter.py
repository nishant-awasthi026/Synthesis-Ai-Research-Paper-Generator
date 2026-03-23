"""
LaTeX Export System
Generates publication-ready LaTeX documents from research papers
"""
from typing import Dict, List, Any, Optional
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, Template
import os
import subprocess
import tempfile
import re

from backend.database.models import ResearchPaper, Citation


class LaTeXExporter:
    """Export research papers to LaTeX"""
    
    def __init__(self):
        self.templates_dir = Path(__file__).parent / "templates"
        self.templates_dir.mkdir(exist_ok=True)
        
        # Setup Jinja2 environment
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=False  # Don't escape LaTeX commands
        )
        
        # Add custom filters
        self.jinja_env.filters['latex_escape'] = self.latex_escape
    
    @staticmethod
    def latex_escape(text: str) -> str:
        """
        Escape special LaTeX characters
        """
        if not text:
            return ""
        
        # Characters that need escaping in LaTeX
        replacements = {
            '&': r'\&',
            '%': r'\%',
            '$': r'\$',
            '#': r'\#',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '~': r'\textasciitilde{}',
            '^': r'\textasciicircum{}',
            '\\': r'\textbackslash{}',
        }
        
        for char, replacement in replacements.items():
            text = text.replace(char, replacement)
        
        return text
    
    def export_to_latex(
        self,
        paper: ResearchPaper,
        citations: List[Citation],
        template: str = "ieee_conference"
    ) -> str:
        """
        Generate LaTeX document from paper
        
        Args:
            paper: ResearchPaper instance
            citations: List of citations
            template: Template name (ieee_conference, acm_conference, springer_lncs, generic_article)
            
        Returns:
            LaTeX document as string
        """
        # Prepare paper data
        paper_data = paper.paper_data or {}
        
        # Extract sections
        sections = {
            'abstract': paper_data.get('abstract', ''),
            'introduction': paper_data.get('introduction', ''),
            'related_work': paper_data.get('related_work', ''),
            'methodology': paper_data.get('methodology', ''),
            'results': paper_data.get('results', ''),
            'discussion': paper_data.get('discussion', ''),
            'conclusion': paper_data.get('conclusion', ''),
            'limitations': paper_data.get('limitations', ''),
            'future_work': paper_data.get('future_work', '')
        }
        
        # Format citations for LaTeX
        latex_citations = self.format_citations_latex(citations)
        
        # Prepare template data
        template_data = {
            'title': paper.title,
            'author': 'Author Name',  # TODO: Get from user
            'email': 'author@example.com',  # TODO: Get from user
            'affiliation': 'Institution',  # TODO: Get from user
            'abstract': sections['abstract'],
            'sections': sections,
            'citations': latex_citations,
            'keywords': paper_data.get('keywords', [])
        }
        
        # Load and render template
        try:
            template_obj = self.jinja_env.get_template(f"{template}.tex")
            latex_content = template_obj.render(**template_data)
            return latex_content
        except Exception as e:
            # Fallback to generic template
            return self._generate_generic_latex(template_data)
    
    def format_citations_latex(self, citations: List[Citation]) -> str:
        """
        Format citations as BibTeX entries
        """
        bibtex_entries = []
        
        for idx, citation in enumerate(citations):
            cite_key = f"ref{idx + 1}"
            
            # Extract citation metadata
            meta = citation.meta_data or {}
            
            # Generate BibTeX entry
            entry = f"""@article{{{cite_key},
    author = {{{meta.get('authors', 'Unknown')}}},
    title = {{{meta.get('title', citation.citation_text)}}},
    year = {{{meta.get('year', '2024')}}},
    journal = {{{meta.get('journal', 'Unknown')}}},
    doi = {{{citation.doi or ''}}}
}}"""
            bibtex_entries.append(entry)
        
        return '\n\n'.join(bibtex_entries)
    
    def _generate_generic_latex(self, data: Dict[str, Any]) -> str:
        """
        Generate generic LaTeX document (fallback)
        """
        sections_latex = []
        
        for section_name, content in data['sections'].items():
            if content:
                section_title = section_name.replace('_', ' ').title()
                sections_latex.append(f"\\section{{{section_title}}}\n{content}\n")
        
        latex = f"""\\documentclass{{article}}
\\usepackage{{amsmath}}
\\usepackage{{graphicx}}
\\usepackage{{cite}}
\\usepackage{{hyperref}}

\\title{{{data['title']}}}
\\author{{{data['author']}}}
\\date{{\\today}}

\\begin{{document}}

\\maketitle

\\begin{{abstract}}
{data['abstract']}
\\end{{abstract}}

{chr(10).join(sections_latex)}

\\bibliographystyle{{plain}}
\\bibliography{{references}}

\\end{{document}}
"""
        return latex
    
    def compile_to_pdf(self, latex_content: str, output_dir: Optional[str] = None) -> bytes:
        """
        Compile LaTeX to PDF using pdflatex
        
        Args:
            latex_content: LaTeX document string
            output_dir: Directory to save PDF (uses temp if None)
            
        Returns:
            PDF file content as bytes
            
        Raises:
            RuntimeError: If pdflatex is not available or compilation fails
        """
        # Check if pdflatex is available
        try:
            subprocess.run(['pdflatex', '--version'], 
                         capture_output=True, check=True, timeout=5)
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            raise RuntimeError(
                "pdflatex not found. Please install TeX Live or MiKTeX. "
                "Alternatively, use LaTeX-only export."
            )
        
        # Create temporary directory for compilation
        with tempfile.TemporaryDirectory() as tmpdir:
            tex_file = Path(tmpdir) / "paper.tex"
            
            # Write LaTeX file
            tex_file.write_text(latex_content, encoding='utf-8')
            
            # Run pdflatex (twice for references)
            for _ in range(2):
                try:
                    result = subprocess.run(
                        ['pdflatex', '-interaction=nonstopmode', 'paper.tex'],
                        cwd=tmpdir,
                        capture_output=True,
                        timeout=30
                    )
                except subprocess.TimeoutExpired:
                    raise RuntimeError("PDF compilation timed out")
            
            # Check if PDF was created
            pdf_file = Path(tmpdir) / "paper.pdf"
            if not pdf_file.exists():
                # Try to get error from log
                log_file = Path(tmpdir) / "paper.log"
                error_msg = "PDF compilation failed"
                if log_file.exists():
                    log_content = log_file.read_text()
                    # Extract error lines
                    error_lines = [l for l in log_content.split('\n') if '!' in l]
                    if error_lines:
                        error_msg += f": {error_lines[0]}"
                raise RuntimeError(error_msg)
            
            # Read PDF content
            pdf_content = pdf_file.read_bytes()
            
            # Optionally save to output directory
            if output_dir:
                output_path = Path(output_dir) / "paper.pdf"
                output_path.write_bytes(pdf_content)
            
            return pdf_content


def create_default_templates():
    """
    Create default LaTeX templates
    """
    templates_dir = Path(__file__).parent / "templates"
    templates_dir.mkdir(exist_ok=True)
    
    # IEEE Conference Template
    ieee_template = r"""
\documentclass[conference]{IEEEtran}
\usepackage{amsmath}
\usepackage{graphicx}
\usepackage{cite}
\usepackage{hyperref}

\title{ {{ title }} }
\author{
\IEEEauthorblockN{ {{ author }} }
\IEEEauthorblockA{ {{ affiliation }} \\
Email: {{ email }}}
}

\begin{document}

\maketitle

\begin{abstract}
{{ abstract }}
\end{abstract}

\begin{IEEEkeywords}
{% for keyword in keywords %}{{ keyword }}{% if not loop.last %}, {% endif %}{% endfor %}
\end{IEEEkeywords}

{% if sections.introduction %}
\section{Introduction}
{{ sections.introduction }}
{% endif %}

{% if sections.related_work %}
\section{Related Work}
{{ sections.related_work }}
{% endif %}

{% if sections.methodology %}
\section{Methodology}
{{ sections.methodology }}
{% endif %}

{% if sections.results %}
\section{Results}
{{ sections.results }}
{% endif %}

{% if sections.discussion %}
\section{Discussion}
{{ sections.discussion }}
{% endif %}

{% if sections.conclusion %}
\section{Conclusion}
{{ sections.conclusion }}
{% endif %}

\bibliographystyle{IEEEtran}
\begin{thebibliography}{1}
% Citations will be added here
\end{thebibliography}

\end{document}
"""
    
    # Generic Article Template
    generic_template = r"""
\documentclass{article}
\usepackage{amsmath}
\usepackage{graphicx}
\usepackage{cite}
\usepackage{hyperref}

\title{ {{ title }} }
\author{ {{ author }} }
\date{\today}

\begin{document}

\maketitle

\begin{abstract}
{{ abstract }}
\end{abstract}

{% if sections.introduction %}
\section{Introduction}
{{ sections.introduction }}
{% endif %}

{% if sections.related_work %}
\section{Related Work}
{{ sections.related_work }}
{% endif %}

{% if sections.methodology %}
\section{Methodology}
{{ sections.methodology }}
{% endif %}

{% if sections.results %}
\section{Results}
{{ sections.results }}
{% endif %}

{% if sections.discussion %}
\section{Discussion}
{{ sections.discussion }}
{% endif %}

{% if sections.limitations %}
\section{Limitations}
{{ sections.limitations }}
{% endif %}

{% if sections.conclusion %}
\section{Conclusion}
{{ sections.conclusion }}
{% endif %}

{% if sections.future_work %}
\section{Future Work}
{{ sections.future_work }}
{% endif %}

\bibliographystyle{plain}
\bibliography{references}

\end{document}
"""
    
    # Save templates
    (templates_dir / "ieee_conference.tex").write_text(ieee_template)
    (templates_dir / "generic_article.tex").write_text(generic_template)
    
    print(f"✓ Created LaTeX templates in {templates_dir}")


if __name__ == "__main__":
    # Create templates when run directly
    create_default_templates()
