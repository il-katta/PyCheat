import struct

from winappdbg import Process, HexOutput, System


# import ctypes
# import psutil

class MemoryManager(Process):
    def __init__(self, process_name, wait_for_process=False):
        pid = MemoryManager.find_pid(process_name, wait_for_process)
        super(MemoryManager, self).__init__(pid)

    @staticmethod
    def find_pid(process_name, wait_for_process=False):
        # for proc in psutil.process_iter():
        #    if proc.name().lower() == process_name.lower():
        #        return proc.pid
        # raise Exception("process not found")

        system = System()
        # for process in system:
        #    if process.get_image_name() and \
        #                    basename(process.get_filename()).lower() == process_name.lower():
        #        return process.get_pid()
        # if wait_for_process:
        #    return MemoryManager.find_pid(process_name, True)
        # raise Exception("process not found")


        process = system.find_processes_by_filename(process_name)

        if not process:
            if wait_for_process:
                return MemoryManager.find_pid(process_name, True)
            raise Exception("Process '%s' not found" % process_name)

        if len(process) > 1:
            raise Exception("Too many processes found:")
        return process[0][0].get_pid()

    '''
    def read_pointer(process, address):
        # return process.read_pointer(address)
        size = ctypes.sizeof(ctypes.c_void_p)
        packed = process.read(address, size)
        if len(packed) != size:
            raise ctypes.WinError()
        return struct.unpack('@P', packed)[0]
    '''

    @staticmethod
    def print_address(name, int_value):
        print "%s : %s" % (name, HexOutput.address(int_value))

    def get_module_address(self, moduleName):
        self.scan()
        self.scan_modules()

        for module in self.iter_modules():
            if module.get_name().lower() == moduleName.lower():
                return (
                    module.get_base(),
                    module.get_size()
                )

    def memory_search_aob(self, module, aob):
        # Search for the string in the process memory.
        (mod_addr, mod_size) = self.get_module_address(module)
        # module = process.get_main_module()
        # mod_addr = module.get_base()
        # mod_size = module.get_size()
        #results = self.search_hexa(aob, mod_addr, mod_addr + mod_size)
        results = self.search(aob, mod_addr, mod_addr + mod_size)
        for address in results:
            print(address)
            bits = self.get_bits()
            print HexOutput.address(address[0], bits)
        return results[0][0]

    def get_pointer_address(self, basePointer, offsets):
        v = self.read_pointer(basePointer)
        for offset in offsets[:-1]:
            v_ = self.read_pointer(v + offset)
            self.print_address(
                "[%s + %s] ->" % (HexOutput.address(v), HexOutput.address(offset)),
                v_
            )
            v = v_
        self.print_address(
            "%s + %s = " % (HexOutput.address(v), HexOutput.address(offsets[-1:][0])),
            v + offsets[-1:][0]
        )
        return v + offsets[-1:][0]

    def write_string(self, address, value, max_length=None):
        # TODO
        pass
        #raise NotImplementedError()

    def read_string(self, address, size, fUnicode=False):
        super(MemoryManager, self).read_string(address, size)

    def write_bool(self, address, value, true_value=1, false_value=0):
        if value:
            value = true_value
        else:
            value = false_value
        self.write_int(address, value)

    def read_bool(self, address, true_value=1, false_value=0):
        v = self.read_int(address)
        if v is not None:
            if v == true_value:
                return True
            if v == false_value:
                return False
        return None

    def write_float(self, address, value):
        return self.write(address, struct.pack('<f', value))

    '''
    def _write_float(self, address, value):
        """Reads 4 byte from an area of memory in a specified process.
        The entire area to be read must be accessible or the operation fails.
        Unpack the value using struct.unpack('<f')
        https://msdn.microsoft.com/en-us/library/windows/desktop/ms680553%28v=vs.85%29.aspx
        :param handle: A handle to the process with memory that is being read.
                       The handle must have PROCESS_VM_READ access to the process.
        :param address: An address of the region of memory to be freed.
        :type handle: ctypes.wintypes.HANDLE
        :type address: int
        :return: If the function succeeds, returns the value read
        :rtype: float
        :raise: TypeError if address is not a valid integer
        :raise: WinAPIError if ReadProcessMemory failed
        """
        src = ctypes.c_float(value)
        length = struct.calcsize('f')
        # res = write_bytes(handle, address, ctypes.addressof(src), length)
        # write_bytes(handle, address, src, length):
        src = ctypes.addressof(src)
        address = int(address)
        if not isinstance(address, int) and not isinstance(address, long):
            raise TypeError('Address must be int: {}, get {}'.format(address, type(address)))
        dst = ctypes.cast(address, ctypes.c_char_p)
        ctypes.windll.kernel32.SetLastError(0)
        handle = self.get_handle(win32.PROCESS_VM_WRITE |
                                    win32.PROCESS_VM_OPERATION |
                                    win32.PROCESS_QUERY_INFORMATION)
        res = ctypes.windll.kernel32.WriteProcessMemory(handle, dst, src, length, 0x0)
        error_code = ctypes.windll.kernel32.GetLastError()
        if error_code:
            ctypes.windll.kernel32.SetLastError(0)
            raise Exception(error_code)
        return res
    '''
