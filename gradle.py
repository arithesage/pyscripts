#!/usr/bin/env python

from filesystem import append_to_file, copy, cwd, makedir, make_tempdir, make_path, dir_exists, file_exists
from lang import type_of
from os_utils import path_of, ProcessResult, run_from, run_from_quietly, si_path
from stdio import print_va
from str_utils import str_empty
    

def __run_gradle (params, quiet = False, cwd:str = ".") -> ProcessResult:
    cmdline = []
    cmdline.append (gradle_path)

    if type_of (params, str):
        params = params.split (" ")

    for p in params:
        cmdline.append (p)

    if quiet:
        gradle_result = run_from_quietly (cmdline, cwd)
    else:
        gradle_result = run_from (cmdline, cwd)

    return gradle_result


def add_module (module_name: str,
                package_name: str,
                project_type: str = "java-library",
                dsl: str = "kotlin") -> bool:
    
    """
    Adds a module to the current project
    """

    temp_path = make_tempdir ()

    if str_empty (temp_path):
        print ("ERROR: Temp path could not be created.")
        return False

    temp_module_path = make_path (temp_path, module_name)

    gradle_params = []
    gradle_params.append ("init")
    gradle_params.append ("--type")
    gradle_params.append (project_type)
    gradle_params.append ("--dsl")
    gradle_params.append (dsl)
    gradle_params.append ("--package")
    gradle_params.append (package_name)
    gradle_params.append ("--project-name")
    gradle_params.append (module_name)
    gradle_params.append ("--project-dir")
    gradle_params.append (temp_module_path)

    if not makedir (temp_module_path):
        print_va ("ERROR: Failed creating module temp path '$[0]'.", temp_module_path)
        return False
    
    print_va ("Creating module '$[0]'...", module_name)

    gradle_result = __run_gradle (gradle_params)

    if gradle_result.failed ():
        print ("Failed creating project.")
        return False
    else:
        temp_module_path = make_path (temp_module_path, module_name)
        final_module_path = make_path (cwd (), module_name)

        settings_path = "settings.gradle"
        settings_kts_path = "settings.gradle.kts"

        copy (temp_module_path, final_module_path)

        if not dir_exists (final_module_path):
            print_va ("ERROR: Could not create module in '$[0]'.", final_module_path)
            return False
        
        if file_exists (settings_kts_path):
            append_to_file (settings_kts_path, "\ninclude (" + module_name + ")\n")

        print ("Module created.")
        return True


def create_project (project_name: str = "",
                    project_type: str = "java-application",
                    package_name: str = "me.java.apps.testapp",
                    dsl: str = "kotlin") -> bool:
    
    """
    Creates a new project.
    
    By default, creates a Java application, with the package
    'me.java.apps.testapp' and Kotlin as DSL.

    The project is named as the current directory if no project name is
    specified.

    If a project name is specified, and the corresponding directory
    does not exists, it will be created.
    """

    project_path = "."

    gradle_params = []
    gradle_params.append ("init")

    if not str_empty (project_name):
        gradle_params.append ("--project-name")
        gradle_params.append (project_name)
        project_path = make_path (cwd (), project_name)
    
    gradle_params.append ("--type")
    gradle_params.append (project_type)
    gradle_params.append ("--dsl")
    gradle_params.append (dsl)
    gradle_params.append ("--package")
    gradle_params.append (package_name)

    if not dir_exists (project_path):
        print_va ("Creating project in '$[0]'...", project_path)

        if not makedir (project_path):
            print_va ("ERROR: Failed creating path '$[0].", project_path)
            print ("Project creation aborted.")
            print ()
            return False

    gradle_result = __run_gradle (gradle_params, False, project_path)

    if gradle_result.failed ():
        print ("Failed creating project.")
        return False
    else:
        print ("Project created.")
        return True


def use_gradlew (gradlew_path: str) -> bool:
    global gradle_path

    gradlew_path = si_path (gradlew_path)

    if file_exists (gradlew_path):
        _version = version ()

        if not str_empty (_version):
            print_va ("Using gradlew from '$[0]'.", gradle_path)
            gradle_path = gradlew_path
            return True

        print_va ("ERROR: Failed executing gradlew from '$[0]'.", gradlew_path) 
        return False
    

def tasks () -> str:
    __run_gradle ("tasks")


def version () -> str:
    _version = ""

    gradle_result = __run_gradle ("--version", True)

    if gradle_result.ok ():
        for line in gradle_result.output_lines ():
            if ("Gradle") in line:
                _version = line.split (" ")[1]

    return _version




gradle_path = path_of ("gradle")

if not str_empty (gradle_path):
    print_va ("Using Gradle: $[0]", gradle_path)
else:
    print ("ERROR: No Gradle found in path.")
    print ("Call 'use_gradlew' if want to use any wrapper.")
    print ("")


