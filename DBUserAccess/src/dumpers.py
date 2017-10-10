import strs
from logs import Log
import csv


class DumpResult :
    """
    Dump list to file
    """

    def __init__(self, output_formate, input_list):
        self.input_list = input_list
        self.output_formate = output_formate

        # dump file to required formate
        if self.output_formate == strs.output_formate_csv :
            self.dumpToCsv(self.input_list)
        elif self.output_formate == strs.output_formate_excel:
            self.dumpToExcel(self.input_list)
        else:            
            Log.writeLog('File format not recognized. Formate: ' + str(self.output_formate) + ' : ' + str(output_formate), strs.ERRO)

    def dumpToCsv(self, input_list):
        """
        Convert the input list into csv file. 
        Filename: output.csv
        """        

        try:
            with open(strs.output_file_csv, "wb") as f:
                writer = csv.writer(f)
                for row in input_list: # modified speciall for this class.
                    writer.writerows(row)

            return 1
        except Exception, e:
            Log.writeLog('Exception while writing to ' + strs.output_file_csv, strs.ERRO)
            return 0


    def dumpToExcel(self, input_list):
        """
        Convert the input list into excel file. 
        Filename: output.xls
        """
        pass