import importlib.util
import sys
import os
import tempfile
import subprocess
import mpmath

# Load the module
spec = importlib.util.spec_from_file_location('MODULE_FILENAME', 'MODULE_FILENAME')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_module_loads():
    assert hasattr(module, 'compute_silver_ratio_hpc')
    assert hasattr(module, 'save_oeis_files')
    assert hasattr(module, 'main')

def test_digits_correct():
    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            for n in [1, 2, 5, 10]:
                digits = module.compute_silver_ratio_hpc(n)
                # Compute expected using mpmath
                mpmath.mp.dps = n + 50
                val = mpmath.mpf('1') + mpmath.sqrt(2)
                val_str = mpmath.nstr(val, n + 50)
                expected = val_str.replace('.', '')[:n]
                assert digits == expected, f'Mismatch for n={n}: got {digits}, expected {expected}'
        finally:
            os.chdir(original_cwd)

def test_output_files():
    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            digits = module.compute_silver_ratio_hpc(5)
            # Check raw file
            raw_file = 'Silver_Ratio_5_digits.txt'
            assert os.path.exists(raw_file)
            with open(raw_file, 'r') as f:
                raw_content = f.read().strip()
            assert raw_content == digits
            # Check b-file
            b_file = 'b_file_Silver_Ratio_5.txt'
            assert os.path.exists(b_file)
            with open(b_file, 'r') as f:
                lines = f.readlines()
            assert len(lines) == 5
            for i, line in enumerate(lines, start=1):
                parts = line.strip().split()
                assert len(parts) == 2
                assert parts[0] == str(i)
                assert parts[1] == digits[i-1]
        finally:
            os.chdir(original_cwd)

def test_cli():
    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            result = subprocess.run([sys.executable, 'MODULE_FILENAME', '-n', '5'],
                                    capture_output=True, text=True)
            assert result.returncode == 0
            assert os.path.exists('Silver_Ratio_5_digits.txt')
            assert os.path.exists('b_file_Silver_Ratio_5.txt')
            assert 'Saved raw digit output to Silver_Ratio_5_digits.txt' in result.stdout
            assert 'Saved OEIS b-file output to b_file_Silver_Ratio_5.txt' in result.stdout
            assert 'Execution finished in' in result.stdout
            assert 'using 12 cores.' in result.stdout
        finally:
            os.chdir(original_cwd)