# ASL Payroll

The purpose of this script is to format payroll information for the ASL brand in a particular way.

TODO: describe the way in which this payroll information is accepted and subsequently formatted.

## Folder Setup

Looks for a file called `~/Documents/asl-payroll/EiD_SageImport_Template.xlsm` and modifies it

## Python Env Setup
- Export conda packages to environment
`conda env export > environment.yml`

- Conda install package
`conda install mypackage`

- Update conda from yml (must be activated first)

`conda env update --file environment.yml`

- Switch to the conda env

`conda activate asl`

## Running the project

`python main.py`

## Standalone Executable
Create .exe installer in dist folder
Make changes in code
Copy/send entire vba folder (send to ASL)
Or can use Windows "IDLE" editor and modify directly
From cmd prompt:
cd [map to vb folder on desktop] NOTE: Don't map to document folder because doesn't recognize OneDrive
Type: `pyinstaller -F main.py`
Executable will be placed in "dist" folder ["main"]
Run the new executable (in future, VBA will run this directly from within Excel*)
*POSSIBLE ERROR: In prior testing, running the .exe caused an error
*Since Excel is already open when running the VBA script, Excel says: "cannot open file with same filename as open file"
*Needs more testing on Windows machine

## Backup to GIT

This is another test change.
'nuther test    