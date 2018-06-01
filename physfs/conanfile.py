from conans import ConanFile, CMake, tools


class PhysfsConan(ConanFile):
    name = "physfs"
    version = "3.0.1"
    license = "zlib"
    url = "https://github.com/eXpl0it3r/conan-packages"
    description = "PhysicsFS is a library to provide abstract access to various archives."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"

    def source(self):
        tools.get("https://hg.icculus.org/icculus/physfs/archive/release-%s.zip" % self.version)
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it properly
        tools.replace_in_file("physfs-release-%s/CMakeLists.txt" % self.version, "project(PhysicsFS)",
                              """project(PhysicsFS)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()""")

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="physfs-release-%s" % self.version)
        cmake.build()

    def package(self):
        self.copy("physfs.h", dst="include", src="physfs-release-%s/src" % self.version)
        self.copy("*physfs.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["physfs"]
