import csv
import serial
import serial.tools.list_ports
from datetime import datetime

ports = serial.tools.list_ports.comports()
portsList = []
for port in ports:
    portsList.append(str(port))
    print(str(port))

selectedPort = input("Please select an available port (COM): ")
watchString = input("String to analyze (starts with): ")
fileName = input("Output File: ")

max_entries = int(input("Enter the maximum number of data entries: "))
print(max_entries)

workbook = f'{fileName}.csv'

serialDebug = serial.Serial(port=f'COM{selectedPort}', baudrate=115200,
                            bytesize=8, parity="N", stopbits=serial.STOPBITS_TWO, timeout=1)

# Counter variables
index = 1
count = 0

# Open the CSV file for writing
with open(workbook, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['No', 'payload', 'timestamp'])  # CSV header

    while True:
        try:
            serialString = serialDebug.readline().decode("utf").rstrip("\n")
            if len(serialString) > 0:
                print(serialString)
                if serialString.startswith(watchString):
                    payload = serialString.replace("_x000D_", " ")
                    timestamp = datetime.strftime(
                        datetime.now(), '%H:%M:%S.%f')[:-3]
                    writer.writerow([index, payload, timestamp])

                    index += 1
                    count += 1
                    if count == max_entries:
                        print("Saving File...")
                        break
        except KeyboardInterrupt:
            print("Handling interrupt...")
            print("Saving File...")
            break

print("Process Done")
