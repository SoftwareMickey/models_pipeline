from django.http import JsonResponse
import csv
import io

def dataloading(data):
    print()
    print('----------------------------- FILE PROCESSING ----------------------------------------')
    
    try:
            # Read and decode the file contents
            decoded_file = data.read().decode('utf-8')

            # Use io.StringIO to treat the decoded content as a file object
            io_string = io.StringIO(decoded_file)

            # Read the CSV file using csv.reader
            reader = csv.reader(io_string)

            # Initialize a list to store the rows
            data_list = []

            # Iterate through each row in the CSV file
            for row in reader:
                # Append each row to the data_list
                data_list.append(row)
                
            for data_set in data_list:
                print(data_set)

            # Return the processed CSV content as a JSON response
            return JsonResponse({"data": data_list})

    except Exception as e:
        # Handle any errors that occur during processing
        return JsonResponse({"error": str(e)}, status=500)