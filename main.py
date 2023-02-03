import pandas as pd
import csv
from gender_detector import GenderDetector


def structure_raw_data():
    charge_data = {}
    current_charge = ""
    current_record_count = 0
    with open('combined_data_chap1_2.txt', 'rt') as file:
        for line in file:
            if not line.isspace():
                if line.isupper():
                    current_charge = line.strip("\n").capitalize()
                    continue

                for records in line.split("; "):
                    fields = records.strip("\n").split(", ")
                    # calculate id concatenation of current charge and current record count
                    current_charge_id = current_charge + \
                        str(current_record_count)
                    temp_record = [current_charge_id, current_charge, "unknown",
                                   "unknown", "unknown", "unknown", "unknown", "'"]
                    # name does not have "negro" or  "unknown" in it, then only assign names
                    if not("negro" in fields[1].lower()) and not("unknown" in fields[1].lower()):
                        name = fields[1].strip().split(" ")
                        temp_record[2] = name[0]
                        temp_record[3] = name[-1]
                    # assign date
                    temp_record[4] = fields[0].strip()
                    # assign city
                    temp_record[5] = fields[2].strip()
                    if len(fields) == 4:
                        # assign state
                        temp_record[6] = fields[3].strip()
                    if temp_record[2] != "unknown":
                        # assign gender
                        detector = GenderDetector('us')
                        # We use detector function for United States as the names are from US
                        try:
                            temp_record[7] = detector.guess(temp_record[2])  # guess using first name
                        except:
                            temp_record[7] = ","
                    else:
                        temp_record[7] = ","
                    charge_data[current_charge_id] = temp_record
                    current_record_count += 1

        return charge_data


def create_csv(charge_data):
    with open("processed_data.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(["Charge_ID", "Charge", "First_Name",
                        "Last_Name", "Date", "City", "State", "Gender"])
        for charge_data in charge_data.values():
            writer.writerow(charge_data)


def create_excel():
    read_file = pd.read_csv("processed_data.csv")
    read_file.to_excel("processed_data.xlsx", header=True, index=None)


if __name__ == "__main__":
    create_csv(structure_raw_data())
    create_excel()
