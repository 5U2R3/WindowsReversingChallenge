#TODO write a description for this script
#@author 
#@category _NEW_
#@keybinding 
#@menupath 
#@toolbar 
#@runtime PyGhidra


#TODO Add User Code Here

memory = currentProgram.getMemory()

def rol(value, shift, bit_size):
    value = value & ((1 << bit_size) - 1)
    return ((value << shift) | (value >> (bit_size - shift))) & (( 1 << bit_size) - 1)

def main():
    start_offset = "0x140003238"
    end_offset = "0x14000325e"
    start_addr = toAddr(start_offset)
    end_addr = toAddr(end_offset)
    read_length = end_addr.subtract(start_addr)
    flag = ''
    data_array = []
    shift = 5
    bit_size = 8
    for i in range(read_length):
        byte_value = memory.getByte(start_addr.add(i)) & 0xFF
        data_array.append(byte_value)
    for i in range(len(data_array)):
        data_array[i] = rol(data_array[i], shift, bit_size)
        flag += chr(data_array[i])
    print(flag)

if __name__ == "__main__":
    main()
