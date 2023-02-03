!include "MUI.nsh"

Name "Scooby Maze"
OutFile "Scooby Maze Installer.exe"

InstallDir "$PROGRAMFILES\Scooby Maze"
InstallDirRegKey HKCU "Software\Scooby Maze" ""

!define MUI_STARTMENUPAGE_REGISTRY_ROOT "HKCU"
!define MUI_STARTMENUPAGE_REGISTRY_KEY "Software\Scooby Maze"
!define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "Start Menu Folder"
Var MUI_TEMP
Var STARTMENU_FOLDER

!define MUI_ICON "scooby_maze.ico"
!define MUI_UNICON "uninst_scooby_maze.ico"

;Pages
    !insertmacro MUI_PAGE_LICENSE "LICENSE"
    !insertmacro MUI_PAGE_DIRECTORY
    !insertmacro MUI_PAGE_STARTMENU Application $STARTMENU_FOLDER
    !insertmacro MUI_PAGE_INSTFILES
    !insertmacro MUI_PAGE_FINISH
    !insertmacro MUI_LANGUAGE "English"

    !insertmacro MUI_UNPAGE_CONFIRM
    !insertmacro MUI_UNPAGE_INSTFILES
    !insertmacro MUI_UNPAGE_FINISH

Section "Install"
    SetOutPath "$INSTDIR\data"
    File dist\data\*
    SetOutPath "$INSTDIR"
    File dist\*

    WriteRegStr HKCU "Software\Scooby Maze" "" $INSTDIR
    WriteUninstaller "$INSTDIR\Uninstall.exe"

    !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
        CreateDirectory "$SMPROGRAMS\$STARTMENU_FOLDER"
        CreateShortCut "$SMPROGRAMS\$STARTMENU_FOLDER\Uninstall.lnk" "$INSTDIR\Uninstall.exe" \
                       "" "$INSTDIR\Uninstall.exe"
        CreateShortCut "$SMPROGRAMS\$STARTMENU_FOLDER\ReadMe.lnk" "$INSTDIR\ReadMe.txt"
        CreateShortCut "$SMPROGRAMS\$STARTMENU_FOLDER\Scooby Maze (parent mode).lnk" "$INSTDIR\scooby_maze.exe" \
                       "-p" "$INSTDIR\scooby_maze.exe"
        CreateShortCut "$SMPROGRAMS\$STARTMENU_FOLDER\Scooby Maze.lnk" "$INSTDIR\scooby_maze.exe" \
                       "" "$INSTDIR\scooby_maze.exe"

    !insertmacro MUI_STARTMENU_WRITE_END
    
SectionEnd

Section "Uninstall"
    Delete "$INSTDIR\data\*"
    Delete "$INSTDIR\*"
    RMDir "$INSTDIR\data"
    RMDir "$INSTDIR"

    !insertmacro MUI_STARTMENU_GETFOLDER Application $MUI_TEMP
    Delete "$SMPROGRAMS\$MUI_TEMP\*"
    RMDir "$SMPROGRAMS\$MUI_TEMP"
    
    DeleteRegKey HKCU "Software\Scooby Maze"
SectionEnd