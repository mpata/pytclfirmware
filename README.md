# pytclfirmware
Scan and extract TCL SmartTV Televisions firmware

Firmware files are available on TCL website.
Tested with S83 series files.

## Usage
```shell
git https://github.com/mpata/pytclfirmware.git
cd pytclfirmware/
pip install .

tclfirmware --file ~/Downloads/V8-NT67F02-LF1V436.bin --verify True --extract
```
