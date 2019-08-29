from conans import ConanFile
from conans import tools
import subprocess
import os
import codecs

class GcovrConan(ConanFile):
    name = "gcovr_installer"
    version = "4.1"
    url = "https://github.com/bincrafters/conan-protoc_installer"
    homepage = "http://gcovr.com"
    gitpage = "https://github.com/gcovr/gcovr"
    topics = ("gcovr", "gcov reporting", "coverage")
    author = "mjvk <>"
    description = ("gcovr can process output from gcov")
    license = "MIT"
    settings = "os_build", "arch_build"
    _source_subfolder = "sourcefolder"
    
    def _makeAbsoluteImport(self,input_name):
        tmp_name = input_name + ".bak"
        with codecs.open(input_name, 'r', encoding='utf8') as fi, \
            codecs.open(tmp_name, 'w', encoding='utf8') as fo:

            for line in fi:
                fo.write(line.replace("from .", "from gcovr."))

        os.remove(input_name) # remove original
        os.rename(tmp_name, input_name) # rename temp to original name
                
    def source(self):
        tools.get("{0}/archive/{1}.tar.gz".format(self.gitpage, self.version))
        os.rename("gcovr-%s" % self.version, self._source_subfolder)
        
    def build(self):
        subprocess.call("pip install pyinstaller lxml", shell=True)
        mainfilename = os.path.join(self._source_subfolder,"gcovr","__main__.py")
        self._makeAbsoluteImport(mainfilename)
        subprocess.call('pyinstaller %s --name gcovr --onefile --workpath %s --distpath %s --specpath %s' % (mainfilename, os.path.join(self.build_folder,"build"), os.path.join(self.build_folder,"bin"), self.build_folder), shell=True)

    def package(self):
        self.copy("*gcovr", dst="bin", src="bin", keep_path=False)
        self.copy("*gcovr.exe", dst="bin", src="bin", keep_path=False)

    def deploy(self):
        self.copy("*", src="bin", dst="bin")
        
    def package_id(self):
        self.info.include_build_settings()
    
    def package_info(self):
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
        