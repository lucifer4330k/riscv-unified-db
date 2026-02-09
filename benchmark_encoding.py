
import time
import random
import string

def generate_dummy_data(n):
    instr_dict = {}
    # Use consistent seed for reproducibility
    random.seed(42)
    for _ in range(n):
        name = "".join(random.choices(string.ascii_lowercase, k=10)) + "." + "".join(random.choices(string.ascii_lowercase, k=3))
        match = hex(random.randint(0, 2**32))
        mask = hex(random.randint(0, 2**32))
        instr_dict[name] = {"match": match, "mask": mask}
    return instr_dict

def original_loop(instr_dict):
    start_time = time.time()
    mask_match_str = ""
    for i in sorted(instr_dict.keys()):
        mask_match_str += f"#define MATCH_{i.upper().replace('.', '_')} {instr_dict[i]['match']}\n"
        mask_match_str += f"#define MASK_{i.upper().replace('.', '_')} {instr_dict[i]['mask']}\n"
    end_time = time.time()
    return end_time - start_time, len(mask_match_str), mask_match_str

def optimized_loop(instr_dict):
    start_time = time.time()
    lines = []
    for i in sorted(instr_dict.keys()):
        lines.append(f"#define MATCH_{i.upper().replace('.', '_')} {instr_dict[i]['match']}\n")
        lines.append(f"#define MASK_{i.upper().replace('.', '_')} {instr_dict[i]['mask']}\n")
    mask_match_str = "".join(lines)
    end_time = time.time()
    return end_time - start_time, len(mask_match_str), mask_match_str

def main():
    n = 20000
    print(f"Generating {n} dummy instructions...")
    instr_dict = generate_dummy_data(n)

    print("Running original loop...")
    orig_time, orig_len, orig_str = original_loop(instr_dict)
    print(f"Original time: {orig_time:.4f}s")

    print("Running optimized loop...")
    opt_time, opt_len, opt_str = optimized_loop(instr_dict)
    print(f"Optimized time: {opt_time:.4f}s")

    if orig_len != opt_len:
        print(f"ERROR: Length mismatch! {orig_len} vs {opt_len}")
    elif orig_str != opt_str:
        print(f"ERROR: Content mismatch!")
    else:
        print("Lengths and content match.")

    print(f"Speedup: {orig_time / opt_time:.2f}x")

if __name__ == "__main__":
    main()
