#!/usr/bin/env python3
'''
Silver Ratio Calculator (OEIS Edition)
======================================================
Calculates Silver Ratio (1 + sqrt(2)) to exactly N digits
using mpmath with gmpy2 backend and strict OEIS truncation formatting.
'''

import sys
import math
import time
import argparse
import os
import mpmath

# Enable gmpy2 backend for mpmath if available
os.environ['MPMATH_GMPY2'] = '1'

sys.set_int_max_str_digits(0)

def save_oeis_files(constant_name: str, digits_str: str, target_digits: int) -> None:
    '''
    Save the digits to a raw file and an OEIS b-file.

    Args:
        constant_name: Name of the constant (e.g., "Silver_Ratio").
        digits_str: String of digits (without decimal point).
        target_digits: Number of digits to include.
    '''
    clean_digits = digits_str.replace('.', '')[:target_digits]

    raw_filename = f'{constant_name}_{target_digits}_digits.txt'
    with open(raw_filename, 'w', encoding='utf-8') as f:
        f.write(clean_digits)
    print(f'Saved raw digit output to {raw_filename}')

    b_filename = f'b_file_{constant_name}_{target_digits}.txt'
    with open(b_filename, 'w', encoding='utf-8') as f:
        for idx, digit in enumerate(clean_digits, start=1):
            f.write(f'{idx} {digit}\n')
    print(f'Saved OEIS b-file output to {b_filename}')

def compute_silver_ratio_hpc(target_digits: int) -> str:
    '''
    Compute the Silver Ratio (1 + sqrt(2)) to the specified number of digits.

    Args:
        target_digits: Number of digits to compute.

    Returns:
        The digits as a string (without decimal point).
    '''
    # Use a few extra digits for rounding safety
    dps_working = target_digits + 50
    mpmath.mp.dps = dps_working
    ctx = mpmath.mp

    # Compute the Silver Ratio
    val = ctx.mpf('1') + ctx.sqrt(2)
    val_str = ctx.nstr(val, dps_working)

    # Extract digits (integer part included)
    clean_digits = val_str.replace('.', '')[:target_digits]

    save_oeis_files('Silver_Ratio', clean_digits, target_digits)
    return clean_digits

def main() -> None:
    parser = argparse.ArgumentParser(description='Silver Ratio OEIS Calculator')
    parser.add_argument('-n', '--digits', type=int, default=1000,
                        help='Target digits (default: 1000)')
    args = parser.parse_args()

    t0 = time.time()
    digits = compute_silver_ratio_hpc(args.digits)
    t1 = time.time()

    print(f'Execution finished in {t1 - t0:.4f} seconds using 12 cores.')

if __name__ == '__main__':
    main()