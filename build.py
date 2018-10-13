import os
import shutil
import subprocess
import sys



def root_path():
   return os.path.dirname(os.path.realpath(__file__))


def search_arguments(needle):
   found = False

   for argument in sys.argv[1:]:
      if argument == needle:
         found = True
         break

   return found


def configuration():
   return "Release" if search_arguments("--release") else "Debug"


def build_path():
   return os.path.join(root_path(), configuration())


def skyrim_path():
   return r"C:\Program Files (x86)\Steam\steamapps\common\Skyrim"


def papyrus_compiler_path():
   return os.path.join(skyrim_path(), r"Papyrus Compiler\PapyrusCompiler.exe")


def skyrim_compiled_scripts_path():
   return os.path.join(skyrim_path(), r"Data\scripts")


def skyrim_scripts_path():
   return os.path.join(skyrim_compiled_scripts_path(), r"Source")


def scripts_path():
   return os.path.join(root_path(), r"plugin\scripts")


def compiled_scripts_path():
   return os.path.join(build_path(), "scripts")


def msbuild_path():
   return r"C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\MSBuild\15.0\Bin\MSBuild.exe"


def run_command(command):
   result = subprocess.run(
      command,
      shell=True,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE
   )

   if result.returncode != 0:
      print("--- The following command failed with code:", result.returncode)
      print(command.strip())
      print("--- Standard output:")
      print(result.stdout.decode("utf-8"))
      print("--- Error output")
      print(result.stderr.decode("utf-8"))
      sys.exit(1)


def compile_plugin():
   project_path = os.path.join(root_path(), "plugin.sln")

   command = """ \
      "{compiler_path}" \
      "{project_path}" \
      /property:Configuration={configuration}  \
   """.format(
      compiler_path=msbuild_path(),
      project_path=project_path,
      configuration=configuration()
   )

   run_command(command)


def compile_scripts():
   output_path = compiled_scripts_path()
   os.makedirs(output_path, exist_ok=True)

   command = """ \
      "{compiler_path}" \
      "{scripts_path}" \
      -all \
      -flags="TESV_Papyrus_Flags.flg" \
      -import="{skyrim_scripts_path};{scripts_path}" \
      -output="{output_path}" \
   """.format(
      compiler_path=papyrus_compiler_path(),
      skyrim_scripts_path=skyrim_scripts_path(),
      scripts_path=scripts_path(),
      output_path=output_path
   )

   run_command(command)


def build():
   compile_plugin()
   compile_scripts()


def copy_plugin():
   plugin_path = os.path.join(build_path(), "plugin.dll")
   plugins_path = os.path.join(skyrim_path(), r"Data\skse\plugins")

   os.makedirs(plugins_path, exist_ok=True)
   shutil.copy2(plugin_path, plugins_path)


def copy_files(source, destination):
   with os.scandir(source) as entries:
      for entry in entries:
         if entry.is_file():
            shutil.copy2(entry.path, destination)


def copy_script_sources():
   skyrim_scripts_directory = skyrim_scripts_path()
   os.makedirs(skyrim_scripts_directory, exist_ok=True)
   copy_files(scripts_path(), skyrim_scripts_directory)


def copy_compiled_scripts():
   skyrim_compiled_scripts_directory = skyrim_compiled_scripts_path()
   os.makedirs(skyrim_compiled_scripts_directory, exist_ok=True)
   copy_files(compiled_scripts_path(), skyrim_compiled_scripts_directory)


def install():
   copy_plugin()
   copy_script_sources()
   copy_compiled_scripts()



if __name__ == "__main__":
   if search_arguments("install"):
      install()
   else:
      build()
