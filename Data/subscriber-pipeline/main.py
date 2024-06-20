import sqlite3
import pandas as pd
import json
import unittest
import logging
import os

logging.basicConfig(filename='logs/data_pipeline.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

def log_update(message):
    logging.info(message)

def log_error(message):
    logging.error(message)

def extract_contact_info(contact_info):
    try:
        info = json.loads(contact_info.replace("'", '"'))
        return pd.Series([info.get('mailing_address'), info.get('email')])
    except json.JSONDecodeError:
        return pd.Series([None, None])

def is_database_updated():
    global last_mod_time
    current_mod_time = os.path.getmtime(db_path)
    if last_mod_time is None or current_mod_time > last_mod_time:
        last_mod_time = current_mod_time
        return True
    return False

def write_changelog(version, new_rows_count, missing_data_count):
    with open(changelog_path, 'a') as f:
        f.write(f"Version: {version}\n")
        f.write(f"New rows added: {new_rows_count}\n")
        f.write(f"Missing data count: {missing_data_count}\n")
        f.write("\n")

try:
    db_path = 'dev/cademycode.db'
    changelog_path = 'logs/changelog.txt'
    last_mod_time = None

    if is_database_updated():
        log_update("Updated database. Running the pipeline...")

        con = sqlite3.connect(db_path)
        print('Database connection established successfully.')

        tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", con)
        table_names = tables['name'].tolist()
        df = {table: pd.read_sql_query(f"SELECT * FROM {table}", con) for table in table_names}

        students_df = df['cademycode_students'].copy()
        students_df['dob'] = pd.to_datetime(students_df['dob'], errors='coerce')
        students_df['job_id'] = pd.to_numeric(students_df['job_id'], errors='coerce')
        students_df['num_course_taken'] = pd.to_numeric(students_df['num_course_taken'], errors='coerce')
        students_df['current_career_path_id'] = pd.to_numeric(students_df['current_career_path_id'], errors='coerce')
        students_df['time_spent_hrs'] = pd.to_numeric(students_df['time_spent_hrs'], errors='coerce')
        students_df.loc[:, 'job_id'] = students_df['job_id'].fillna(0)
        students_df.loc[:, 'current_career_path_id'] = students_df['current_career_path_id'].fillna(0)
        students_df.loc[:, 'num_course_taken'] = students_df['num_course_taken'].fillna(students_df['num_course_taken'].median())
        students_df.loc[:, 'time_spent_hrs'] = students_df['time_spent_hrs'].fillna(students_df['time_spent_hrs'].median())
        students_df[['mailing_address', 'email']] = students_df['contact_info'].apply(extract_contact_info)
        students_df.drop(columns=['contact_info'], inplace=True)

        jobs_df_cleaned = df['cademycode_student_jobs'].drop_duplicates()

        merged_df_cleaned = pd.merge(students_df, jobs_df_cleaned, how='left', left_on='job_id', right_on='job_id')
        final_df_cleaned = pd.merge(merged_df_cleaned, df['cademycode_courses'], how='left', left_on='current_career_path_id', right_on='career_path_id')

        final_df_cleaned = final_df_cleaned.assign(
            career_path_id=final_df_cleaned['career_path_id'].fillna(0),
            career_path_name=final_df_cleaned['career_path_name'].fillna('Unknown'),
            hours_to_complete=final_df_cleaned['hours_to_complete'].fillna(0)
        )

        clean_db_conn = sqlite3.connect('dev/clean_cademycode.db')
        final_df_cleaned.to_sql('final_table', clean_db_conn, if_exists='replace', index=False)
        final_df_cleaned.to_csv('dev/final_output.csv', index=False)

        log_update("Pipeline executed successfully.")

        original_length = len(df['cademycode_students'])
        final_length = len(final_df_cleaned)

        class TestDataCleaning(unittest.TestCase):
            def test_no_null_values(self):
                self.assertFalse(final_df_cleaned.isnull().values.any(), "There are null values in the final table")

            def test_correct_number_of_rows(self):
                self.assertEqual(original_length, final_length, "The number of rows differs after the merges")

            def test_schema_consistency(self):
                original_schema = set(df['cademycode_students'].columns)
                final_schema = set(final_df_cleaned.columns)
                original_schema.discard('contact_info')
                original_schema.update(['mailing_address', 'email'])
                self.assertTrue(original_schema.issubset(final_schema), "The final table schema does not include all original columns")

        if __name__ == '__main__':
            unittest.main(argv=['first-arg-is-ignored'], exit=False)

        new_rows_count = len(final_df_cleaned) - original_length
        missing_data_count = final_df_cleaned.isnull().sum().sum()
        write_changelog("1.0.0", new_rows_count, missing_data_count)

    else:
        log_update("No updates to the database. Pipeline not executed.")

except Exception as e:
    log_error(f"Error running the pipeline: {e}")
    raise
