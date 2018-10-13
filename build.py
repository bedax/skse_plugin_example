import os
import subprocess
import sys



def base_path():
   return os.path.dirname(os.path.realpath(__file__))


def release_configuration():
   release = False

   for arg in sys.argv[1:]:
      if arg.lower() == "release":
         release = True
         break

   return release


def configuration_string():
   return "Release" if release_configuration() else "Debug"


def build_path():
   return os.path.join(base_path(), configuration_string())


def skyrim_path():
   return r"C:\Program Files (x86)\Steam\steamapps\common\Skyrim"


def papyrus_compiler_path():
   return os.path.join(skyrim_path(), r"Papyrus Compiler\PapyrusCompiler.exe")


def skyrim_scripts_path():
   return os.path.join(skyrim_path(), r"Data\scripts\Source")


def scripts_path():
   return os.path.join(base_path(), r"plugin\scripts")


def script_path():
   return os.path.join(scripts_path(), "ExportPlugin.psc")


def msbuild_path():
   return r"C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\MSBuild\15.0\Bin\MSBuild.exe"


def project_path():
   return os.path.join(base_path(), "plugin.sln")


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
   command = """ \
      "{compiler_path}" \
      "{project_path}" \
      /property:Configuration={configuration}  \
   """.format(
      compiler_path=msbuild_path(),
      project_path=project_path(),
      configuration=configuration_string()
   )

   run_command(command)


def compile_script():
   command = """ \
      "{compiler_path}" \
      "{scripts_path}" \
      -all \
      -flags="TESV_Papyrus_Flags.flg" \
      -import="{skyrim_scripts_path};{scripts_path}" \
      -output="{build_path}" \
   """.format(
      compiler_path=papyrus_compiler_path(),
      skyrim_scripts_path=skyrim_scripts_path(),
      scripts_path=scripts_path(),
      build_path=build_path()
   )

   run_command(command)


def build():
   compile_plugin()
   compile_script()



if __name__ == "__main__":
   build()
