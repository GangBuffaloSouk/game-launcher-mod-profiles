#pragma once

#include <string>

namespace glmp {

// Injects a DLL into a live process by PID using the classic
// OpenProcess/VirtualAllocEx/WriteProcessMemory/CreateRemoteThread path.
// Returns 0 on success, a Win32 error code on failure.
int inject_dll(unsigned long pid, const std::string& dll_path);

}  // namespace glmp