import econ_pb2
import zlib

import sys
import struct

# All you need to generate a gen code
def generate_inspect(proto):
    # Needs to be prefixed with a null byte
    buffer = bytearray([0]) 
    buffer.extend(proto.SerializeToString())

    # calculate the checksum
    crc = zlib.crc32(buffer)
    xored_crc = (crc & 0xFFFF) ^ (proto.ByteSize() * crc)
    
    buffer.extend((xored_crc & 0xFFFFFFFF).to_bytes(length=4, byteorder='big'))

    # Must be upper case
    return buffer.hex().upper()

# Very primitive arg parsing
class ArgParser:
    def __init__(self) -> None:
        self.args = sys.argv[1:]

    @property
    def count(self):
        return len(self.args)

    def pop_string(self, default_value=None):
        if len(self.args) > 0:
            return self.args.pop(0)
        return default_value
    
    def pop_int(self, default_value=None):
        if len(self.args) > 0:
            try:
                return int(self.args.pop(0))
            except:
                return default_value
        return default_value
    
    def pop_float(self, default_value=None):
        if len(self.args) > 0:
            try:
                return float(self.args.pop(0))
            except:
                return default_value
        return default_value

ALLOWED_COMMANDS = ["gen", "gengl", "genrarity"]

def main():
    
    input_args = sys.argv[1:]
    args = ArgParser()
    
    # Not too proud of this
    command_name = args.pop_string()
    command_name = command_name.lower()

    # You can modify other parameters to your liking (check econ.proto for all variables)
    proto = econ_pb2.CEconItemPreviewDataBlock()

    proto.rarity = args.pop_int(0)
    proto.defindex = args.pop_int(1)
    proto.paintindex = args.pop_int(0)
    proto.paintseed = args.pop_int(0)
    paint_wear = args.pop_float(0)

    # Is there a better way to do it in python? 
    proto.paintwear = int.from_bytes(struct.pack(">f", paint_wear), "big")

    sticker1_id = args.pop_int()
    sticker1_wear = args.pop_float(0)

    sticker2_id = args.pop_int()
    sticker2_wear = args.pop_float(0)

    sticker3_id = args.pop_int()
    sticker3_wear = args.pop_float(0)

    sticker4_id = args.pop_int()
    sticker4_wear = args.pop_float(0)

    sticker_string = ""

    if sticker1_id is not 0:
        sticker = proto.stickers.add()
        sticker.slot = 0
        sticker.sticker_id = sticker1_id
        sticker.wear = sticker1_wear

        sticker_string += f"{sticker1_id} {sticker1_wear}"
    
    if sticker2_id is not 0:
        sticker = proto.stickers.add()
        sticker.slot = 1
        sticker.sticker_id = sticker2_id
        sticker.wear = sticker2_wear

        sticker_string += f"{sticker2_id} {sticker2_wear}"
    
    if sticker3_id is not 0:
        sticker = proto.stickers.add()
        sticker.slot = 2
        sticker.sticker_id = sticker3_id
        sticker.wear = sticker3_wear

        sticker_string += f"{sticker3_id} {sticker3_wear}"
    
    if sticker4_id is not 0:
        sticker = proto.stickers.add()
        sticker.slot = 3
        sticker.sticker_id = sticker4_id
        sticker.wear = sticker4_wear

        sticker_string += f"{sticker4_id} {sticker4_wear}"


    generated_payload = generate_inspect(proto)

    print(f"csgo_econ_action_preview {generated_payload} : steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20{generated_payload} : !gen {proto.defindex} {proto.paintindex} {proto.paintseed} {paint_wear} {sticker_string}")

if __name__ == "__main__":
    main()