from airflow import DAG
from datetime import timedelta, datetime
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.task_group import TaskGroup
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.http.sensors.http import HttpSensor
import json
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook

from pythonCD import transform_load_data, loading, save_join_tbl_to_s3


#                            ---> create_table_1 --> truncate_table --> uploadS3_to_postgres_city ------------------------------------------------------------------------------------------->
# start_pipline -- group_A --|                                                                                                                                                                |-- 
#                            ---> create_table_2 --> is_houston_weather_api_ready --> extract_houston_weather_data --> transform_load_houston_weather_data --> uploadS3_to_postgres_weather-->
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 8),
    'email': ['myemail@domain.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=2)
}

with DAG('weather_dag_2',
        default_args=default_args,
        schedule_interval = '@daily',
        catchup=False) as dag:


        # Intital junction task from where parallel tasks gets segregated
        start_pipeline = DummyOperator(
            task_id = 'start_pipeline_task'
        )


        # Now we create a group and add connect workflow in it
        # Assume it as DAG inside a DAG
        # tooltip display name whern you hover over the Group pipeline in Airflow
        with TaskGroup(group_id = 'group_a', tooltip= "Extract_from_S3_and_weatherapi") as group_A:
            
            # Table 1,  task1 create table and schema in postgres
            create_table_1 = PostgresOperator(
                task_id='create_table1_psql_tsk',
                postgres_conn_id = "postgres_conn",
                sql= '''  
                    CREATE TABLE IF NOT EXISTS city_look_up (
                    city TEXT NOT NULL,
                    state TEXT NOT NULL,
                    census_2020 numeric NOT NULL,
                    land_Area_sq_mile_2020 numeric NOT NULL                    
                );
                '''
            )
            # task2: Clear all previous records and restore the schema
            truncate_table = PostgresOperator(
                task_id='truncate_table_tsk',
                postgres_conn_id = "postgres_conn",
                sql= ''' TRUNCATE TABLE city_look_up;
                    '''
            )

            # Loading data from s3 to schema defined in postgres
            uploadS3_to_postgres_city  = PostgresOperator(
                task_id = "uploadS3_postgres_tsk",
                postgres_conn_id = "postgres_conn",
                # postgres_conn_id, must in `connection` tab of airflow. In airflow connection tab, host will be endpoint copied from AWS RDS postgres

                sql = "SELECT aws_s3.table_import_from_s3('city_look_up', '', '(format csv, DELIMITER '','', HEADER true)', 'myy-s3-buckett', 'us_city.csv', 'ap-south-1');"
                # city_look_up - table into which data need to be inserted
                # myy-s3-buckett - bucket name from where data to be extracted
                # us_city.csv - is file within bucket to be extracted and ingested into RDS
            )


            # First task flow is completed by adding data from S3 to Postrgresql
            # Now its turn to implement second pipeline 

            # Second flow 
            create_table_2 = PostgresOperator(
                task_id='create_table2_psql_tsk',
                postgres_conn_id = "postgres_conn", 
                sql= ''' 
                    CREATE TABLE IF NOT EXISTS weather_data (
                    city TEXT,
                    description TEXT,
                    temperature_farenheit TEXT,
                    temp_degree TEXT,
                    feels_like_farenheit TEXT,
                    minimun_temp_farenheit TEXT,
                    maximum_temp_farenheit TEXT,
                    minimun_temp_degree TEXT,
                    maximum_temp_degree TEXT,
                    pressure NUMERIC,
                    humidity NUMERIC,
                    wind_speed NUMERIC,
                    time_of_record TIMESTAMP,
                    sunrise_local_time TIMESTAMP,
                    sunset_local_time TIMESTAMP                    
                );
                '''
            )


            # Task 2.2 : Check API credentials
            is_houston_weather_api_ready = HttpSensor(
                task_id ='is_houston_weather_api_ready_tsk',
                http_conn_id='weathermap_api',
                endpoint='/data/2.5/weather?q=houston&APPID=f102a751041e1dafd40de62c26d945c5' 
                # url = api.openweathermap.org + /data/2.5/weather?q=houston&APPID=f102a751041e1dafd40de62c26d945c5 (location & API key)
                # In Airflow Connection tab We will provide 
                # connection_id = `weathermap_api`, host = http/api.openweathermap.org/
            )

            # Task 2.3 to extract the Data in JSON
            extract_houston_weather_data = SimpleHttpOperator(
                task_id = 'extract_houston_weather_data_tsk',
                http_conn_id = 'weathermap_api',
                endpoint='/data/2.5/weather?q=houston&APPID=f102a751041e1dafd40de62c26d945c5',
                method = 'GET',
                response_filter= lambda r: json.loads(r.text),
                log_response=True
            )


            # python code - Extract json data convert into pandas and load into s3 bucket
            transform_load_houston_weather_data = PythonOperator(
                task_id= 'transform_load_houston_weather_data',
                python_callable=transform_load_data
            )


            #loading data from s3 bucket to postgres
            uploadS3_to_postgres_weather  = PostgresOperator(
                task_id = "uploadS3_postgres2_tsk",
                postgres_conn_id = "postgres_conn",
                # postgres_conn_id, must in `connection` tab of airflow. In airflow host will be endpoint copied from AWS RDS postgres

                # weather_data - table in postgres created above to store data from s3 bucket
                sql = "SELECT aws_s3.table_import_from_s3('weather_data', '', '(format csv, DELIMITER '','', HEADER true)', 'myy-s3-buckett', 'houston_data.csv', 'ap-south-1');"
            )

            # ### ---------- OR




            ## Python code - Load csv file created by transform_load_houston_weather_data where we downloaded file in local system rather than s3
            ##  and upload into postgres db
            
            # uploadLocal_to_postgres = PythonOperator(
            #     task_id = "uploadLocaltoPG_tsk",
            #     python_callable = loading 
            # )

            # Unless we provide this workflow, it new task will join from junction task 
            # We want 2 junction table 1 and table 2 and remaining must connect either of table task
            create_table_1 >> truncate_table >> uploadS3_to_postgres_city 
            create_table_2 >> is_houston_weather_api_ready >> extract_houston_weather_data >> transform_load_houston_weather_data >> uploadS3_to_postgres_weather
            # >> uploadLocal_to_postgres 

        
        # Join table 1 and table 2 created in postgres on common column `city`
        join_data = PostgresOperator(
                task_id='task_join_data',
                postgres_conn_id = "postgres_conn",
                sql= '''SELECT 
                    w.city,                    
                    description,
                    temperature_farenheit,
                    feels_like_farenheit,
                    minimun_temp_farenheit,
                    maximum_temp_farenheit,
                    pressure,
                    humidity,
                    wind_speed,
                    time_of_record,
                    sunrise_local_time,
                    sunset_local_time,
                    state,
                    census_2020,
                    land_area_sq_mile_2020                    
                    FROM weather_data w
                    INNER JOIN 
                    city_look_up c 
                    ON w.city = c.city                                      
                ;
                '''
            ) 

        # Loading this joined table into S3 bucket
        save_join_data_s3 = PythonOperator(
            task_id = "join_table_to_s3_tsk",
            python_callable = save_join_tbl_to_s3
        )

        # End our pipeline (dummy task only for represntation purpose)

        end_pipeline = DummyOperator(
            task_id = 'end_pipeline_task'
        )

        start_pipeline >> group_A >> join_data >> save_join_data_s3 >> end_pipeline
