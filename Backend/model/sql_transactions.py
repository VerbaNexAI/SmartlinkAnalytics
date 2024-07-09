import os
import pyodbc
import pandas as pd
from fastapi import HTTPException
from typing import List, Dict
from transformers import pipeline
from huggingface_hub import login
from config.data_connection import DataConnection




class SQLTransactions:

    def __init__(self):
        connection = DataConnection()
        self.access_token = os.getenv('ACCESS_TOKEN')
        self.cursor = connection.cursor
        login(token=self.access_token)

    @staticmethod
    def read_sql_file(file_path: str) -> str:
        """
        Reads the contents of a SQL file.

        :param file_path: Path to the SQL file.
        :type file_path: str
        :returns: Content of the SQL file.
        :rtype: str
        """
        with open(file_path, 'r') as file:
            return file.read()

    def get_active_projects(self):
        if not self.cursor:
            raise HTTPException(
                status_code=500, detail="Could not connect to the database")
        try:
            sql_query = self.read_sql_file(r'config\data\project-active.sql')

            self.cursor.execute(sql_query)
            rows = self.cursor.fetchall()
            columns = [column[0] for column in self.cursor.description]
            projects = [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error executing the query: {str(e)}"
        )

        return projects
    
    def get_view_data(self) -> List[Dict]:
        """
        Retrieve view data from the database or create the view if it does not exist.

        :returns: A list of data from the view.
        :rtype: List[Dict]
        :raises HTTPException: If there is an issue connecting to the database or executing queries.
        """
        if not self.cursor:
            raise HTTPException(status_code=500, detail="Could not connect to the database")
        try:
            sql_query = self.read_sql_file(r'config\data\view.sql')
            
            self.cursor.execute(sql_query)
            rows = self.cursor.fetchall()
            columns = [column[0] for column in self.cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error executing the query: {str(e)}")
        

    def get_project(self) -> List[Dict]:
        """
        Retrieve projects from the database based on project name.

        :param project_name: The name of the project to retrieve.
        :type project_name: str
        :returns: A list of projects matching the project name.
        :rtype: List[Dict]
        :raises HTTPException: If there is an issue connecting to the database or executing queries.
        """
        if not self.cursor:
            raise HTTPException(status_code=500, detail="Could not connect to the database")
        
        try:
            sql_query = self.read_sql_file(r'config\data\project.sql')
            self.cursor.execute(sql_query)
            columns = [column[0] for column in self.cursor.description]
            projects = [dict(zip(columns, row)) for row in self.cursor.fetchall()]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error executing the query: {str(e)}")
        return projects

    async def get_inactive_projects_from_db(self) -> List[Dict]:
        """
        Retrieve inactive projects from the database asynchronously.

        :returns: A list of inactive projects.
        :rtype: List[Dict]
        :raises HTTPException: If there is an issue connecting to the database or executing queries.
        """
        if not self.connection:
            raise HTTPException(
                status_code=500, detail="Could not connect to the database"
            )

        try:
            sql_query = self.read_sql_file(r'SmartlinkAnalytics\Backend\config\data\project-inactve.sql')
            self.cursor.execute(sql_query)
            rows = self.cursor.fetchall()
            columns = [column[0] for column in self.cursor.description]
            projects = [dict(zip(columns, row)) for row in rows]
            return projects
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error executing the query: {str(e)}"
            )

    def create_text_label_df(self, result: List[Dict]) -> List[Dict]:
        """
        Convert the result data into a DataFrame, create text and label columns, and classify text.

        :param result: The result data to process.
        :type result: List[Dict]
        :returns: Predictions from the text classification model.
        :rtype: List[Dict]
        """
        df = pd.DataFrame(result)
        df['text'] = df.apply(lambda row: ' '.join(f"{key}:{row[key]}" for key in row.keys() if key != 'InconsistencyType'), axis=1)
        df['label'] = df['InconsistencyType'].apply(str)
        data = df[['text', 'label']]
        data.loc[:, 'text'] = data['text'].astype(str)
        text_list = data['text'].to_list()
        classifier = pipeline("text-classification", model="JeisonJA/distilbert-pid-smartlink-V2", tokenizer="distilbert-base-cased")
        prediction = classifier(text_list)
        print(prediction)
        return prediction


