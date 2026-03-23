"""
Results Parser Utilities
Parses experimental results from various file formats
"""
from typing import Dict, List, Any, Optional
import json
import csv
import io
import re
from pathlib import Path
import nbformat
from nbformat import NotebookNode


class ResultsParser:
    """Parse experimental results from different file formats"""
    
    def __init__(self):
        self.supported_formats = ['txt', 'csv', 'json', 'ipynb']
    
    def parse_file(self, file_path: str, file_type: str) -> Dict[str, Any]:
        """
        Parse file based on type
        
        Args:
            file_path: Path to file
            file_type: File extension (txt, csv, json, ipynb)
            
        Returns:
            Dictionary with parsed results
        """
        if file_type not in self.supported_formats:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        if file_type == 'txt':
            return self.parse_text_file(file_path)
        elif file_type == 'csv':
            return self.parse_csv_file(file_path)
        elif file_type == 'json':
            return self.parse_json_file(file_path)
        elif file_type == 'ipynb':
            return self.parse_notebook(file_path)
    
    def parse_text_file(self, file_path: str) -> Dict[str, Any]:
        """
        Parse plain text results file
        Extracts numerical values, statistics, and structured data
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        results = {
            'raw_text': content,
            'metrics': {},
            'statistics': {},
            'numerical_data': []
        }
        
        # Extract key-value pairs (e.g., "Accuracy: 95.2%")
        kv_pattern = r'(\w+(?:\s+\w+)*)\s*:\s*([\d.]+)(\s*%)?'
        matches = re.findall(kv_pattern, content)
        
        for key, value, percent in matches:
            key_clean = key.strip().lower().replace(' ', '_')
            val_num = float(value)
            if percent:
                val_num /= 100.0
            results['metrics'][key_clean] = val_num
        
        # Extract statistical terms (mean, std, p-value, etc.)
        stats_patterns = {
            'mean': r'mean\s*[=:]\s*([\d.]+)',
            'std': r'std(?:dev)?\s*[=:]\s*([\d.]+)',
            'variance': r'var(?:iance)?\s*[=:]\s*([\d.]+)',
            'p_value': r'p[-_]?value\s*[=:]\s*([\d.]+)',
            'confidence': r'(?:confidence|CI)\s*[=:]\s*([\d.]+)'
        }
        
        for stat_name, pattern in stats_patterns.items():
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                results['statistics'][stat_name] = float(match.group(1))
        
        # Extract all numbers for general analysis
        numbers = re.findall(r'\b\d+\.?\d*\b', content)
        results['numerical_data'] = [float(n) for n in numbers]
        
        return results
    
    def parse_csv_file(self, file_path: str) -> Dict[str, Any]:
        """
        Parse CSV results file
        Assumes first row is headers
        """
        results = {
            'columns': [],
            'data': [],
            'statistics': {}
        }
        
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            results['columns'] = reader.fieldnames
            
            for row in reader:
                results['data'].append(dict(row))
        
        # Calculate basic statistics for numerical columns
        if results['data']:
            for col in results['columns']:
                try:
                    values = [float(row[col]) for row in results['data'] if row[col]]
                    if values:
                        results['statistics'][col] = {
                            'count': len(values),
                            'mean': sum(values) / len(values),
                            'min': min(values),
                            'max': max(values)
                        }
                        
                        # Calculate std dev
                        mean = results['statistics'][col]['mean']
                        variance = sum((x - mean) ** 2 for x in values) / len(values)
                        results['statistics'][col]['std'] = variance ** 0.5
                except (ValueError, TypeError):
                    # Skip non-numerical columns
                    pass
        
        return results
    
    def parse_json_file(self, file_path: str) -> Dict[str, Any]:
        """
        Parse JSON results file
        Assumes top-level is results dictionary
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        results = {
            'raw_data': data,
            'metrics': {},
            'statistics': {}
        }
        
        # Extract metrics (any numerical values at top level)
        def extract_numbers(obj, prefix=''):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    new_prefix = f"{prefix}.{key}" if prefix else key
                    if isinstance(value, (int, float)):
                        results['metrics'][new_prefix] = value
                    elif isinstance(value, dict):
                        extract_numbers(value, new_prefix)
                    elif isinstance(value, list) and value and isinstance(value[0], (int, float)):
                        # Calculate stats for numerical arrays
                        results['statistics'][new_prefix] = {
                            'count': len(value),
                            'mean': sum(value) / len(value),
                            'min': min(value),
                            'max': max(value)
                        }
        
        extract_numbers(data)
        
        return results
    
    def parse_notebook(self, file_path: str) -> Dict[str, Any]:
        """
        Parse Jupyter notebook and extract results
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            notebook = nbformat.read(f, as_version=4)
        
        results = {
            'cells': [],
            'outputs': [],
            'code_cells': [],
            'markdown_cells': [],
            'results_data': {},
            'visualizations': []
        }
        
        # Extract code and outputs
        for cell_idx, cell in enumerate(notebook.cells):
            cell_data = {
                'index': cell_idx,
                'type': cell.cell_type,
                'source': cell.source
            }
            
            if cell.cell_type == 'code':
                results['code_cells'].append(cell_data)
                
                # Extract outputs
                if hasattr(cell, 'outputs'):
                    for output in cell.outputs:
                        output_data = {
                            'cell_index': cell_idx,
                            'output_type': output.output_type
                        }
                        
                        # Text/stream output
                        if output.output_type == 'stream':
                            output_data['text'] = output.text
                            results['outputs'].append(output_data)
                        
                        # Display data (plots, images)
                        elif output.output_type == 'display_data':
                            if 'image/png' in output.data:
                                output_data['type'] = 'image'
                                results['visualizations'].append(output_data)
                        
                        # Execution results
                        elif output.output_type == 'execute_result':
                            if 'text/plain' in output.data:
                                output_data['text'] = output.data['text/plain']
                                results['outputs'].append(output_data)
            
            elif cell.cell_type == 'markdown':
                results['markdown_cells'].append(cell_data)
        
        # Extract numerical results from outputs
        all_outputs_text = ' '.join([
            out.get('text', '') for out in results['outputs'] 
            if isinstance(out.get('text'), str)
        ])
        
        # Parse numbers from outputs
        numbers = re.findall(r'\b\d+\.?\d*\b', all_outputs_text)
        if numbers:
            results['results_data']['numerical_values'] = [float(n) for n in numbers]
        
        # Look for common result patterns
        metrics_pattern = r'(\w+)\s*[=:]\s*([\d.]+)'
        matches = re.findall(metrics_pattern, all_outputs_text)
        if matches:
            results['results_data']['metrics'] = {
                key.lower(): float(value) for key, value in matches
            }
        
        return results
    
    def extract_notebook_results(self, notebook_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract clean results summary from parsed notebook
        """
        summary = {
            'total_cells': len(notebook_data.get('cells', [])),
            'code_cells': len(notebook_data.get('code_cells', [])),
            'outputs_count': len(notebook_data.get('outputs', [])),
            'has_visualizations': len(notebook_data.get('visualizations', [])) > 0,
            'metrics': notebook_data.get('results_data', {}).get('metrics', {}),
            'numerical_summary': {}
        }
        
        # Get numerical summary
        nums = notebook_data.get('results_data', {}).get('numerical_values', [])
        if nums:
            summary['numerical_summary'] = {
                'count': len(nums),
                'mean': sum(nums) / len(nums),
                'min': min(nums),
                'max': max(nums)
            }
        
        return summary


class ColabNotebookHandler:
    """Handle Google Colab notebook URLs"""
    
    @staticmethod
    def parse_colab_url(url: str) -> Dict[str, Any]:
        """
        Parse Colab notebook URL to extract notebook ID
        
        Example URL formats:
        - https://colab.research.google.com/drive/NOTEBOOK_ID
        - https://colab.research.google.com/github/USER/REPO/blob/master/notebook.ipynb
        """
        result = {
            'url': url,
            'type': None,
            'id': None,
            'valid': False
        }
        
        if 'colab.research.google.com' in url:
            if '/drive/' in url:
                # Drive-based notebook
                match = re.search(r'/drive/([a-zA-Z0-9_-]+)', url)
                if match:
                    result['type'] = 'drive'
                    result['id'] = match.group(1)
                    result['valid'] = True
            
            elif '/github/' in url:
                # GitHub-based notebook
                result['type'] = 'github'
                result['valid'] = True
                result['github_url'] = url.replace(
                    'colab.research.google.com/github/',
                    'raw.githubusercontent.com/'
                ).replace('/blob/', '/')
        
        return result
    
    @staticmethod
    def get_download_url(notebook_id: str, notebook_type: str = 'drive') -> str:
        """
        Generate download URL for Colab notebook
        Note: This requires authentication for actual download
        """
        if notebook_type == 'drive':
            return f"https://drive.google.com/uc?export=download&id={notebook_id}"
        return None
