import re

from functions import get_size_and_entry_point
from memory import Memory, ProcessException


class MemoryManager(Memory):
    pid = None

    def __init__(self, process_name, wait_for_process=False):
        self.pid = MemoryManager.find_pid(process_name, wait_for_process)
        super(MemoryManager, self).__init__(self.pid)

    @staticmethod
    def find_pid(process_name, wait_for_process=False):
        try:
            import psutil

            for proc in psutil.process_iter():
                if proc.name().lower() == process_name.lower():
                    return proc.pid
            if wait_for_process:
                return MemoryManager.find_pid(process_name, wait_for_process=True)
            raise ProcessException("process not found")
        except ImportError:
            pass
        try:
            import System.Diagnostics
            process_name = process_name.split('.')[0]
            processes = System.Diagnostics.Process.GetProcessesByName(process_name)
            if processes.Count == 0:
                if wait_for_process:
                    return MemoryManager.find_pid(process_name, wait_for_process=True)
                raise ProcessException("process not found")
            return processes.Get(0).Id
        except ImportError:
            pass

        try:
            from get_pid import get_pid
            return get_pid(process_name)
        except ImportError:
            pass

        raise Exception("no method to get pid")

    def get_pointer_address(self, basePointer, offsets):
        v = self.read_pointer(basePointer)
        for offset in offsets[:-1]:
            v = self.read_pointer(v + offset)
        return v + offsets[-1:][0]

    def write_bool(self, address, value, true_value=1, false_value=0):
        if value:
            value = true_value
        else:
            value = false_value
        self.write_byte(address, value)

    def read_bool(self, address, true_value=1, false_value=0):
        v = self.read_byte(address)
        if v is not None:
            if v == true_value:
                return True
            if v == false_value:
                return False
        return None

    def getProcedureAddress(self, base):
        (_,entrypoiny) = get_size_and_entry_point(self.processHandle, base)
        return entrypoiny

    def resolve_label(self, label):
        (module, procedure, offset) = self.split_label(label)
        module_addr = self.getModuleAddress(module)

        if procedure:
            if procedure == 'start':
                module_addr = self.getProcedureAddress(module_addr)
            else:
                raise NotImplementedError("procedure: %s" % procedure)
        else:
            procedure = 0
        #print("LABEL: {} | module: {}, offset: {}".format(label, module_addr, offset))
        return module_addr + offset

    def is_hex(self, hexstr):
        pattern = '(0[xX])?[0-9a-fA-F]+'
        return re.match(pattern, hexstr)

    def to_int(self, hexStr):
        return int(hexStr, 16)

    def split_label(self, label):
        '''
        split simple label: like 'MODULE.EXE+0x123' or 'MODULE.EXE+FF00'
        :param label: 
        :return: tuple of module (str) and offset (int)
        '''
        label = label.replace(' ', '')
        label = label.replace('\t', '')
        label = label.replace('\r', '')
        label = label.replace('\n', '')

        regexp = re.compile("([A-Za-z0-9.]+)(!(\w+))?(\+([0-9a-fA-F]+))?")

        if not regexp.match(label):
            raise ValueError("invalid label: '%s'" % label)

        (_, module, _, procedure, _, offset, _) = regexp.split(label)

        offset = self.to_int(offset)

        return (module, procedure, offset)
        '''
        module = None
        offset = None
        procedure = None

        if "+" in label:
            module, offset = label.split('+')
            if "!" in module:
                module, procedure = module.split('!')
        elif "!" in label:
            module, procedure = label.split('!')
        if "!" not in label and "+" not in label:
            module = label
            offset = "0x0"

        if not self.is_hex(offset):
            raise ValueError("invalid label: '%s'" % label)

        offset = self.to_int(offset)

        return (module, procedure, offset)
        '''
