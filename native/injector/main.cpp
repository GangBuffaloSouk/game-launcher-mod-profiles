// glmp_injector — CLI shim: glmp_injector.exe --pid <pid> --dll <path>
// Called by launcher/drivers/native_injector.py. Exit 0 on success.
#include "injector.hpp"

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>

int main(int argc, char** argv) {
    int pid = 0;
    std::string dll_path;

    for (int i = 1; i < argc; ++i) {
        if (std::strcmp(argv[i], "--pid") == 0 && i + 1 < argc) {
            pid = std::atoi(argv[++i]);
        } else if (std::strcmp(argv[i], "--dll") == 0 && i + 1 < argc) {
            dll_path = argv[++i];
        }
    }

    if (pid <= 0 || dll_path.empty()) {
        std::fprintf(stderr, "usage: glmp_injector --pid <pid> --dll <path>\n");
        return 2;
    }

    const int rc = glmp::inject_dll(static_cast<unsigned long>(pid), dll_path);
    if (rc != 0) {
        std::fprintf(stderr, "inject failed for pid %d: code %d\n", pid, rc);
        return 1;
    }
    return 0;
}