# pytclfirmware
Scan and extract TCL SmartTV Televisions firmware

Firmware files are available on [TCL](http://www.tcl.eu/) website.
Tested with S83 series files.

## Usage
```shell
git https://github.com/mpata/pytclfirmware.git
cd pytclfirmware/
pip install .

tclfirmware --file ~/Downloads/V8-NT67F02-LF1V436.bin --verify True --extract
```

## Output (example)
```json
{
  "header": {
    "md5": "6333f936d7ee00d78d0eb052aa20f41e", 
    "verified": true, 
    "size": 415113347
  }, 
  "partitions": [
    {
      "md5sum": "9b0c4fa23ea5e4c521c8eb0b4f248edc", 
      "verified": true, 
      "start_pos": 368, 
      "header_pos": 284, 
      "device_name": "/dev/mmcblk0boot0", 
      "name": "mloader", 
      "end_pos": 52192, 
      "type": "none", 
      "size": 51824
    }, 
    {
      "md5sum": "b5e81dd1ec14552a2118a9b4325cd1da", 
      "verified": true, 
      "start_pos": 52276, 
      "header_pos": 52192, 
      "device_name": "/dev/mmcblk0boot0", 
      "name": "ddrcfg", 
      "end_pos": 298036, 
      "type": "none", 
      "size": 245760
    }, 
    {
      "md5sum": "f07226ec8df65abdef979a310050beed", 
      "verified": true, 
      "start_pos": 298120, 
      "header_pos": 298036, 
      "device_name": "/dev/mmcblk0", 
      "name": "stbc", 
      "end_pos": 363656, 
      "type": "none", 
      "size": 65536
    }, 
    {
      "md5sum": "c2675f23a910c00203bd5e9e15092d8d", 
      "verified": true, 
      "start_pos": 363740, 
      "header_pos": 363656, 
      "device_name": "/dev/mmcblk0", 
      "name": "uboot", 
      "end_pos": 726984, 
      "type": "none", 
      "size": 363244
    }, 
    {
      "md5sum": "4972e32330921e58916654b0b4e32cd4", 
      "verified": true, 
      "start_pos": 727068, 
      "header_pos": 726984, 
      "device_name": "/dev/mmcblk0", 
      "name": "logo", 
      "end_pos": 810126, 
      "type": "none", 
      "size": 83058
    }, 
    {
      "md5sum": "03048b17efe129d552bb0ef3aed8d70d", 
      "verified": true, 
      "start_pos": 810210, 
      "header_pos": 810126, 
      "device_name": "/dev/mmcblk0", 
      "name": "secos", 
      "end_pos": 1529786, 
      "type": "none", 
      "size": 719576
    }, 
    {
      "md5sum": "6b80ffb7f2cbc0d4001673c3144e1903", 
      "verified": true, 
      "start_pos": 1529870, 
      "header_pos": 1529786, 
      "device_name": "/dev/mmcblk0p2", 
      "name": "vertbl", 
      "end_pos": 1530022, 
      "type": "none", 
      "size": 152
    }, 
    {
      "md5sum": "40745c8cb2541cc6d51dfeef34d6737d", 
      "verified": true, 
      "start_pos": 1530106, 
      "header_pos": 1530022, 
      "device_name": "/dev/mmcblk0p3", 
      "name": "kernel", 
      "end_pos": 17529082, 
      "type": "none", 
      "size": 15998976
    }, 
    {
      "md5sum": "43919ba0945010e4ed620bb29673dbe5", 
      "verified": true, 
      "start_pos": 17529166, 
      "header_pos": 17529082, 
      "device_name": "/dev/mmcblk0p10", 
      "name": "tclconfig", 
      "end_pos": 18960977, 
      "type": "gzip", 
      "size": 1431811
    }, 
    {
      "md5sum": "75ac915a883168ac108a43759919a10f", 
      "verified": true, 
      "start_pos": 18961061, 
      "header_pos": 18960977, 
      "device_name": "/dev/mmcblk0p11", 
      "name": "tvos", 
      "end_pos": 42595418, 
      "type": "gzip", 
      "size": 23634357
    }, 
    {
      "md5sum": "8265c69ec5136e570b6d36b29715225d", 
      "verified": true, 
      "start_pos": 42595502, 
      "header_pos": 42595418, 
      "device_name": "/dev/mmcblk0p13", 
      "name": "system", 
      "end_pos": 414884871, 
      "type": "gzip", 
      "size": 372289369
    }, 
    {
      "md5sum": "b2a91abc3f151260df5ec95d48b59a9b", 
      "verified": true, 
      "start_pos": 414884955, 
      "header_pos": 414884871, 
      "device_name": "FRC", 
      "name": "FRC", 
      "end_pos": 415113631, 
      "type": "none", 
      "size": 228676
    }
  ]
}
```
