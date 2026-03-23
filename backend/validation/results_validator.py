"""
Results Validation System
Validates experimental results for scientific integrity
"""
from typing import List, Dict, Any, Optional
import json
import numpy as np
from scipy import stats
import warnings

class ResultsValidator:
    """
    Validates research results for common integrity issues
    Helps catch fabricated or suspicious data
    """
    
    def __init__(self):
        self.warnings_list = []
    
    def validate_results(self, results_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive validation of experimental results
        
        Args:
            results_data: Dictionary containing experimental results
            
        Returns:
            Dictionary with validation results and warnings
        """
        self.warnings_list = []
        checks = {
            "statistical_checks": self._check_statistics(results_data),
            "reproducibility_checks": self._check_reproducibility(results_data),
            "completeness_checks": self._check_completeness(results_data),
            "plausibility_checks": self._check_plausibility(results_data)
        }
        
        return {
            "status": "warning" if self.warnings_list else "passed",
            "warnings": self.warnings_list,
            "checks": checks,
            "overall_score": self._calculate_score(checks)
        }
    
    def _check_statistics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Check for statistical red flags"""
        issues = []
        
        # Check for results
        if "numerical_results" in data:
            results = data["numerical_results"]
            
            # Check 1: Too-perfect p-values (all < 0.001)
            if "p_values" in results:
                p_vals = results["p_values"]
                if isinstance(p_vals, list) and len(p_vals) > 0:
                    if all(p < 0.001 for p in p_vals):
                        issues.append("All p-values < 0.001 (suspiciously perfect)")
                        self.warnings_list.append("⚠️ Statistical anomaly: All p-values extremely low")
            
            # Check 2: Unrealistic effect sizes
            if "effect_sizes" in results:
                effects = results["effect_sizes"]
                if isinstance(effects, list) and len(effects) > 0:
                    if any(abs(e) > 3.0 for e in effects):  # Cohen's d > 3 is very rare
                        issues.append("Unusually large effect sizes detected")
                        self.warnings_list.append("⚠️ Effect sizes seem unrealistically large")
            
            # Check 3: Missing error measurements
            has_errors = any(k in results for k in ["std_dev", "confidence_intervals", "error_bars"])
            if not has_errors:
                issues.append("No error measurements found")
                self.warnings_list.append("⚠️ Missing error measurements (std dev, CI, etc.)")
        
        return {"passed": len(issues) == 0, "issues": issues}
    
    def _check_reproducibility(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Check for reproducibility indicators"""
        issues = []
        
        # Check for code/methodology details
        if "code_available" not in data or not data["code_available"]:
            issues.append("No code provided for reproducibility")
            self.warnings_list.append("⚠️ No code available for verification")
        
        # Check for random seed
        if "methodology" in data:
            method = str(data["methodology"]).lower()
            if "random" in method and "seed" not in method:
                issues.append("Uses randomness but no seed specified")
                self.warnings_list.append("⚠️ Random processes without fixed seed")
        
        # Check for dataset description
        if "dataset" not in data or not data["dataset"]:
            issues.append("Dataset not described")
            self.warnings_list.append("ℹ️ Dataset information missing")
        
        return {"passed": len(issues) == 0, "issues": issues}
    
    def _check_completeness(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Check if results are complete"""
        issues = []
        required_fields = ["methodology", "results", "sample_size"]
        
        for field in required_fields:
            if field not in data or not data[field]:
                issues.append(f"Missing: {field}")
                self.warnings_list.append(f"ℹ️ Missing required field: {field}")
        
        return {"passed": len(issues) == 0, "issues": issues}
    
    def _check_plausibility(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Check if results are plausible"""
        issues = []
        
        # Check sample size
        if "sample_size" in data:
            n = data["sample_size"]
            if isinstance(n, (int, float)):
                if n < 10:
                    issues.append("Very small sample size (n < 10)")
                    self.warnings_list.append("⚠️ Sample size is very small")
                elif n > 1000000:
                    issues.append("Unusually large sample size")
                    self.warnings_list.append("ℹ️ Very large sample size (verify)")
        
        # Check for perfect correlations
        if "correlations" in data:
            corrs = data["correlations"]
            if isinstance(corrs, list) and any(abs(c) > 0.99 for c in corrs):
                issues.append("Near-perfect correlation detected")
                self.warnings_list.append("⚠️ Correlation suspiciously close to 1.0")
        
        return {"passed": len(issues) == 0, "issues": issues}
    
    def _calculate_score(self, checks: Dict[str, Any]) -> float:
        """
        Calculate overall validation score (0-1)
        1.0 = perfect, 0.0 = many issues
        """
        total_checks = len(checks)
        passed_checks = sum(1 for check in checks.values() if check["passed"])
        return passed_checks / total_checks if total_checks > 0 else 0.0


def validate_notebook_results(notebook_path: str) -> Dict[str, Any]:
    """
    Parse and validate results from Jupyter notebook
    
    Args:
        notebook_path: Path to .ipynb file
        
    Returns:
        Validation results
    """
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        # Extract results from cells
        results_data = {
            "code_available": True,
            "methodology": "",
            "numerical_results": {},
            "source": "jupyter_notebook"
        }
        
        # Parse cells for results
        for cell in notebook.get("cells", []):
            if cell.get("cell_type") == "code":
                # Found code - good for reproducibility
                source = "".join(cell.get("source", []))
                results_data["methodology"] += source + "\n"
            
            elif cell.get("cell_type") == "markdown":
                # Check for results description
                content = "".join(cell.get("source", []))
                if any(keyword in content.lower() for keyword in ["result", "finding", "conclusion"]):
                    results_data["results"] = content
        
        # Validate
        validator = ResultsValidator()
        return validator.validate_results(results_data)
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "warnings": [f"❌ Failed to parse notebook: {str(e)}"]
        }


def validate_csv_results(csv_data: str) -> Dict[str, Any]:
    """
    Validate results from CSV file
    
    Args:
        csv_data: CSV content as string
        
    Returns:
        Validation results
    """
    try:
        import csv
        from io import StringIO
        
        reader = csv.DictReader(StringIO(csv_data))
        rows = list(reader)
        
        # Extract numerical columns
        numerical_results = {}
        for col in rows[0].keys():
            try:
                values = [float(row[col]) for row in rows if row[col]]
                numerical_results[col] = {
                    "values": values,
                    "mean": np.mean(values),
                    "std": np.std(values),
                    "n": len(values)
                }
            except (ValueError, KeyError):
                continue
        
        results_data = {
            "numerical_results": numerical_results,
            "sample_size": len(rows),
            "source": "csv_file"
        }
        
        validator = ResultsValidator()
        return validator.validate_results(results_data)
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "warnings": [f"❌ Failed to parse CSV: {str(e)}"]
        }
