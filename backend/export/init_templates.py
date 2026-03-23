"""
Initialize LaTeX templates
Run this to create default templates
"""
from pathlib import Path

def create_default_templates():
    """
    Create default LaTeX templates
    """
    templates_dir = Path(__file__).parent / "templates"
    templates_dir.mkdir(exist_ok=True)
    
    # IEEE Conference Template
    ieee_template = r"""\documentclass[conference]{IEEEtran}
\usepackage{amsmath}
\usepackage{graphicx}
\usepackage{cite}
\usepackage{hyperref}

\title{ {{- title -}} }
\author{
\IEEEauthorblockN{ {{- author -}} }
\IEEEauthorblockA{ {{- affiliation -}} \\
Email: {{- email -}} }
}

\begin{document}

\maketitle

\begin{abstract}
{{- abstract -}}
\end{abstract}

\begin{IEEEkeywords}
{% for keyword in keywords %}{{- keyword -}}{% if not loop.last %}, {% endif %}{% endfor %}
\end{IEEEkeywords}

{% if sections.introduction %}
\section{Introduction}
{{- sections.introduction -}}
{% endif %}

{% if sections.related_work %}
\section{Related Work}
{{- sections.related_work -}}
{% endif %}

{% if sections.methodology %}
\section{Methodology}
{{- sections.methodology -}}
{% endif %}

{% if sections.results %}
\section{Results}
{{- sections.results -}}
{% endif %}

{% if sections.discussion %}
\section{Discussion}
{{- sections.discussion -}}
{% endif %}

{% if sections.conclusion %}
\section{Conclusion}
{{- sections.conclusion -}}
{% endif %}

\bibliographystyle{IEEEtran}
\begin{thebibliography}{1}
\end{thebibliography}

\end{document}
"""
    
    # Generic Article Template
    generic_template = r"""\documentclass{article}
\usepackage{amsmath}
\usepackage{graphicx}
\usepackage{cite}
\usepackage{hyperref}

\title{ {{- title -}} }
\author{ {{- author -}} }
\date{\today}

\begin{document}

\maketitle

\begin{abstract}
{{- abstract -}}
\end{abstract}

\section*{Keywords}
{% for keyword in keywords %}{{- keyword -}}{% if not loop.last %}, {% endif %}{% endfor %}

{% if sections.introduction %}
\section{Introduction}
{{- sections.introduction -}}
{% endif %}

{% if sections.related_work %}
\section{Related Work}
{{- sections.related_work -}}
{% endif %}

{% if sections.methodology %}
\section{Methodology}
{{- sections.methodology -}}
{% endif %}

{% if sections.results %}
\section{Results}
{{- sections.results -}}
{% endif %}

{% if sections.discussion %}
\section{Discussion}
{{- sections.discussion -}}
{% endif %}

{% if sections.limitations %}
\section{Limitations}
{{- sections.limitations -}}
{% endif %}

{% if sections.conclusion %}
\section{Conclusion}
{{- sections.conclusion -}}
{% endif %}

{% if sections.future_work %}
\section{Future Work}
{{- sections.future_work -}}
{% endif %}

\bibliographystyle{plain}
\bibliography{references}

\end{document}
"""
    
    # Save templates
    (templates_dir / "ieee_conference.tex").write_text(ieee_template, encoding='utf-8')
    (templates_dir / "generic_article.tex").write_text(generic_template, encoding='utf-8')
    
    print(f"✓ Created LaTeX templates in {templates_dir}")
    print(f"  - ieee_conference.tex")
    print(f"  - generic_article.tex")

if __name__ == "__main__":
    create_default_templates()
