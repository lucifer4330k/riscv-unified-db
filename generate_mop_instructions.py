#!/usr/bin/env python3
"""
Script to generate MOP instruction YAML files from layout templates.
This is a standalone script that emulates what the Rakefile does.
"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ZIMOP_DIR = os.path.join(BASE_DIR, "spec", "std", "isa", "inst", "Zimop")
ZCMOP_DIR = os.path.join(BASE_DIR, "spec", "std", "isa", "inst", "Zcmop")


def generate_mop_r_yaml(n: int) -> str:
    """Generate mop.r.{n} instruction YAML content."""
    # Original encoding for mop.r.n: 1-00--0111-------100-----1110011 (32 bits)
    # Let's break it down by bit positions (31 to 0):
    # Bit 31: 1 (fixed)
    # Bit 30: n[4] (variable)
    # Bits 29-28: 00 (fixed)
    # Bits 27-26: n[3:2] (variable)
    # Bits 25-22: 0111 (fixed)
    # Bits 21-20: n[1:0] (variable - BUT these map to bits 21-20, which are part of the 7-bit xs2/imm field)
    # Wait, let me re-analyze the original encoding:
    # 1-00--0111-------100-----1110011
    # Positions:
    # 31: 1
    # 30: - (n[4])
    # 29-28: 00
    # 27-26: -- (n[3:2])
    # 25-22: 0111
    # 21-15: ------- (7 bits for xs2[4:0] and bits 21-20 for n[1:0])
    # Actually looking at the original:
    #   - name: n
    #     location: 30|27-26|21-20
    # So n is spread across: bit 30, bits 27-26, and bits 21-20
    # The pattern 1-00--0111-------100-----1110011 has:
    # Position 31: 1
    # Position 30: -
    # Position 29-28: 00
    # Position 27-26: --
    # Position 25-22: 0111
    # Position 21-15: ------- (this is 7 bits but contains n[1:0] at 21-20!)
    # Position 14-12: 100
    # Position 11-7: ----- (rd)
    # Position 6-0: 1110011 (opcode)

    # For the individual instruction, we fix the n bits:
    bit_30 = (n >> 4) & 1  # n[4]
    bit_27 = (n >> 3) & 1  # n[3]
    bit_26 = (n >> 2) & 1  # n[2]
    bit_21 = (n >> 1) & 1  # n[1]
    bit_20 = n & 1  # n[0]

    # Build the 32-bit match string:
    # 31 30 29-28 27  26  25-22 21  20  19-15    14-12 11-7     6-0
    # 1  n4 00    n3  n2  0111  n1  n0  -----    100   -----    1110011
    match = f"1{bit_30}00{bit_27}{bit_26}0111{bit_21}{bit_20}-----100-----1110011"

    # Verify length
    assert len(match) == 32, f"Match pattern has {len(match)} bits, expected 32"

    return f"""# Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries.

# WARNING: This file is auto-generated from spec/std/isa/inst/Zimop/mop.r.N.layout

# SPDX-License-Identifier: BSD-3-Clause-Clear

# yaml-language-server: $schema=../../../../schemas/inst_schema.json

$schema: "inst_schema.json#"
kind: instruction
name: mop.r.{n}
long_name: May-be-operation {n} (1 source register)
description: |
  Unless redefined by another extension, this instruction simply writes 0 to X[xd].
  The encoding allows future extensions to define it to read X[xs1], as well as write X[xd].

  This is mop.r.{n} from the MOP.R instruction family (n={n}).
definedBy:
  extension:
    name: Zimop
assembly: xd, xs1
encoding:
  match: "{match}"
  variables:
    - name: xs1
      location: 19-15
    - name: xd
      location: 11-7
access:
  s: always
  u: always
  vs: always
  vu: always
data_independent_timing: false
operation(): |
  X[xd] = 0;
"""


def generate_mop_rr_yaml(n: int) -> str:
    """Generate mop.rr.{n} instruction YAML content."""
    # Original encoding for mop.rr.n: 1-00--1----------100-----1110011 (32 bits)
    # Variable 'n' is encoded in bits: 30|27-26
    # Bit 30: n[2], Bits 27-26: n[1:0]
    # Breakdown:
    # 31: 1
    # 30: - (n[2])
    # 29-28: 00
    # 27-26: -- (n[1:0])
    # 25: 1
    # 24-15: ---------- (10 bits for xs2 and xs1)
    # 14-12: 100
    # 11-7: ----- (rd)
    # 6-0: 1110011 (opcode)

    bit_30 = (n >> 2) & 1  # n[2]
    bit_27 = (n >> 1) & 1  # n[1]
    bit_26 = n & 1  # n[0]

    # Build the 32-bit match string:
    match = f"1{bit_30}00{bit_27}{bit_26}1----------100-----1110011"

    # Verify length
    assert len(match) == 32, f"Match pattern has {len(match)} bits, expected 32"

    return f"""# Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries.

# WARNING: This file is auto-generated from spec/std/isa/inst/Zimop/mop.rr.N.layout

# SPDX-License-Identifier: BSD-3-Clause-Clear

# yaml-language-server: $schema=../../../../schemas/inst_schema.json

$schema: "inst_schema.json#"
kind: instruction
name: mop.rr.{n}
long_name: May-be-operation {n} (2 source registers)
description: |
  The Zimop extension defines 8 MOP instructions named MOP.RR.n, where n is an integer between 0
  and 7, inclusive. Unless redefined by another extension, this instruction simply writes 0 to X[xd].
  Its encoding allows future extensions to define it to read X[xs1] and X[xs2], as well as write X[xd].

  This is mop.rr.{n} from the MOP.RR instruction family (n={n}).
definedBy:
  extension:
    name: Zimop
assembly: xd, xs1, xs2
encoding:
  match: "{match}"
  variables:
    - name: xs2
      location: 24-20
    - name: xs1
      location: 19-15
    - name: xd
      location: 11-7
access:
  s: always
  u: always
  vs: always
  vu: always
data_independent_timing: false
operation(): |
  X[xd] = 0;
"""


def generate_c_mop_yaml(n: int) -> str:
    """Generate c.mop.{n} instruction YAML content."""
    # c.mop.n instructions use odd numbers: 1, 3, 5, 7, 9, 11, 13, 15
    # Original encoding: 01100---10000001 (16 bits)
    # Bits 10-8 contain the index (0-7)
    # index = (n - 1) / 2
    index = (n - 1) // 2

    # Build the 16-bit match string
    bit_10 = (index >> 2) & 1
    bit_9 = (index >> 1) & 1
    bit_8 = index & 1
    match = f"01100{bit_10}{bit_9}{bit_8}10000001"

    # Verify length
    assert len(match) == 16, f"Match pattern has {len(match)} bits, expected 16"

    return f"""# Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries.

# WARNING: This file is auto-generated from spec/std/isa/inst/Zcmop/c.mop.N.layout

# SPDX-License-Identifier: BSD-3-Clause-Clear

# yaml-language-server: $schema=../../../../schemas/inst_schema.json

$schema: inst_schema.json#
kind: instruction
name: c.mop.{n}
long_name: Compressed May-Be-Operation {n}
description: |
  C.MOP.{n} is encoded in the reserved encoding space corresponding to C.LUI x{n}, 0.
  Unlike the MOPs defined in the Zimop extension, the C.MOP.n instructions are defined to not
  write any register. Their encoding allows future extensions to define them to read register x[{n}].

  This is c.mop.{n} from the compressed MOP instruction family.
definedBy:
  extension:
    name: Zcmop
assembly: ""
encoding:
  match: "{match}"
access:
  s: always
  u: always
  vs: always
  vu: always
data_independent_timing: false
operation(): "" #do nothing
"""


def main():
    # Generate MOP.R instructions (mop.r.0 through mop.r.31)
    print("Generating MOP.R instructions...")
    for n in range(32):
        filepath = os.path.join(ZIMOP_DIR, f"mop.r.{n}.yaml")
        content = generate_mop_r_yaml(n)
        with open(filepath, "w", newline="\n") as f:
            f.write(content)
        print(f"  Created {filepath}")

    # Generate MOP.RR instructions (mop.rr.0 through mop.rr.7)
    print("Generating MOP.RR instructions...")
    for n in range(8):
        filepath = os.path.join(ZIMOP_DIR, f"mop.rr.{n}.yaml")
        content = generate_mop_rr_yaml(n)
        with open(filepath, "w", newline="\n") as f:
            f.write(content)
        print(f"  Created {filepath}")

    # Generate C.MOP instructions (c.mop.1, c.mop.3, ..., c.mop.15)
    print("Generating C.MOP instructions...")
    for n in [1, 3, 5, 7, 9, 11, 13, 15]:
        filepath = os.path.join(ZCMOP_DIR, f"c.mop.{n}.yaml")
        content = generate_c_mop_yaml(n)
        with open(filepath, "w", newline="\n") as f:
            f.write(content)
        print(f"  Created {filepath}")

    print("\nGenerated 48 instruction files total:")
    print(f"  - 32 mop.r.N files in {ZIMOP_DIR}")
    print(f"  - 8 mop.rr.N files in {ZIMOP_DIR}")
    print(f"  - 8 c.mop.N files in {ZCMOP_DIR}")


if __name__ == "__main__":
    main()
