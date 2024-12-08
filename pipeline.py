import argparse
import csv
import datetime
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
from apache_beam.io import ReadFromText
from apache_beam.io.gcp.bigquery import WriteToBigQuery

class ParseCustomers(beam.DoFn):
    def process(self, element):
        # Ignora header
        if element.startswith('customer_id,'):
            return
        fields = next(csv.reader([element]))
        if len(fields) != 3:
            return
        customer_id, customer_name, customer_email = fields
        
        # Verifica campos nulos
        if not (customer_id and customer_name and customer_email):
            return
        
        yield {
            'customer_id': customer_id,
            'customer_name': customer_name,
            'customer_email': customer_email
        }

class ParseTransactionsFile1(beam.DoFn):
    def process(self, element):
        if element.startswith('transaction_id,'):
            return
        fields = next(csv.reader([element]))
        if len(fields) != 5:
            return
        transaction_id, customer_id, transaction_date, transaction_amount, transaction_status = fields
        
        if not (transaction_id and customer_id and transaction_date and transaction_amount and transaction_status):
            return
        
        # Converte data
        try:
            parsed_date = datetime.datetime.strptime(transaction_date, '%Y-%m-%d').date()
        except ValueError:
            return
        
        # Converte valor para float
        try:
            amount = float(transaction_amount)
        except ValueError:
            return
        
        yield {
            'transaction_id': transaction_id,
            'customer_id': customer_id,
            'transaction_date': parsed_date,
            'transaction_amount': amount,
            'transaction_status': transaction_status
        }

class ParseTransactionsFile2(beam.DoFn):
    def process(self, element):
        if element.startswith('transaction_id,'):
            return
        fields = next(csv.reader([element]))
        if len(fields) != 4:
            return
        transaction_id, transaction_type, qtty, price = fields
        
        if not (transaction_id and transaction_type and qtty and price):
            return
        
        # Converte qtty e price
        try:
            qtty_val = float(qtty)
            price_val = float(price)
        except ValueError:
            return
        
        yield {
            'transaction_id': transaction_id,
            'transaction_type': transaction_type,
            'qtty': qtty_val,
            'price': price_val
        }

def run():
    # Ajuste conforme necessário
    project_id = 'nexus-443823'
    dataset = 'nxscase2024'
    region = 'us-west1'
    bucket = 'nxs'
    
    # Tabelas alvo
    customers_table = f'{project_id}:{dataset}.customers_file3'
    transactions1_table = f'{project_id}:{dataset}.transactions_file1'
    transactions2_table = f'{project_id}:{dataset}.transactions_file2'
    
    # Padrões de entrada
    customers_pattern = 'gs://nxs/csv_files/customer*.csv'
    transactions1_pattern = 'gs://nxs/csv_files/transactions_file1*.csv'
    transactions2_pattern = 'gs://nxs/csv_files/transactions_file2*.csv'
    
    # Esquemas
    customers_schema = {
        'fields': [
            {'name': 'customer_id', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'customer_name', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'customer_email', 'type': 'STRING', 'mode': 'NULLABLE'}
        ]
    }

    transactions1_schema = {
        'fields': [
            {'name': 'transaction_id', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'customer_id', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'transaction_date', 'type': 'DATE', 'mode': 'NULLABLE'},
            {'name': 'transaction_amount', 'type': 'FLOAT', 'mode': 'NULLABLE'},
            {'name': 'transaction_status', 'type': 'STRING', 'mode': 'NULLABLE'}
        ]
    }

    transactions2_schema = {
        'fields': [
            {'name': 'transaction_id', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'transaction_type', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'qtty', 'type': 'FLOAT', 'mode': 'NULLABLE'},
            {'name': 'price', 'type': 'FLOAT', 'mode': 'NULLABLE'}
        ]
    }

    # Opções do pipeline
    pipeline_options = PipelineOptions(
        runner='DataflowRunner',
        project=project_id,
        region=region,
        temp_location=f'gs://{bucket}/temp',
        staging_location=f'gs://{bucket}/temp',
        job_name='csv-to-bq-pipeline',
        #template_location='gs://nxs/templates/csv-to-bq-pipeline',
        save_main_session=True)

    
    pipeline_options.view_as(StandardOptions).streaming = False

    with beam.Pipeline(options=pipeline_options) as p:
        
        # Customers
        (
            p
            | 'ReadCustomers' >> ReadFromText(customers_pattern, skip_header_lines=0)
            | 'ParseCustomers' >> beam.ParDo(ParseCustomers())
            | 'WriteCustomersToBQ' >> WriteToBigQuery(
                customers_table,
                schema=customers_schema,
                write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
                create_disposition=beam.io.BigQueryDisposition.CREATE_NEVER
            )
        )

        # Transactions 1
        (
            p
            | 'ReadTransactions1' >> ReadFromText(transactions1_pattern, skip_header_lines=0)
            | 'ParseTransactions1' >> beam.ParDo(ParseTransactionsFile1())
            | 'WriteTransactions1ToBQ' >> WriteToBigQuery(
                transactions1_table,
                schema=transactions1_schema,
                write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
                create_disposition=beam.io.BigQueryDisposition.CREATE_NEVER
            )
        )

        # Transactions 2
        (
            p
            | 'ReadTransactions2' >> ReadFromText(transactions2_pattern, skip_header_lines=0)
            | 'ParseTransactions2' >> beam.ParDo(ParseTransactionsFile2())
            | 'WriteTransactions2ToBQ' >> WriteToBigQuery(
                transactions2_table,
                schema=transactions2_schema,
                write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
                create_disposition=beam.io.BigQueryDisposition.CREATE_NEVER
            )
        )

if __name__ == '__main__':
    run()
