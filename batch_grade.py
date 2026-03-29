import csv
import subprocess
import concurrent.futures
import sys
import os

CSV_PATH = "Grading - HW1.csv"
REFERENCE_STUDENT = "Yujin Chen"
PROMPT_FILE = "efficient_grader_prompt.md"
CONCURRENCY = 5 
TASK_TIMEOUT = 600 

def run_grading_task(student_name, problem_id, base_prompt):
    prompt = (
        f"Use the grade-problem skill.\n\n"
        f"INSTRUCTIONS:\n{base_prompt}\n\n"
        f"PARAMETERS:\n"
        f"- Target Student: {student_name}\n"
        f"- Reference Student: {REFERENCE_STUDENT}\n"
        f"- Problem ID: {problem_id}\n"
        f"- Spreadsheet: {CSV_PATH}\n"
    )
    
    print(f"Starting: {student_name} - {problem_id}", flush=True)
    
    try:
        result = subprocess.run(
            ["gemini", "--prompt", prompt, "--yolo"],
            capture_output=True,
            text=True,
            timeout=TASK_TIMEOUT
        )
        if result.returncode == 0:
            print(f"✅ Finished: {student_name} - {problem_id}", flush=True)
        else:
            print(f"❌ Failed: {student_name} - {problem_id}", flush=True)
    except subprocess.TimeoutExpired:
        print(f"⏰ Timeout: {student_name} - {problem_id}", flush=True)
    except Exception as e:
        print(f"⚠️ Error: {student_name} - {problem_id} -> {e}", flush=True)

def main():
    limit = 10 # Default limit for this run
    if len(sys.argv) > 1:
        limit = int(sys.argv[1])

    if not os.path.exists(PROMPT_FILE):
        print(f"Error: {PROMPT_FILE} not found.", flush=True)
        sys.exit(1)
    
    with open(PROMPT_FILE, 'r') as f:
        base_prompt = f.read()

    try:
        with open(CSV_PATH, 'r', encoding='utf-8') as f:
            reader = list(csv.reader(f))
    except Exception as e:
        print(f"Failed to read CSV: {e}", flush=True)
        sys.exit(1)

    all_headers = reader[1]
    problem_cols = {pid: j for j, pid in enumerate(all_headers) if j >= 6 and pid.strip() and pid not in ["TOTAL HW1", "%HW1"]}
    
    tasks = []
    for i in range(5, len(reader)):
        row = reader[i]
        if len(row) > 2 and row[1].strip() and row[2].strip():
            student_name = f"{row[1].strip()} {row[2].strip()}"
            for pid, col_idx in problem_cols.items():
                current_val = row[col_idx].strip() if col_idx < len(row) else ""
                if not current_val:
                    tasks.append((student_name, pid))

    if not tasks:
        print("All problems are already graded!", flush=True)
        return

    # Apply limit
    tasks = tasks[:limit]

    print(f"Running {len(tasks)} tasks with concurrency {CONCURRENCY}...", flush=True)
    print("-" * 40, flush=True)

    with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
        futures = [executor.submit(run_grading_task, s, p, base_prompt) for s, p in tasks]
        for _ in concurrent.futures.as_completed(futures):
            pass

    print("-" * 40, flush=True)
    print("Batch completed!", flush=True)

if __name__ == "__main__":
    main()
