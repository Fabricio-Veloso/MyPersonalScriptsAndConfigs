#Requires AutoHotkey v2.0+

; Alt + H - Abrir ou focar Zen Browser
!j::
{
    if WinExist("ahk_class MozillaWindowClass")  ; Classe da janela do Zen Browser
        WinActivate
    else if WinExist("ahk_exe zen.exe")  ; Executável do Zen Browser
        WinActivate
    else
        Run("C:\Path\To\ZenBrowser\zen.exe")  ; Substitua pelo caminho real
}

; Alt + J - Abrir ou focar Windows Terminal (com WSL)
!k::
{
    if WinExist("ahk_class CASCADIA_HOSTING_WINDOW_CLASS")  ; Classe da janela do Terminal
        WinActivate
    else if WinExist("ahk_exe WindowsTerminal.exe")  ; Executável do Windows Terminal
        WinActivate
    else
        Run("wt.exe")  ; Comando para abrir o Windows Terminal
}

; Alt + K - Abrir ou focar Obsidian
!l::
{
    if WinExist("ahk_class Chrome_WidgetWin_1")  ; Classe da janela do Obsidian
        WinActivate
    else if WinExist("ahk_exe Obsidian.exe")  ; Executável do Obsidian
        WinActivate/
    else
        Run("C:\Path\To\Obsidian.exe")  ; Substitua pelo caminho real
}

F24 & j::Send("{Backspace}")
F24 & k::Send("{Delete}")
F24 & l::Send("{Home}")
F24 & ç::Send("{End}")

F24::Return
