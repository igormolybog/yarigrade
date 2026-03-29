import argparse
import csv
import sys
import re

def fuzzy_match(student_name, row):
    # Combine all text in the row to search for the student name
    row_text = " ".join(row).lower()
    name_parts = student_name.lower().split()
    
    # Check if all parts of the student name are in the row
    return all(part in row_text for part in name_parts)

def update_grade(csv_path, student_name, problem_id, score):
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = list(csv.reader(f))
    except Exception as e:
        print(f"Error reading {csv_path}: {e}")
        sys.exit(1)

    problem_col_idx = -1
    # Find the problem ID column (scan first 10 rows to be safe)
    for i in range(min(10, len(reader))):
        for j, cell in enumerate(reader[i]):
            if cell.strip() == problem_id:
                problem_col_idx = j
                break
        if problem_col_idx != -1:
            break
            
    if problem_col_idx == -1:
        print(f"Error: Problem ID '{problem_id}' not found in the first 10 rows of {csv_path}.")
        sys.exit(1)

    student_row_idx = -1
    # Find the student row
    for i, row in enumerate(reader):
        if fuzzy_match(student_name, row):
            student_row_idx = i
            break

    if student_row_idx == -1:
        print(f"Error: Student '{student_name}' not found in {csv_path}.")
        sys.exit(1)

    # Pad row if necessary (though usually well-formed)
    while len(reader[student_row_idx]) <= problem_col_idx:
        reader[student_row_idx].append("")

    reader[student_row_idx][problem_col_idx] = str(score)

    try:
        with open(csv_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(reader)
        print(f"Successfully updated score for {student_name} on problem {problem_id} to {score}.")
    except Exception as e:
        print(f"Error writing to {csv_path}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Update a grade in a CSV spreadsheet.')
    parser.add_argument('--csv_path', required=True, help='Path to the grading CSV')
    parser.add_argument('--student', required=True, help='Name of the student')
    parser.add_argument('--problem_id', required=True, help='Problem ID (must match a column header exactly)')
    parser.add_argument('--score', required=True, help='Score to record')
    
    args = parser.parse_args()
    update_grade(args.csv_path, args.student, args.problem_id, args.score)
