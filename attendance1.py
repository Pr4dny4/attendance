import pandas as pd
import re

# Function to validate email format
def is_valid_email(email):
    if pd.isna(email) or not isinstance(email, str):  # Handle NaN and non-string values
        return False
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(email_pattern, email))

# Function to process attendance data and generate messages for parents
def process_attendance(attendance_df, students_df):
    # Merge attendance data with student information
    merged_df = attendance_df.merge(students_df, on="student_id", how="left")

    # Fill missing parent emails with an empty string
    merged_df['parent_email'] = merged_df['parent_email'].fillna('')

    # Validate and filter out incorrect emails
    merged_df['email'] = merged_df['parent_email'].apply(lambda email: email if is_valid_email(email) else None)

    # Generate absence notification messages for parents
    def generate_message(row):
        if row['email']:  # Only generate messages if a valid email exists
            return (f"Dear Parent, your child {row['student_name']} was absent from "
                    f"{row['absence_start_date']} to {row['absence_end_date']} for "
                    f"{row['total_absent_days']} days. Please ensure their attendance improves.")
        return None

    merged_df['msg'] = merged_df.apply(generate_message, axis=1)

    # Select relevant columns for the final output
    return merged_df[['student_id', 'absence_start_date', 'absence_end_date', 'total_absent_days', 'email', 'msg']]

# Sample attendance records
attendance_data = {
    "student_id": [101, 102, 103],
    "absence_start_date": ["01-03-2024", "02-03-2024", "05-03-2024"],
    "absence_end_date": ["04-03-2024", "05-03-2024", "09-03-2024"],
    "total_absent_days": [4, 4, 5]
}

# Student details with parent email information
students_data = {
    "student_id": [101, 102],
    "student_name": ["Alice Johnson", "Bob Smith"],
    "parent_email": ["alice_parent@example.com", None]  # Simulating missing email
}

# Convert dictionaries to Pandas DataFrames
attendance_df = pd.DataFrame(attendance_data)
students_df = pd.DataFrame(students_data)

# Process data and display the result
final_result = process_attendance(attendance_df, students_df)
print(final_result)
