import argparse
import binascii
import hashlib
import json
import logging
import mmap
import struct
import sys
import zlib


CHUNK_SIZE = 1024 * 1024
HEADER_SIZE = 84


def calculate_digest(buf, buf_type="none"):
    """Calculate MD5 digest
       In case the string is gziped, uncompress it.

    Args:
        buf(str): String to calculate digest
        buf_type: Type of data

    Returns:
        str: md5 digest
    """
    md5 = hashlib.md5()
    start = 0
    end = start + CHUNK_SIZE
    if buf_type.startswith("gzip"):
        d = zlib.decompressobj(16+zlib.MAX_WBITS)
    while start < len(buf):
        if buf_type.startswith("gzip"):
            md5.update(d.decompress(buf[start:end]))
        else:
            md5.update(buf[start:end])
        start += CHUNK_SIZE
        end += CHUNK_SIZE
    digest = md5.digest()
    return(digest)


def extract_partition(firmware, part, filename):
    """Extract partition from firmware file

    Args:
        firmware(file): Firmware file
        part(dict): Partition information
        filename(str): Output filename

    Returns:
        nothing
    """
    logging.debug("Writing firmware partition '{name}' to '{file}'".format(
        file=filename,
        name=part["name"]))
    # Map file to memory
    mm = mmap.mmap(firmware.fileno(), 0, prot=mmap.PROT_READ)
    with open(filename, "wb") as fp:
        mm.seek(part["start_pos"])
        bytes_read = 0
        while bytes_read < part["size"]:
            if bytes_read + CHUNK_SIZE < part["size"]:
                buf = mm.read(CHUNK_SIZE)
                bytes_read += CHUNK_SIZE
            else:
                buf = mm.read(part["size"] - bytes_read)
                bytes_read = part["size"]
            fp.write(buf)


def scan(firmware, verify):
    """Scan firmware file for partitions

    Args:
        firmware(file): Firmware file
        verify(bool): Verify MD5 of firmware file and partitions

    Returns:
        dict: Firmware information
    """
    # Map file to memory
    mm = mmap.mmap(firmware.fileno(), 0, prot=mmap.PROT_READ)

    # Find file magic
    ix = mm.find('TIMG')
    if ix == -1:
        logging.error("Header no found.")
        return None

    # Load firmware size and md5
    # size is little-endian unsigned int
    size = struct.unpack('<I', mm[4:8])[0]
    logging.debug("Firmware size: %s" % size)
    md5digest = mm[8:24]
    logging.debug("Firmware MD5 digest: %s" % md5digest)

    if verify is True:
        # Verify signature (firmware starts at 284)
        digest = calculate_digest(mm[284:])
        logging.debug("Firmware calculated MD5 digest: {digest}".format(
            digest=digest))
        if md5digest != digest:
            logging.error("Firmware file MD5 doesn't match.")
            raise Exception("Firmware file MD5 doesn't match")
    firmware = {
        "header": {
            "size": size,
            "md5": binascii.b2a_hex(md5digest),
            "verified": verify},
        "partitions": []}

    # Read file and find partitions
    while True:
        ix = mm.find('PIMG')
        if ix == -1:
            logging.info("No more partitions found.")
            break
        # Partition signature is usually 84 bytes long
        end = ix + HEADER_SIZE
        buf = mm[ix:end]
        mm.seek(ix+1)

        # size is little-endian unsigned int
        size = struct.unpack('<I', buf[4:8])[0]
        logging.debug("Partition size: %s" % size)
        start = ix + HEADER_SIZE
        end = start + size

        # md5sum of file/object
        md5sum = buf[8:24]
        logging.debug("Partition MD5 digest: %s" % md5sum)

        # Partition metadata
        ptype = str(buf[64:68]).strip('\0').decode("ascii", "ignore")
        pname = str(buf[24:40]).strip('\0').decode("ascii", "ignore")
        pdevice_name = str(buf[40:64]).strip('\0').decode("ascii", "ignore")
        if verify is True:
            digest = calculate_digest(mm[start:end], ptype)
            if digest != md5sum:
                raise Exception("Partition MD5 doesn't match.")

        firmware["partitions"].append({
            "header_pos": ix,
            "start_pos": start,
            "end_pos": end,
            "md5sum": binascii.b2a_hex(md5sum),
            "verified": verify,
            "size": size,
            "name": pname,
            "device_name": pdevice_name,
            "type": ptype})
        logging.debug("Index: %9s(%8x)\t \
                       Start: %9s(%8x)\t \
                       End: %9s(%8x)\t   \
                       Size: %9s\t       \
                       Name: %16s\t      \
                       Device: %24s\t    \
                       Type: %20s" %
                      (ix, ix,
                       start, start,
                       end, end,
                       size,
                       pname,
                       pdevice_name,
                       ptype))
    return(firmware)


def main():
    parser = argparse.ArgumentParser(
               description="Scan and extract TCL SmartTV Televisions firmware")
    parser.add_argument("--file",
                        type=file,
                        required=True)
    parser.add_argument("--verify",
                        type=str,
                        choices=["True", "False"],
                        default="True")
    parser.add_argument("--extract",
                        type=str,
                        choices=["True", "False"],
                        default="False")
    args = vars(parser.parse_args())
    # Convert str to bool (verify, extract)
    if args["verify"].lower() == "true":
        args["verify"] = True
    else:
        args["verify"] = False

    if args["extract"].lower() == "true":
        args["extract"] = True
    else:
        args["extract"] = False

    file_map = scan(args["file"], verify=args["verify"])
    print(json.dumps(file_map, indent=2))
    if args["extract"] is True:
        for part in file_map["partitions"]:
            filename = "{firmware}_{start}_{pname}".format(
                firmware=args["file"].name,
                pname=part["name"],
                start=part["start_pos"])
            extract_partition(args["file"], part, filename)


if __name__ == "__main__":
    main()
