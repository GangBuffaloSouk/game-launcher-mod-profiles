#include "injector.hpp"

#ifdef _WIN32
#include <windows.h>
#include <tlhelp32.h>
#endif

namespace glmp {

#ifdef _WIN32

int inject_dll(unsigned long pid, const std::string& dll_path) {
    const DWORD access = PROCESS_VM_WRITE | PROCESS_VM_OPERATION |
                         PROCESS_CREATE_THREAD | PROCESS_QUERY_INFORMATION;
    HANDLE proc = OpenProcess(access, FALSE, static_cast<DWORD>(pid));
    if (!proc) return static_cast<int>(GetLastError());

    const SIZE_T len = dll_path.size() + 1;
    LPVOID remote = VirtualAllocEx(proc, nullptr, len, MEM_COMMIT | MEM_RESERVE,
                                   PAGE_READWRITE);
    if (!remote) {
        const int err = static_cast<int>(GetLastError());
        CloseHandle(proc);
        return err;
    }

    if (!WriteProcessMemory(proc, remote, dll_path.c_str(), len, nullptr)) {
        const int err = static_cast<int>(GetLastError());
        VirtualFreeEx(proc, remote, 0, MEM_RELEASE);
        CloseHandle(proc);
        return err;
    }

    HMODULE kernel32 = GetModuleHandleA("kernel32.dll");
    auto load_lib = reinterpret_cast<LPTHREAD_START_ROUTINE>(
        GetProcAddress(kernel32, "LoadLibraryA"));

    HANDLE thread = CreateRemoteThread(proc, nullptr, 0, load_lib, remote, 0, nullptr);
    if (!thread) {
        const int err = static_cast<int>(GetLastError());
        VirtualFreeEx(proc, remote, 0, MEM_RELEASE);
        CloseHandle(proc);
        return err;
    }

    WaitForSingleObject(thread, 5000);
    DWORD exit_code = 0;
    GetExitCodeThread(thread, &exit_code);

    CloseHandle(thread);
    VirtualFreeEx(proc, remote, 0, MEM_RELEASE);
    CloseHandle(proc);

    // LoadLibrary returns the HMODULE as the thread exit code; 0 means failure.
    return exit_code == 0 ? 1 : 0;
}

#else

int inject_dll(unsigned long, const std::string&) {
    return 1;