---
name: grade-problem
description: Grades a student's solution to a specific problem by visually comparing their work against a reference student's work and updates the grading spreadsheet. Use when asked to grade, evaluate, or compare a student's answer.
---

# Grade Problem Skill

This skill allows Gemini CLI to grade a student's submission for a specific problem by visually comparing it with a reference student's solution, and automatically updates the grading CSV spreadsheet. It is designed to be generic and works across different assignments and courses.

## Workflow

1.  **Identify Parameters**: From the user's prompt or the current context, identify:
    *   **Target Student Name**
    *   **Reference Student Name** (the example/gold standard student)
    *   **Problem ID**
    *   **Grading Spreadsheet Path** (e.g., `Grading - HW1.csv`)
2.  **Locate Submissions**:
    *   Find the target student's submission folder and read their solution for the problem (this could be inside code files or a PDF writeup).
    *   Find the reference student's folder and read their solution for the same problem.
3.  **Compare and Evaluate**:
    *   Visually and textually compare the target student's answer against the reference. Evaluate accuracy, completeness, and correctness.
    *   *Do NOT run tests or execute code.* Rely on visual inspection.
    *   Determine an appropriate score based on the comparison.
4.  **Record Score**:
    *   Execute the bundled Python script to update the spreadsheet:
        ```bash
        python <SKILL_DIR>/scripts/update_grade.py --csv_path "path/to/spreadsheet.csv" --student "Target Student Name" --problem_id "problem_id" --score "X"
        ```

## Notes
- The Python script automatically finds the correct column for the problem ID by searching the header rows.
- The script automatically finds the correct row for the target student using fuzzy matching.
