#!/usr/bin/env python

from scripting_commons import *



class RetroArch:
    class Consts:
        UNIX_CORES_EXT = ".so"
        WINDOWS_CORES_EXT = ".dll"

        def __init__(self) -> None:
            pass


    class Paths:
        Cores = ""
        BIOS = ""
        Exec = ""
        Home = ""
        SystemFiles = ""

        def __init__(self) -> None:
            pass

        @staticmethod
        def Init (retroarch_path: str) -> bool:
            retroarch_exec = concat ("RetroArch-",
                                     os_name().capitalize(),
                                     "-",
                                     os_arch())
            
            if in_windows ():
                retroarch_exec += ".exe"
            elif in_linux ():
                retroarch_exec += ".AppImage"
            else:
                retroarch_exec += ".app"                            

            if not file_exists (make_path (retroarch_path, 
                                           retroarch_exec)):
                
                print_va ("ERROR: No RetroArch installation found in '$[0]",
                          retroarch_path)
                
                return False
             
            else:
                RetroArch.Paths.Exec = make_path (retroarch_path, 
                                                  retroarch_exec)
                
                RetroArch.Paths.Home = make_path (retroarch_path, 
                                                  concat (retroarch_exec, 
                                                  ".home"))

                RetroArch.Paths.SystemFiles = make_path (RetroArch.Paths.Home,
                                                         ".config",
                                                         "retroarch")

                RetroArch.Paths.BIOS = make_path (RetroArch.Paths.SystemFiles,
                                                  "saves")
                
                RetroArch.Paths.Cores = make_path (RetroArch.Paths.SystemFiles,
                                                   "cores")
                
                return True
            

    class URL:
        LINUX = "https://buildbot.libretro.com/nightly"\
                "/linux/x86_64/RetroArch.7z"
        
        MACOS = "https://buildbot.libretro.com/stable/1.19.1"\
                "/apple/osx/universal/RetroArch_Metal.dmg"
        
        MACOS_LEGACY = "https://buildbot.libretro.com/nightly"\
                       "/apple/osx/x86_64/RetroArch.dmg"
        
        WINDOWS_X86 = "https://buildbot.libretro.com/stable/1.19.1"\
                      "/windows/x86/RetroArch.7z"
        
        WINDOWS_X64 = "https://buildbot.libretro.com/stable/1.19.1"\
                      "/windows/x86_64/RetroArch.7z"
        
        WINDOWS_LEGACY = "https://buildbot.libretro.com/stable/1.19.1"\
                         "/windows-msvc2010/x86/RetroArch.7z"
        
        WINDOWS_9X = "https://buildbot.libretro.com/stable/1.19.1"\
                     "/windows-msvc2005/x86/RetroArch.7z"

        def __init__(self) -> None:
            pass


    DefaultCores = {
                        "amiga": "puae",
                        "gb": "gambatte",
                        "gba": "vbam",
                        "mame": "mame",
                        "md": "genesis_plus_gx",
                        "nds": "melondsds",
                        "nes": "mesen",
                        "psx": "mednafen_psx_hw",
                        "snes": "snes9x",
                        "zx": "fuse"
                    }
    
    SystemsGameExtensions = { 
                                "amiga": [".adf", ".uae", ".zip"],
                                "gb": [".gb", ".gbc", ".sgb"],
                                "gba": [".gba"],
                                "mame": [".zip"],
                                "md": [".bin"],
                                "nds": [".nds"],
                                "nes": [".nes"],
                                "psx": [".cue", ".iso"],
                                "snes": [".sfc", ".smc"],
                                "zx": [".sna", ".tap", ".tzx"]
                            }

    ready = False


    def __init__(self) -> None:
        pass    


    @staticmethod
    def cores_ext () -> str:
        if in_windows ():
            return RetroArch.Consts.WINDOWS_CORES_EXT
        else:
            return RetroArch.Consts.UNIX_CORES_EXT    


    @staticmethod
    def download (destination: str) -> bool:
        url = ""

        if in_windows ():
            url = RetroArch.URL.WINDOWS_X64
        elif in_linux ():
            url = RetroArch.URL.LINUX
        else:
            url = RetroArch.URL.MACOS_LEGACY

        download (url, destination)


    @staticmethod
    def launch () -> None:
        if RetroArch.ready:
            cmdline = []
            cmdline.append (RetroArch.Paths.Exec)

            exec (cmdline)


    @staticmethod
    def play (game: str, with_core: str = None) -> bool:
        if not RetroArch.ready:
            return False
        
        if (with_core == None):
            game_system = RetroArch.system_of (game)

            if (game_system == None):
                return False
            
            with_core = RetroArch.DefaultCores[game_system]
        
        cmdline = []
        cmdline.append (RetroArch.Paths.Exec)
        cmdline.append ("-L")        
        cmdline.append (make_path (RetroArch.Paths.Cores, 
                                   concat (with_core, RetroArch.cores_ext())))
        
        cmdline.append (game)

        exec_result = exec (cmdline)

        return exec_result.ok    


    @staticmethod
    def system_of (game: str) -> str:
        game_ext = file_ext (game)

        for system in RetroArch.SystemsGameExtensions.keys():
            system_exts = RetroArch.SystemsGameExtensions[system]

            if game_ext in system_exts:
                return system
            
        return None


    @staticmethod
    def use (retroarch_path: str) -> None:
        """
        Use a custom RetroArch installation
        """
        if RetroArch.Paths.Init (retroarch_path):
            RetroArch.retro_path = retroarch_path
            RetroArch.ready = True


    @staticmethod
    def use_local () -> None:
        """
        Use a RetroArch installation located at the current directory.
        """
        retroarch_path = make_path (cwd (),
                                    concat ("RetroArch-",
                                            os_name().capitalize,
                                            "-",
                                            os_arch ()))
        
        if not dir_exists (retroarch_path):
            if not download (cwd ()):
                print ("Failed downloading RetroArch.")
                print ()
                exit (1)
        
        if RetroArch.Paths.Init (retroarch_path):
            RetroArch.retro_path = retroarch_path
            RetroArch.ready = True


    @staticmethod
    def use_user () -> None:
        """
        Use a RetroArch installation located at user home directory
        """
        retroarch_path = make_path (user_home (),
                                    concat ("RetroArch-",
                                            os_name().capitalize,
                                            "-",
                                            os_arch ()))
        
        if not dir_exists (retroarch_path):
            if not download (user_home ()):
                print ("Failed downloading RetroArch.")
                print ()
                exit (1)
        
        if RetroArch.Paths.Init (retroarch_path):
            RetroArch.retro_path = retroarch_path
            RetroArch.ready = True




def help () -> None:
    print ("RetroArch Command line util")
    print ("---------------------------")
    print ("Usage: ")
    print ()
    print ("retroarch_cu [-h|--help]")
    print (": Shows this help")
    print ()
    print ("retroarch_cu use local|<RetroArch path>|user")
    print (": Makes this RetroArch the default")
    print ()
    print ("  Local: Searches RetroArch in the current directory.")
    print ("  User: Searches RetroArch in the user home directory.")
    print ("  ")
    print ("  If 'local' or 'user' is given, and no RetroArch")
    print ("  installation is found, the proper RetroArch for")
    print ("  this system will be downloaded and extracted")
    print ("  in the corresponding place.")
    print ()
    print ("retroarch_cu play <game path> [-core:<core name|core path>] [-s]")
    print (": Launches the given game.")
    print ()
    print ("  The needed core is detected from the game file extension.")
    print ("  If a ZIP file is given, it will be scanned to find game files.")
    print ()
    print ("  The -core parameter can be added to use another core")
    print ("  instead the default one for that system.")
    print ()
    print ("  The -s parameter saves this core as the new default")
    print ("  for this game's system.")
    print ()




DEBUGGING = True

if __name__ == "__main__":
    if DEBUGGING:
        argv = ("DUMMY", "")
    else:        
        argv = sys.argv

    args = len (argv[1:])

    if not DEBUGGING:
        if no_args ():
            help ()
            exit (1)


    RetroArch.use ("/home/javier/apps/RetroArch")
