import csv
import sys
from datetime import datetime

# Verifying user args
if len(sys.argv) != 2:
    print("Usage: python split_data.py <path_of_file.csv>")
    sys.exit(1)

filename=str(sys.argv[1])

print("Read data from:" , filename)

# Open file as CSV
with open(filename, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    # Store columns headers'
    fields=csv_reader.fieldnames
    # Sorting by station_id
    csv_reader = sorted(csv_reader, key=lambda row: datetime.strptime(row['event_time'], "%Y-%m-%d %H:%M:%S UTC"))
    # This will be the current station_id variable
    count=0
    # This will count the number of different station_id (aka subdataset)
    sidn=0
    # This will be the current output file
    outf=None
    # Size of the dataset
    size=len(csv_reader)
    for row in csv_reader:
        # If the station_id change
        if (count%5000) == 0:
            # Close the previous outfile (except for first pass)
            if outf:
                outf.close()
            # Update count
            count+=1
            # Generate a subset name
            subset_fn = 'subdataset_' + str(sidn) + '.csv'
            sidn += 1
            # Creating the file
            outf=open(subset_fn, mode='w')
            writer=csv.DictWriter(outf, fieldnames=fields)
            writer.writeheader()
            print("Start writing subdataset number", sidn)
        count+=1
        # Writing current row
        writer.writerow(row)
    outf.close()
