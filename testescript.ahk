#Requires AutoHotkey v2.0+

; Alt + H - Abrir ou focar Zen Browser
!h::
{
    if WinExist("ahk_class MozillaWindowClass")  ; Classe da janela do Zen Browser
        WinActivate
    else if WinExist("ahk_exe zen.exe")  ; Executável do Zen Browser
        WinActivate
    else
        Run("C:\Path\To\ZenBrowser\zen.exe")  ; Substitua pelo caminho real
}

; Alt + J - Abrir ou focar Windows Terminal (com WSL)
!j::
{
    if WinExist("ahk_class CASCADIA_HOSTING_WINDOW_CLASS")  ; Classe da janela do Terminal
        WinActivate
    else if WinExist("ahk_exe WindowsTerminal.exe")  ; Executável do Windows Terminal
        WinActivate
    else
        Run("wt.exe")  ; Comando para abrir o Windows Terminal
}

; Alt + K - Abrir ou focar Obsidian
!k::
{
    if WinExist("ahk_class Chrome_WidgetWin_1")  ; Classe da janela do Obsidian
        WinActivate
    else if WinExist("ahk_exe Obsidian.exe")  ; Executável do Obsidian
        WinActivate
    else
        Run("C:\Path\To\Obsidian.exe")  ; Substitua pelo caminho real
}

