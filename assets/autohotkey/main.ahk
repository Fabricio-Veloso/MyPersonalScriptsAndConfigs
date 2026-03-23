#Requires AutoHotkey v2.0+

; LEMBRE-SE QUE ESTE PROGRAMAS PRECISAM ESTAR NO PATH PARA QUE FUNCIONE!

; Alt + j - Abrir ou focar Zen Browser
!j::
{
    if WinExist("ahk_class MozillaWindowClass")
        WinActivate
    else if WinExist("ahk_exe zen.exe")
        WinActivate
    else
        Run("zen.exe")
}

; Alt + k - Abrir ou focar Windows Terminal
!k::
{
    if WinExist("ahk_exe WindowsTerminal.exe")
        WinActivate
    else
        Run("wt.exe")
}

; Alt + l - Abrir ou focar Obsidian
!l::
{
    if WinExist("ahk_class Chrome_WidgetWin_1")
        WinActivate
    else if WinExist("ahk_exe Obsidian.exe")
        WinActivate
    else
        Run("Obsidian.exe")
}

; Alt + ç - Abrir ou focar WhatsApp
!ç::
{
    if WinExist("ahk_class ApplicationFrameWindow ahk_exe ApplicationFrameHost.exe") and WinExist("WhatsApp")
    {
        WinActivate
    }
    else
    {
        Run("shell:AppsFolder\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App")
    }
}
return

F24 & j:: {
    if GetKeyState("Shift", "P")
        Send("+{Backspace}")
    else
        Send("{Backspace}")
}

F24 & k:: {
    if GetKeyState("Shift", "P")
        Send("+{Delete}")
    else
        Send("{Delete}")
}

F24 & l:: {
    if GetKeyState("Shift", "P")
        Send("+{Home}")
    else
        Send("{Home}")
}

F24 & ç:: {
    if GetKeyState("Shift", "P")
        Send("+{End}")
    else
        Send("{End}")
}

F24::Return

F24 & h:: {
    if GetKeyState("Shift", "P")
        Send("+{Esc}")
    else
        Send("{Esc}")
}
