import requests
import zipfile
import os
import pandas as pd
import tempfile
import shutil
import logging
from datetime import datetime, timedelta
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import EquityRecord

logger = logging.getLogger(__name__)

def home(request):
    return HttpResponse("<h1>Welcome to the Equity Bhavcopy Application!</h1>")

@api_view(['POST'])
def download_bhavcopy(request):
    date_str = request.data.get('date', '')

    if not date_str:
        return Response({'message': 'Date parameter is required'}, status=400)

    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return Response({'message': 'Invalid date format'}, status=400)

    zip_url = f'https://www.bseindia.com/download/BhavCopy/Equity/EQ{selected_date.strftime("%d%m%y")}_CSV.ZIP'
    print("Downloading ZIP from URL:", zip_url)

    headers = {'User-Agent': 'Mozilla/5.0'}
    
    response = requests.get(zip_url, headers=headers, allow_redirects=True)
    if response.status_code != 200:
        return Response({'message': 'Failed to download data'}, status=response.status_code)

    with tempfile.NamedTemporaryFile(delete=False) as temp_zip_file:
        temp_zip_file.write(response.content)
        temp_zip_path = temp_zip_file.name

    extract_to = tempfile.mkdtemp()

    try:
        with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)

            # List the contents of the ZIP file
            zip_contents = zip_ref.namelist()
            print("Contents of the ZIP file:", zip_contents)  # Log the names of files in the ZIP

        # Debugging: List extracted files
        extracted_files = os.listdir(extract_to)
        print("Extracted files:", extracted_files)  # Log the names of extracted files

        csv_file_name = [f for f in extracted_files if f.endswith('.csv') or 'csv' in f.lower()]
        if not csv_file_name:
            return Response({'message': 'No CSV file found after extraction'}, status=500)

        csv_file_path = os.path.join(extract_to, csv_file_name[0])
        
        # Debugging: Check the content of the CSV file
        with open(csv_file_path, 'r') as csv_file:
            first_lines = csv_file.readlines()[:5]  # Read the first 5 lines
            print("First few lines of the detected CSV file:", first_lines)

        # Read CSV with Pandas
        data = pd.read_csv(csv_file_path, skip_blank_lines=True, encoding='utf-8')
        print("DataFrame shape:", data.shape)  # Log the shape of the DataFrame
        print("DataFrame contents:\n", data.head())  # Log the contents of the DataFrame

        if data.empty:
            return Response({'message': 'No data found in CSV'}, status=500)

       
        for index, row in data.iterrows():
             try:
                 print(f"Saving record: {row['SC_CODE']}, {row['SC_NAME']}, {row['OPEN']}, {row['HIGH']}, {row['LOW']}, {row['CLOSE']}, {row['NO_OF_SHRS']}, {row['LAST']}")
                 EquityRecord.objects.update_or_create(
            code=row.get('SC_CODE', ''),
            defaults={
                'name': row.get('SC_NAME', ''),
                'open': row.get('OPEN', None),
                'high': row.get('HIGH', None),
                'low': row.get('LOW', None),
                'close': row.get('CLOSE', None),
                'volume': row.get('NO_OF_SHRS', None),
                'date': pd.to_datetime(row.get('LAST', None)).date() if 'LAST' in row else None
            }
        )
             except Exception as e:
                  logger.error(f"Error saving record at index {index}: {e}, row data: {row}")


        

        return Response({'message': 'Data downloaded and saved successfully'})
    finally:
        os.remove(temp_zip_path)
        shutil.rmtree(extract_to)

@api_view(['POST'])
def search_equity(request):
    code = request.data.get('code', None)
    name = request.data.get('name', None)
    
    filters = {}
    if code:
        filters['code__icontains'] = code
    if name:
        filters['name__icontains'] = name

    records = EquityRecord.objects.filter(**filters)

    response_data = [
        {
            'id': record.id,
            'code': record.code,
            'name': record.name,
            'open': record.open,
            'high': record.high,
            'low': record.low,
            'close': record.close,
            'volume': record.volume,
            'date': record.date,
        } for record in records
    ]

    return Response({'records': response_data})



@api_view(['POST'])
def update_equity(request):
    record_id = request.data.get('id', None)
    if not record_id:
        return Response({'message': 'Record ID is required'}, status=400)

    try:
        record = EquityRecord.objects.get(id=record_id)
    except EquityRecord.DoesNotExist:
        return Response({'message': 'Record not found'}, status=404)

    for field in ['code', 'name', 'open', 'high', 'low', 'close', 'volume', 'date']:
        if field in request.data:
            setattr(record, field, request.data[field])

    record.save()
    return Response({'message': 'Record updated successfully'})

@api_view(['POST'])
def delete_equity(request):
    record_id = request.data.get('id', None)
    if not record_id:
        return Response({'message': 'Record ID is required'}, status=400)

    try:
        record = EquityRecord.objects.get(id=record_id)
        record.delete()
        return Response({'message': 'Record deleted successfully'}, status=204)
    except EquityRecord.DoesNotExist:
        return Response({'message': 'Record not found'}, status=404)

@api_view(['POST'])
def available_dates(request):
    # Define the end date (July 31, 2024)
    end_date = datetime(2024, 7, 31)
    
    # Create a list of dates from January 1, 2024, to July 31, 2024
    available_dates = []
    current_date = datetime(2024, 1, 1)
    
    while current_date <= end_date:
        available_dates.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=1)

    return Response({'available_dates': available_dates})

