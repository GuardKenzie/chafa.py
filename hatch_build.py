from hatchling.builders.hooks.plugin.interface import BuildHookInterface
import sys
from pathlib import Path


class CustomBuildHook(BuildHookInterface):
    
    def initialize(self, version, build_data) -> None:

        build_data["infer_tag"] = True
        libs_folder = Path("src/chafa/libs/")

        build_data["pure_python"] = False

        if sys.platform == "linux":
            chafa_glob = list(Path("libs/linux").glob("*chafa*.so"))

            if len(chafa_glob) > 1:
                raise FileNotFoundError("Too many files matched the glob pattern 'libs/linux/*chafa*.dll'")

            elif len(chafa_glob) < 1:
                raise FileNotFoundError("No file matched the glob pattern 'libs/linux/*chafa*.dll'")

            build_data["force_include"][str(chafa_glob[0])] = str(libs_folder / "libchafa.dll")

            build_data["force_include"][str(chafa_glob[0])] = str(libs_folder / "libchafa.so")


        elif sys.platform == "win32":
            # Add all the dlls we need to the wheel if we are building for windows

            # Find the chafa library
            chafa_glob = Path("libs/windows").glob("*chafa*.dll")
            chafa_glob = list(chafa_glob)

            if len(chafa_glob) > 1:
                raise FileNotFoundError("Too many files matched the glob pattern 'libs/windows/*chafa*.dll'")

            elif len(chafa_glob) < 1:
                raise FileNotFoundError("No file matched the glob pattern 'libs/windows/*chafa*.dll'")

            build_data["force_include"][str(chafa_glob[0])] = str(libs_folder / "libchafa.dll")
            
            # Find everything else
            not_chafa_glob = [p for p in Path("libs/windows").glob("*.dll") if not "chafa" in p.name]

            for file in not_chafa_glob:
                build_data["force_include"][str(file)] = str(libs_folder / file.name)
        
        else:
            chafa_glob = Path("libs/macos").glob("*chafa*.dylib")
            chafa_glob = chafa_glob = [p for p in chafa_glob if not ".0" in p.name]
            
            print(chafa_glob)

            if len(chafa_glob) > 1:
                raise FileNotFoundError("Too many files matched the glob pattern 'libs/macos/*chafa*.dylib'")

            elif len(chafa_glob) < 1:
                raise FileNotFoundError("No file matched the glob pattern 'libs/macos/*chafa*.dylib'")

            build_data["force_include"][str(chafa_glob[0])] = str(libs_folder / "libchafa.dylib")
            
            # Find everything else
            not_chafa_glob = [p for p in Path("libs/macos").glob("*.dylib") if not "chafa" in p.name]

            for file in not_chafa_glob:
                build_data["force_include"][str(file)] = str(libs_folder / file.name)



