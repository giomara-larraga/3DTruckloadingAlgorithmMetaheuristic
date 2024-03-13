from utils import read_excel
from container_loading_metaheuristic import container_loading
import sys


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py excel_file container_sheet items_sheet")
        print("Using sample from Sample_data0.xlsx")
        excel_file_path = "Sample_data0.xlsx"
        sheet_container = "Container"
        sheet_items_d1 = "Ex2-del1"
    else:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        arg3 = sys.argv[3]

        excel_file_path = arg1
        sheet_container = arg2
        sheet_items_d1 = arg3
    data_container = read_excel(excel_file_path, sheet_container)
    data_delivery = read_excel(excel_file_path, sheet_items_d1)

    result = container_loading(data_container.to_json(), data_delivery.to_json())

    print(result)
