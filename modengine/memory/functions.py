# from winappdbg/win32/kernel32.py:139

# Standard access rights
DELETE                      = (0x00010000L)
READ_CONTROL                = (0x00020000L)
WRITE_DAC                   = (0x00040000L)
WRITE_OWNER                 = (0x00080000L)
SYNCHRONIZE                 = (0x00100000L)
STANDARD_RIGHTS_REQUIRED    = (0x000F0000L)
STANDARD_RIGHTS_READ        = (READ_CONTROL)
STANDARD_RIGHTS_WRITE       = (READ_CONTROL)
STANDARD_RIGHTS_EXECUTE     = (READ_CONTROL)
STANDARD_RIGHTS_ALL         = (0x001F0000L)
SPECIFIC_RIGHTS_ALL         = (0x0000FFFFL)

# from winappdbg/win32/kernel32.py:199

# The values of PROCESS_ALL_ACCESS and THREAD_ALL_ACCESS were changed in Vista/2008
PROCESS_ALL_ACCESS_NT = (STANDARD_RIGHTS_REQUIRED | SYNCHRONIZE | 0xFFF)
PROCESS_ALL_ACCESS_VISTA = (STANDARD_RIGHTS_REQUIRED | SYNCHRONIZE | 0xFFFF)
THREAD_ALL_ACCESS_NT = (STANDARD_RIGHTS_REQUIRED | SYNCHRONIZE | 0x3FF)
THREAD_ALL_ACCESS_VISTA = (STANDARD_RIGHTS_REQUIRED | SYNCHRONIZE | 0xFFFF)
#if NTDDI_VERSION < NTDDI_VISTA:
#    PROCESS_ALL_ACCESS = PROCESS_ALL_ACCESS_NT
#    THREAD_ALL_ACCESS = THREAD_ALL_ACCESS_NT
#else:
PROCESS_ALL_ACCESS = PROCESS_ALL_ACCESS_VISTA
THREAD_ALL_ACCESS = THREAD_ALL_ACCESS_VISTA

# from memorpy/WinStructures.py:0

# Author: Nicolas VERDIER
# This file is part of memorpy.
#
# memorpy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# memorpy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with memorpy.  If not, see <http://www.gnu.org/licenses/>.

from ctypes import c_long, c_int, c_uint, c_char, c_void_p, c_ulong, c_ulonglong, windll, sizeof, \
    c_size_t, c_longlong, GetLastError, byref, WinError
from ctypes.wintypes import *

from defines import *

if sizeof(c_void_p) == 8:
    ULONG_PTR = c_ulonglong
else:
    ULONG_PTR = c_ulong


class SECURITY_DESCRIPTOR(Structure):
    _fields_ = [
        ('SID', DWORD),
        ('group', DWORD),
        ('dacl', DWORD),
        ('sacl', DWORD),
        ('test', DWORD)
    ]


PSECURITY_DESCRIPTOR = POINTER(SECURITY_DESCRIPTOR)


class MEMORY_BASIC_INFORMATION(Structure):
    _fields_ = [('BaseAddress', c_void_p),
                ('AllocationBase', c_void_p),
                ('AllocationProtect', DWORD),
                ('RegionSize', c_size_t),
                ('State', DWORD),
                ('Protect', DWORD),
                ('Type', DWORD)]


# https://msdn.microsoft.com/fr-fr/library/windows/desktop/aa366775(v=vs.85).aspx
class MEMORY_BASIC_INFORMATION64(Structure):
    _fields_ = [('BaseAddress', c_ulonglong),
                ('AllocationBase', c_ulonglong),
                ('AllocationProtect', DWORD),
                ('alignement1', DWORD),
                ('RegionSize', c_ulonglong),
                ('State', DWORD),
                ('Protect', DWORD),
                ('Type', DWORD),
                ('alignement2', DWORD)]


class SYSTEM_INFO(Structure):
    _fields_ = [('wProcessorArchitecture', WORD),
                ('wReserved', WORD),
                ('dwPageSize', DWORD),
                ('lpMinimumApplicationAddress', LPVOID),
                ('lpMaximumApplicationAddress', LPVOID),
                ('dwActiveProcessorMask', ULONG_PTR),
                ('dwNumberOfProcessors', DWORD),
                ('dwProcessorType', DWORD),
                ('dwAllocationGranularity', DWORD),
                ('wProcessorLevel', WORD),
                ('wProcessorRevision', WORD)]


class PROCESSENTRY32(Structure):
    _fields_ = [('dwSize', c_uint),
                ('cntUsage', c_uint),
                ('th32ProcessID', c_uint),
                ('th32DefaultHeapID', c_uint),
                ('th32ModuleID', c_uint),
                ('cntThreads', c_uint),
                ('th32ParentProcessID', c_uint),
                ('pcPriClassBase', c_long),
                ('dwFlags', DWORD),
                # ('dwFlags', ULONG_PTR),
                ('szExeFile', c_char * 260),
                ('th32MemoryBase', c_long),
                ('th32AccessKey', c_long)]


'''
class MODULEENTRY32(Structure):
    _fields_ = [('dwSize', c_uint),
     ('th32ModuleID', c_uint),
     ('th32ProcessID', c_uint),
     ('GlblcntUsage', c_uint),
     ('ProccntUsage', c_uint),
     ('modBaseAddr', c_uint),
     ('modBaseSize', c_uint),
     ('hModule', c_uint),
     ('szModule', c_char * 256),
     ('szExePath', c_char * 260)]
'''


class MODULEENTRY32(Structure):
    _fields_ = [
        ("dwSize", DWORD),
        ("th32ModuleID", DWORD),
        ("th32ProcessID", DWORD),
        ("GlblcntUsage", DWORD),
        ("ProccntUsage", DWORD),
        ("modBaseAddr", LPVOID),  # BYTE*
        ("modBaseSize", DWORD),
        ("hModule", HMODULE),
        ("szModule", TCHAR * (MAX_MODULE_NAME32 + 1)),
        ("szExePath", TCHAR * MAX_PATH),
    ]


class THREADENTRY32(Structure):
    _fields_ = [('dwSize', c_uint),
                ('cntUsage', c_uint),
                ('th32ThreadID', c_uint),
                ('th32OwnerProcessID', c_uint),
                ('tpBasePri', c_uint),
                ('tpDeltaPri', c_uint),
                ('dwFlags', c_uint)]


class TH32CS_CLASS(object):
    INHERIT = 2147483648L
    SNAPHEAPLIST = 1
    SNAPMODULE = 8
    SNAPMODULE32 = 16
    SNAPPROCESS = 2
    SNAPTHREAD = 4
    ALL = 2032639


Process32First = windll.kernel32.Process32First
Process32First.argtypes = [c_void_p, POINTER(PROCESSENTRY32)]
Process32First.rettype = c_int
Process32Next = windll.kernel32.Process32Next
Process32Next.argtypes = [c_void_p, POINTER(PROCESSENTRY32)]
Process32Next.rettype = c_int

CreateToolhelp32Snapshot = windll.kernel32.CreateToolhelp32Snapshot
CreateToolhelp32Snapshot.reltype = c_long
CreateToolhelp32Snapshot.argtypes = [c_int, c_int]

CloseHandle = windll.kernel32.CloseHandle
CloseHandle.argtypes = [c_void_p]
CloseHandle.rettype = c_int

OpenProcess = windll.kernel32.OpenProcess
OpenProcess.argtypes = [c_void_p, c_int, c_long]
OpenProcess.rettype = c_long
OpenProcessToken = windll.advapi32.OpenProcessToken
OpenProcessToken.argtypes = (HANDLE, DWORD, POINTER(HANDLE))
OpenProcessToken.restype = BOOL

ReadProcessMemory = windll.kernel32.ReadProcessMemory
ReadProcessMemory.argtypes = [HANDLE, LPCVOID, LPVOID, c_size_t, POINTER(c_size_t)]
ReadProcessMemory = windll.kernel32.ReadProcessMemory

WriteProcessMemory = windll.kernel32.WriteProcessMemory
WriteProcessMemory.argtypes = [HANDLE, LPVOID, LPCVOID, c_size_t, POINTER(c_size_t)]
WriteProcessMemory.restype = BOOL

if sizeof(c_void_p) == 8:
    NtWow64ReadVirtualMemory64 = None
else:
    try:
        NtWow64ReadVirtualMemory64 = windll.ntdll.NtWow64ReadVirtualMemory64
        NtWow64ReadVirtualMemory64.argtypes = [HANDLE, c_longlong, LPVOID, c_ulonglong, POINTER(
            c_ulong)]  # NTSTATUS (__stdcall *NtWow64ReadVirtualMemory64)(HANDLE ProcessHandle, PVOID64 BaseAddress, PVOID Buffer, ULONGLONG BufferSize, PULONGLONG NumberOfBytesRead);
        NtWow64ReadVirtualMemory64.restype = BOOL
    except:
        NtWow64ReadVirtualMemory64 = None

VirtualQueryEx = windll.kernel32.VirtualQueryEx
VirtualQueryEx.argtypes = [HANDLE, LPCVOID, POINTER(MEMORY_BASIC_INFORMATION), c_size_t]
VirtualQueryEx.restype = c_size_t

# VirtualQueryEx64 = windll.kernel32.VirtualQueryEx
# VirtualQueryEx64.argtypes = [HANDLE, LPCVOID, POINTER(MEMORY_BASIC_INFORMATION64), c_size_t]
# VirtualQueryEx64.restype = c_size_t

PAGE_EXECUTE_READWRITE = 64
PAGE_EXECUTE_READ = 32
PAGE_READONLY = 2
PAGE_READWRITE = 4
PAGE_NOCACHE = 512
PAGE_WRITECOMBINE = 1024
PAGE_GUARD = 256

MEM_COMMIT = 4096
MEM_FREE = 65536
MEM_RESERVE = 8192

UNPROTECTED_DACL_SECURITY_INFORMATION = 536870912
DACL_SECURITY_INFORMATION = 4


class ProcessException(Exception):
    pass


kernel32 = windll.kernel32
psapi = windll.psapi

'''
Module32First = windll.kernel32.Module32First
Module32First.argtypes = [c_void_p, POINTER(MODULEENTRY32)]
Module32First.rettype = c_int
Module32Next = windll.kernel32.Module32Next
Module32Next.argtypes = [c_void_p, POINTER(MODULEENTRY32)]
Module32Next.rettype = c_int
'''
LPMODULEENTRY32 = POINTER(MODULEENTRY32)


# from winappdbg\win32\kernel32.py:4316

# BOOL WINAPI Module32First(
#   __in     HANDLE hSnapshot,
#   __inout  LPMODULEENTRY32 lpme
# );
def Module32First(hSnapshot):
    _Module32First = windll.kernel32.Module32First
    _Module32First.argtypes = [HANDLE, LPMODULEENTRY32]
    _Module32First.restype = bool

    me = MODULEENTRY32()
    me.dwSize = sizeof(MODULEENTRY32)
    success = _Module32First(hSnapshot, byref(me))
    if not success:
        if GetLastError() == ERROR_NO_MORE_FILES:
            return None
        raise WinError()
    return me


# BOOL WINAPI Module32Next(
#   __in     HANDLE hSnapshot,
#   __out  LPMODULEENTRY32 lpme
# );
def Module32Next(hSnapshot, me=None):
    _Module32Next = windll.kernel32.Module32Next
    _Module32Next.argtypes = [HANDLE, LPMODULEENTRY32]
    _Module32Next.restype = bool

    if me is None:
        me = MODULEENTRY32()
    me.dwSize = sizeof(MODULEENTRY32)
    success = _Module32Next(hSnapshot, byref(me))
    if not success:
        if GetLastError() == ERROR_NO_MORE_FILES:
            return None
        raise ctypes.WinError()
    return me

# typedef struct _MODULEINFO {
#   LPVOID lpBaseOfDll;
#   DWORD  SizeOfImage;
#   LPVOID EntryPoint;
# } MODULEINFO, *LPMODULEINFO;
class MODULEINFO(Structure):
    _fields_ = [
        ("lpBaseOfDll",     LPVOID),    # remote pointer
        ("SizeOfImage",     DWORD),
        ("EntryPoint",      LPVOID),    # remote pointer
]
LPMODULEINFO = POINTER(MODULEINFO)

# BOOL WINAPI GetModuleInformation(
#   __in   HANDLE hProcess,
#   __in   HMODULE hModule,
#   __out  LPMODULEINFO lpmodinfo,
#   __in   DWORD cb
# );
def GetModuleInformation(hProcess, hModule, lpmodinfo = None):
    _GetModuleInformation = windll.psapi.GetModuleInformation
    _GetModuleInformation.argtypes = [HANDLE, HMODULE, LPMODULEINFO, DWORD]
    _GetModuleInformation.restype = bool
    _GetModuleInformation.errcheck = RaiseIfZero

    if lpmodinfo is None:
        lpmodinfo = MODULEINFO()
    _GetModuleInformation(hProcess, hModule, byref(lpmodinfo), sizeof(lpmodinfo))
    return lpmodinfo

PROCESS_QUERY_INFORMATION         = 0x0400
PROCESS_VM_READ                   = 0x0010
def get_size_and_entry_point(hProcess, base): # entrypoint!

        try:
            mi     = GetModuleInformation(hProcess, base)
            return(mi.SizeOfImage, mi.EntryPoint)
        except WindowsError, e:
            raise Exception(
                "Cannot get size and entry point of module reason: %s"\
                % (e.strerror), RuntimeWarning)


# from winappdbg\win32\kernel32.py:1970

#--- Toolhelp library defines and structures ----------------------------------

TH32CS_SNAPHEAPLIST = 0x00000001
TH32CS_SNAPPROCESS  = 0x00000002
TH32CS_SNAPTHREAD   = 0x00000004
TH32CS_SNAPMODULE   = 0x00000008
TH32CS_INHERIT      = 0x80000000
TH32CS_SNAPALL      = (TH32CS_SNAPHEAPLIST | TH32CS_SNAPPROCESS | TH32CS_SNAPTHREAD | TH32CS_SNAPMODULE)


# from memorpy/utils.py

def type_unpack(type):
    """ return the struct and the len of a particular type """
    type = type.lower()
    s = None
    l = None
    if type == 'short':
        s = 'h'
        l = 2
    elif type == 'ushort':
        s = 'H'
        l = 2
    elif type == 'int':
        s = 'i'
        l = 4
    elif type == 'uint':
        s = 'I'
        l = 4
    elif type == 'long':
        s = 'l'
        l = 4
    elif type == 'ulong':
        s = 'L'
        l = 4
    elif type == 'float':
        s = 'f'
        l = 4
    elif type == 'double':
        s = 'd'
        l = 8
    else:
        raise TypeError('Unknown type %s' % type)
    return ('<' + s, l)
