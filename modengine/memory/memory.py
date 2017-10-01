import struct
from ctypes import create_string_buffer

from functions import *


class Memory(object):
    def __init__(self, pid):
        self.pid = pid
        #self.processHandle = OpenProcess(0x10, False, self.pid)
        self.processHandle = OpenProcess(PROCESS_ALL_ACCESS, False, self.pid)

    def read(self, address, type='uint', maxlen=50, errors='raise'):
        for i in range(5):
            try:
                if type == 's' or type == 'string':
                    s = self.read_bytes(int(address), bytes=maxlen)
                    news = ''
                    for c in s:
                        if c == '\x00':
                            continue
                            # return news
                        news += c
                    if errors == 'ignore':
                        return news
                    raise ProcessException('string > maxlen')
                else:
                    if type == 'bytes' or type == 'b':
                        return self.read_bytes(int(address), bytes=maxlen)
                    s, l = type_unpack(type)
                    b = self.read_bytes(int(address), bytes=l)
                    if len(b) < 4:
                        raise ProcessException("invalid value: '{}'".format(str(b)))
                    return struct.unpack(s, b)[0]
            except Exception:
                if i > 3:
                    raise

    def write(self, address, data, type='uint'):
        if type != 'bytes':
            s, l = type_unpack(type)
            return self.write_bytes(int(address), struct.pack(s, data))
        else:
            return self.write_bytes(int(address), data)

    def read_bytes(self, address, bytes=4, use_NtWow64ReadVirtualMemory64=False):
        if use_NtWow64ReadVirtualMemory64:
            if NtWow64ReadVirtualMemory64 is None:
                raise WindowsError("NtWow64ReadVirtualMemory64 is not available from a 64bit process")
            RpM = NtWow64ReadVirtualMemory64
        else:
            RpM = ReadProcessMemory

        address = int(address)
        buffer = create_string_buffer(bytes)
        bytesread = c_size_t(0)
        data = ''
        length = bytes
        while length:
            if RpM(self.processHandle, address, buffer, bytes, byref(bytesread)) or (
                        use_NtWow64ReadVirtualMemory64 and GetLastError() == 0):
                if bytesread.value:
                    data += buffer.raw[:bytesread.value]
                    length -= bytesread.value
                    address += bytesread.value
                if not len(data):
                    raise ProcessException('Error %s in ReadProcessMemory(%08x, %d, read=%d)' % (GetLastError(),
                                                                                                 address,
                                                                                                 length,
                                                                                                 bytesread.value))
                return data
            else:
                if GetLastError() == 299:  # only part of ReadProcessMemory has been done, let's return it
                    data += buffer.raw[:bytesread.value]
                    return data
                raise WinError()
                # data += buffer.raw[:bytesread.value]
                # length -= bytesread.value
                # address += bytesread.value
        return data

    def close(self):
        if self.processHandle:
            CloseHandle(self.processHandle)

    def VirtualProtectEx(self, base_address, size, protection):
        old_protect = c_ulong(0)
        if not kernel32.VirtualProtectEx(self.processHandle, base_address, size, protection, byref(old_protect)):
            raise ProcessException('Error: VirtualProtectEx(%08X, %d, %08X)' % (base_address, size, protection))
        return old_protect.value

    def write_bytes(self, address, data):
        address = int(address)
        # if not self.isProcessOpen:
        #    raise ProcessException("Can't write_bytes(%s, %s), process %s is not open" % (address, data, self.pid))
        buffer = create_string_buffer(data)
        sizeWriten = c_size_t(0)
        bufferSize = sizeof(buffer) - 1
        _address = address
        _length = bufferSize + 1
        old_protect = None
        try:
            old_protect = self.VirtualProtectEx(_address, _length, PAGE_EXECUTE_READWRITE)
        except:
            pass

        res = kernel32.WriteProcessMemory(self.processHandle, address, buffer, bufferSize, byref(sizeWriten))
        try:
            self.VirtualProtectEx(_address, _length, old_protect)
        except:
            pass

        return res

    def read_uint(self, address):
        return self.read(address=address, type='uint')

    def write_uint(self, address, data):
        return self.write(address=address, data=data, type='uint')

    def read_int(self, address):
        return self.read(address=address, type='int')

    def write_int(self, address, data):
        return self.write(address=address, data=data, type='int')

    def read_float(self, address):
        return self.read(address, 'float')

    def write_float(self, address, data):
        return self.write(address=address, data=data, type='float')

    def read_byte(self, address):
        return ord(self.read_bytes(address, 1))

    def write_byte(self, address, data):
        if type(data) == int:
            data = chr(data)
        return self.write_bytes(address=address, data=data)

    def write_string(self, address, data):
        # TODO: fix me
        return self.write_bytes(address, data)

    def read_string(self, address, size=50):
        return self.read(address=address, type="string", maxlen=size, errors='ignore').rstrip('\x00')

    def read_pointer(self, address):
        size = ctypes.sizeof(ctypes.c_void_p)
        packed = self.read_bytes(address, size)
        if len(packed) != size:
            raise ctypes.WinError()
        return struct.unpack('@P', packed)[0]

    @property
    def modules(self):
        modules = {}
        hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE, self.pid)
        module = Module32First(hSnapshot)
        while module is not None:
            modules[module.szModule] = module
            module = Module32Next(hSnapshot)
        return modules

    def getModule(self, modName):
        for name, module in self.modules.iteritems():
            if name.upper() == modName.upper():
                return module
        raise ProcessException("module %s not found" % modName)

    def getModuleAddress(self, modName):
        return self.getModule(modName).modBaseAddr
