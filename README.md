# TableToCSV
A program that accepts the contents of an html file through standard input and sends the contents of the table(s) contained in the file to standard output. Relevant data is extracted using regular expressions. The extracted content of the tables is in .csv format.
# Getting Started
1. Clone the repository using **git clone https://github.com/YOURUSERNAME/TableToCSV.git**
2. Run the program from the command line using the following format **python table_to_csv.py < input.html > output.txt**<br/>

# Example
The code for the following tables was taken from https://www.w3schools.com/html/html_tables.asp. You can view this code in the example file called index.html which is located in the repository.
<table>
  <tr>
    <th>Company</th>
    <th>Contact</th>
    <th>Country</th>
  </tr>
  <tr>
    <td>Alfreds Futterkiste</td>
    <td>Maria Anders</td>
    <td>Germany</td>
  </tr>
  <tr>
    <td>Centro comercial Moctezuma</td>
    <td>Francisco Chang</td>
    <td>Mexico</td>
  </tr>
  <tr>
    <td>Ernst Handel</td>
    <td>Roland Mendel</td>
    <td>Austria</td>
  </tr>
  <tr>
    <td>Island Trading</td>
    <td>Helen Bennett</td>
    <td>UK</td>
  </tr>
  <tr>
    <td>Laughing Bacchus Winecellars</td>
    <td>Yoshi Tannamuri</td>
    <td>Canada</td>
  </tr>
  <tr>
    <td>Magazzini Alimentari Riuniti</td>
    <td>Giovanni Rovelli</td>
    <td>Italy</td>
  </tr>
</table>
<table style="width:100%">
  <tr>
    <th>Firstname</th>
    <th>Lastname</th>
    <th>Age</th>
  </tr>
  <tr>
    <td>Jill</td>
    <td>Smith</td>
    <td>50</td>
  </tr>
  <tr>
    <td>Eve</td>
    <td>Jackson</td>
    <td>94</td>
  </tr>
</table>

**$ python table_to_csv.py < input.html > output.txt**<br/>
<br/>
The contents of output.txt are shown below. Notice that tables are labeled in the same order as they appear in the document.<br/>
<br/>
TABLE 1:<br/>
Company,Contact,Country<br>
Alfreds Futterkiste,Maria Anders,Germany<br/>
Centro comercial Moctezuma,Francisco Chang,Mexico<br/>
Ernst Handel,Roland Mendel,Austria<br/>
Island Trading,Helen Bennett,UK<br/>
Laughing Bacchus Winecellars,Yoshi Tannamuri,Canada<br/>
Magazzini Alimentari Riuniti,Giovanni Rovelli,Italy<br/>

TABLE 2:<br/>
Firstname,Lastname,Age<br/>
Jill,Smith,50<br/>
Eve,Jackson,94<br/>

# Use
The purpose of this program is to extract the contents of html tables and put it into .csv format. Once the data is converted into .csv format, the user can use different programs to analyze this data. One program they could use to do this is the online analytical processing program (OLAP.py) located in the OnlineAnalyticalProcessing repository. 

# Restrictions
This program will not work if the tables make use of the rowspan or colspan html attributes. 
