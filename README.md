# Data Structure of the Woehler QR Code

## General Structure
Every QR code has the same basic structure.
The first few field numbers, as well as the last field number, are general field numbers.
They are the same in every QR code.
The order and presence of the general field numbers can be used to verify the QR code's general validity.

A validity marker is inserted between the field number and the payload.
The validity marker is a single letter.
The meaning of the individual letters is described in the "Validity markers" table.

Every line of text in the QR code has the same structure.
Each line starts with a field number, followed by a validity marker and the payload.
The only exception is the last line, which starts with field number 20.
This line has no payload and signals the end of the transmission.
All lines are terminated by the line feed character (LF, ASCII 0x0A, `\n`).
The payload may also contain an LF. In this case, the LF is replaced by the string "\n".

The general field numbers are described in the JSON file under `general_field`.
The data types of the field numbers are described in the JSON file under `datatype`.
The section names are described in the JSON file under `section_title`.

The JSON file does not contain field numbers for every section listed under `section_title`.
Since many pressure measurements use the same field numbers, these field numbers are not listed separately for every section in the JSON file.
Field numbers used in multiple sections are listed under section 0.

Please note that a missing field number in a measurement does not mean that the measurement is invalid.
Some measurements do not contain all field numbers.
In such cases, the missing field numbers are not relevant.

### General field numbers
|Field number|Data type|Description|
|------------|---------|-----------|
|1|N|Start of transmission; the number specifies the protocol version|
|3|N|Total number of QR codes required for the transmission|
|4|N|Number of the current QR code|
|5|N|Section number indicating which section follows|
|20|S|End of transmission|

### Data types
A data type is always assigned to a field number.
The possible data types are described in the following table.

|Data type|Description|Format|Example|
|---------|-----------|------|-------|
|Z|Text string|Any characters|Hello World|
|D|Date|YYYYMMDD|20210930|
|U|Time|HH:MM|10:39|
|N|Numeric value|Values with a sign and a decimal point are allowed<br>Leading zeroes may be omitted, including for negative values<br>Special value `NaN` represents "Not a Number"|9<br>-9<br>-99.999<br>.99<br>-.99<br>NaN|
|L|List of numeric values|Numeric values separated by tabs<br>(`\t`, ASCII 0x09)<br>Data type N applies to each value|1\t2\t3|
|P|Checkpoint|0: Not checked, no result available<br>1: OK / unrestricted serviceable<br>2: Not OK / not serviceable<br>3: Conditionally OK / reduced serviceability|1|
|S|Control field without payload|---|---|

### Validity markers
A validity marker is inserted between the field number and the payload.
The validity marker is a single letter.
The meaning of the individual letters is described in the following table.

|Validity marker|Meaning|
|---------------|-------|
|G|Valid data or measurement values|
|N|Invalid data|

___
## Value Mappings and Units
Some field numbers have associated value mappings that define the possible values and their meanings.
Other field numbers may have associated units that define the measurement units for the data.
These value mappings help interpret the data correctly, while the associated units identify the units of measurement.

Note that there is also a value mapping for the checkpoint data type (P).
This provides additional information for interpreting the checkpoint field, because the checkpoint data type is already clearly defined.

### Example
Field number `497` in section `0` has an associated value mapping named `pressure_state`.
The possible values are found in the `value_mapping` section, and their meanings are as follows:

|Value|Meaning|
|-----|-------|
|0|Relative pressure|
|1|Absolute pressure|

Field number `450` in section `0` has the associated unit `hPa`.
Note that the key `unit` directly indicates the measurement unit for the associated field.
There is also a `unit` value mapping in the `value_mapping` section.
Field number `109` in section `1` is a special case used to specify the global pressure unit.
This field number shows the global unit setting configured on the device and is not relevant to the units of individual fields in the QR code.
___
## QR Code Example
The following QR code contains data from a leak test on a gas pipe.
The data contains four sections.
The first section contains device information, the second section contains customer information, the third section contains project data, and the fourth section contains the test results.

```text
1G2                 # General field number: start of transmission, protocol version 2
3G1                 # General field number: total number of QR codes required for the transmission
4G1                 # General field number: number of the current QR code
5G1                 #  \    Section number indicating which section follows (here: 1 = device information)
100GWoehler         #  |    Field number 100, data type Z: device information: manufacturer: Woehler
101GM 603           #  |    Field number 101, data type Z: device information: device type: M 603
108GDE 1.15         #  |    Field number 108, data type Z: device information: software version: DE 1.15
102G3               #  |    Field number 102, data type Z: device information: serial number: 3
105G20000101        #  /    Field number 105, data type D: device information: date of last inspection: 2000-01-01
5G2                 #           \   Start of the next section (here: 2 = customer information)
120GCustomer 1      #           |   Field number 120, data type Z: customer information: customer name: Customer 1
25G1                #           /   Field number 25, data type Z: customer information: customer number: 1
5G3                 #   \    Start of the next section (here: 3 = project data)
120GProject 1       #   |    Field number 120, data type Z: project data: project name: Project 1
26G1                #   /    Field number 26, data type N: project data: project number: 1
5G21                #           \   Start of the next section (here: 21 = leak test on gas pipes)
23G20250602         #           |   Field number 23, data type D: test date: 2025-06-02
22G13:13            #           |   Field number 22, data type U: test time: 13:13
450G150             #           |   Field number 450, data type N: preset test pressure in hPa: 150 hPa
453G600             #           |   Field number 453, data type N: preset test duration in seconds: 600 s
480G9               #           |   Field number 480, data type N: stabilization time in seconds: 9 s
241G9               #           |   Field number 241, data type N: measurement duration in seconds: 9 s
481G282.6           #           |   Field number 481, data type N: start pressure: 282.6 hPa
484G100.95          #           |   Field number 484, data type N: stop pressure: 100.95 hPa
487G181.65          #           /   Field number 487, data type N: pressure drop: 181.65 hPa
20G                 # General field number (without payload): end of transmission

```

If the QR code contains multiple measurements, another line with field number 5 and the next section number follows at the end of a section.

```text
1G2                 # General field number: start of transmission, protocol version 2
3G1                 # General field number: total number of QR codes required for the transmission
4G1                 # General field number: number of the current QR code
5G1                 #  \    Section number indicating which section follows (here: 1 = device information)
100GWoehler         #  |    Field number 100, data type Z: device information: manufacturer: Woehler
101GM 603           #  |    Field number 101, data type Z: device information: device type: M 603
108GDE 1.15         #  |    Field number 108, data type Z: device information: software version: DE 1.15
102G3               #  |    Field number 102, data type Z: device information: serial number: 3
105G20000101        #  /    Field number 105, data type D: device information: date of last inspection: 2000-01-01
5G2                 #           \   Start of the next section (here: 2 = customer information)
120GCustomer 1      #           |   Field number 120, data type Z: customer information: customer name: Customer 1
25G1                #           /   Field number 25, data type Z: customer information: customer number: 1
5G3                 #   \    Start of the next section (here: 3 = project data)
120GProject 1       #   |    Field number 120, data type Z: project data: project name: Project 1
26G1                #   /    Field number 26, data type N: project data: project number: 1
5G21                # Start of the first measurement (here: 21 = leak test on gas pipes)
23G20250602         
22G13:13               
450G150             
453G600             
480G9               
241G9               
481G282.6           
484G100.95          
487G181.65          
5G23                # Start of the next measurement (here: 23 = leak test on drinking water pipes)
23G20250602
22G13:14
450G150
468G20
469G20
453G7200
480G2
241G0
461G2
481G202.3
484G201.36
487G.94
5G33                # Start of the next measurement (here: 33 = refrigeration circuit measurement)
23G20250602
22G13:20
500G43
550G.01
551G-.67
552G7
553G0
554G16.9
5G35                # Start of the next measurement (here: 35 = vacuum test on a refrigeration system)
23G20250602
22G13:24
453G5
241G1
467G980
495G0
481G-580
484G-660
450G20
172G1
20G                 # General field number (without payload): end of transmission

```

___
## JSON Consistency Check
The JSON files are the important part of this repository. The repository is included as a submodule in other projects, where the JSON files provide the field-name definitions.

The `check_json_diff.py` script is a development aid for comparing two JSON files. It verifies that both files have the same structure and values, while ignoring the values of the `description` keys. This makes it possible to check whether a newly created file matches its counterpart or whether changes made to both files are consistent.

The script uses only Python's standard library, so no packages need to be installed for the comparison itself. The `requirements.txt` file is therefore empty. The development requirements contain only `ruff`, which is used for linting.

### Create a virtual environment
Make sure that Python 3.10 or newer is installed. From the repository root, create a virtual environment:

```powershell
python -m venv .venv
```

Activate it in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Install development tools
To install the linter, install the development requirements:

```powershell
pip install -r requirements-dev.txt
```

### Run the JSON comparison
Pass the two JSON files to the script in the desired order:

```powershell
python .\check_json_diff.py .\field_names_de.json .\field_names_en.json
```

If the files match apart from their `description` values, the script prints a `MATCH` message and exits successfully. Differences in structure or in any other value produce a `DIFFERENCE` message and a non-zero exit code.