#!/usr/bin/env python3

import re
import sys
import os

def main():

    # If the user does not provide "< filename" in the command line, print a message to standard error
    if(sys.stdin.isatty()):

        print("Error: No input file specified!", file=sys.stderr)
        exit(6)

    # file_content stores the contents of the file as a long string
    file_content = ''

    # For every line in the input file, strip any whitespace off of the line and append it to the file content string
    for line in sys.stdin:

        file_content += line

    # Collapse all whitespaces present in the file to a single space
    # by substituting one or more whitespace characters with a single space
    file_content = re.sub('\s+', ' ', file_content)

    # rowspan and colspan are not permitted, print an error and exit if one of them is found
    if(file_content.find('rowspan') != -1 or file_content.find('colspan') != -1):

        print("Error: The input file cannot contain rowspan or colspan!", file=sys.stderr)
        exit(6)

    # Search file_content for everything located inbetween a pair of table tags
    # table_strings will be a list where each element is the contents of a table
    table_strings = re.findall(r'<table.*?>(.*?)</table.*?>', file_content, flags=re.DOTALL | re.IGNORECASE)
    
    # print a message to stderr if an empty table is found
    if(' ' in table_strings or '' in table_strings):

        print("Warning: This file contains an empty table", file=sys.stderr)

    # Calculate the number of opening and closing tags for tables, rows, headers, and cells
    num_opening_table = len(re.findall(r'<table[^<]*?>', file_content, flags=re.DOTALL | re.IGNORECASE))
    num_closing_table = len(re.findall(r'</table[^<]*?>', file_content, flags=re.DOTALL | re.IGNORECASE))

    num_opening_row = len(re.findall(r'<tr[^<]*?>', file_content, flags=re.DOTALL | re.IGNORECASE))
    num_closing_row = len(re.findall(r'</tr[^<]*?>', file_content, flags=re.DOTALL | re.IGNORECASE))

    num_opening_header = len(re.findall(r'<th[^<]*?>', file_content, flags=re.DOTALL | re.IGNORECASE))
    num_closing_header = len(re.findall(r'</th[^<]*?>', file_content, flags=re.DOTALL | re.IGNORECASE))

    num_opening_cell = len(re.findall(r'<td[^<]*?>', file_content, flags=re.DOTALL | re.IGNORECASE))
    num_closing_cell = len(re.findall(r'</td[^<]*?>', file_content, flags=re.DOTALL | re.IGNORECASE))

    # calculate the number of opening and closing brackets in the document.
    opening_brackets = len(re.findall(r'<', file_content))
    closing_brackets = len(re.findall(r'>', file_content))

    # print an error message and exit if the opening and closing bracket counts are not equal
    if(opening_brackets != closing_brackets):
        
        print("Error: This file contains unbalanced opening and closing brackets!", file=sys.stderr)
        exit(6)

    # if the number of opening tables tags does not equal the number of closing table tags,
    # print an error and then exit
    if(num_opening_table != num_closing_table):

        if(num_opening_table != 0 or num_closing_table != 0):

            print("Error: This file contains unbalanced table tags!", file=sys.stderr)
            exit(6)
    
    # print an error if no tables where found
    if(table_strings == []):

        print("Warning: This file does not contain any tables!", file=sys.stderr)

    # if the number of opening and closing tags are not equal for rows, headers, or cells, print an error message and exit
    if(num_opening_row != num_closing_row):

        print("Error: This file contains unbalanced row tags!", file=sys.stderr)
        exit(6)
    
    if(num_opening_header != num_closing_header):

        print("Error: This file contains unbalanced header tags!", file=sys.stderr)
        exit(6)

    if(num_opening_cell != num_closing_cell):

        print("Error: This file contains unbalanced cell tags!", file=sys.stderr)
        exit(6)

    # calculate the total number of rows, header cells, and regular cells present in the document
    total_num_rows = len(re.findall(r'<tr.*?>(.*?)</tr.*?>', file_content, flags=re.DOTALL | re.IGNORECASE))
    total_num_cells = len(re.findall(r'<td.*?>(.*?)</td.*?>', file_content, flags=re.DOTALL | re.IGNORECASE))
    total_num_header_cells = len(re.findall(r'<th.*?>(.*?)</th.*?>', file_content, flags=re.DOTALL | re.IGNORECASE))

    # variables to count the number of rows, header cells, and regular cells located within the correct tags
    num_cells_in_rows = 0
    num_header_cells_in_rows = 0
    num_rows_in_tables = 0

    # a list to hold table objects
    all_tables = []

    # iterate through each table match found
    for entry in table_strings:

        # data represents a list of the content of all of the rows of the current table 'entry'
        # each element in data represents the contents of a row
        data = re.findall(r'<tr.*?>(.*?)</tr.*?>', entry, flags=re.DOTALL | re.IGNORECASE)

        num_rows_in_tables += len(data)

        # table_data is a list that keeps track of the content of each row in the order it appears
        # the contents of table_data can be that of header-rows and "non-header" rows
        table_data = []

        for item in data:

            # for each row, pick out all of the header cells and all of the non-header cells
            # if there is no match, the result is an empty list []
            headers = re.findall(r'<th.*?>(.*?)</th.*?>', item, flags=re.DOTALL | re.IGNORECASE)
            non_headers = re.findall(r'<td.*?>(.*?)</td.*?>', item, flags=re.DOTALL | re.IGNORECASE)

            num_cells_in_rows += len(non_headers)
            num_header_cells_in_rows += len(headers)

            # if there were no header and non-header matches, the row must be an empty row <tr></tr>
            # account for this by appending an empty row to table_data
            if(headers == [] and non_headers == []):
                
                table_data.append([])
                print("Warning: Found a table with an empty row!", file=sys.stderr)

            # if there were headers and non-headers in the same row, assume the headers come first and 
            # append the concatenation of the two matched lists to table data
            elif(headers != [] and non_headers != []):

                table_data.append(headers + non_headers)

            # If there are only matches on headers, append headers to table_data
            elif(headers != []):

                table_data.append(headers)

            # If there are only matches on non-headers, append non-headers to table data
            elif (non_headers != []):

                table_data.append(non_headers)

        # Convert the list of rows containing row data to a table object called current_table
        current_table = table(table_data)

        # append current_table to the list of tables
        all_tables.append(current_table)

    # if there are more rows than rows within table tags, the input is invalid
    if(total_num_rows > num_rows_in_tables):

        print("Error: <tr> tag occured outside of a <table> tag!", file=sys.stderr)
        exit(6)

    # if there are more cells than cells within row tags, the input is invalid
    if(total_num_cells > num_cells_in_rows):

        print("Error: <td> tag occured outside of a <tr> tag!", file=sys.stderr)
        exit(6)

    # if there are more header cells than header cells within row tags, the input is invalid
    if(total_num_header_cells > num_header_cells_in_rows):
        
        print("Error: <th> tag occured outside of a <tr> tag!", file=sys.stderr)
        exit(6)


    # calculate the number of tables found in the html file
    num_tables = len(all_tables)

    # print out each table in csv format, each table is separated by a space
    # and a title TABLE X: where x represents the order the table appeared in the document
    for i in range(num_tables):

        print("TABLE " + str(i + 1) + ":")
        all_tables[i].print_table()

        if(i < num_tables - 1):
            print()


# the class table is used to store table objects

class table():

    # the constructor of this class takes in a list of rows of the table
    # each item in the list represents the content found in that row

    def __init__(self, row_list = None):

        self.rows = []
        self.max_row_length = 0

        if (row_list != None):

            # convert each element in row_list into a row object and append it to the rows of a table
            for entry in row_list:

                current_row = row(entry)
                self.rows.append(current_row)

                # check the length of each row coming in to determine the maximum length of each row in the table
                if(current_row.get_num_cells() > self.max_row_length):
                    self.max_row_length = current_row.get_num_cells()

            # iterate through each row in the table and expand all rows less than the maximum length to the maximum length
            for entry in self.rows:

                if(not self.full_row(entry.get_cells())):

                    self.expand_row(entry)

    
    def print_table(self):

        """
        Prints the contents of the table to stdout, row by row
        """
        for row in self.rows:

            print(row.get_row_string())

    def expand_row(self, current_row):

        """
        Expands the specified row so that is the same length as the maximum row in the table
        It performs the expansion by appending the required number of empty strings to the row
        """

        for i in range(self.max_row_length - current_row.get_num_cells()):

            current_row.add_cell('')
    
    def full_row(self, current_row):

        """
        Checks if current_row by comparing it to the max length
        """

        if(len(current_row) < self.max_row_length):

            return False
        
        return True

# a class to store rows as row objects
class row():

    # constructor takes in a row of cells
    def __init__(self, cell_row = None):

        if(cell_row == None):

            self.cell_row = []

        else:

            # if a non-empty cell row is input, strip all of the whitespace off of the ends 
            # of each element in the list
            self.cell_row = [word.strip() for word in cell_row]
        
        for word in cell_row:

            if(word.find(',') != -1):

                print("Error: Comma present in cell!", file=sys.stderr)
                exit(6)

    def get_num_cells(self):

        """
        Returns the number of cells in the row
        """

        return len(self.cell_row)

    def get_cells(self):

        """
        Returns the list of cells
        """

        return self.cell_row

    def get_row_string(self):

        """
        Returns a string representation of the row where the contents of each cell are separated by a comma
        """

        return ",".join(self.cell_row)
    
    def add_cell(self, content):

        """
        Adds the string content to the to the list of cells
        """

        self.cell_row.append(content)
        

if __name__ == "__main__":

    main() 
