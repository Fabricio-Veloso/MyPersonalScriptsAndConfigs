#Requires AutoHotkey v2.0+

; LEMBRE-SE QUE ESTE PROGRAMAS PRECISAM ESTAR NO PATH PARA QUE FUNCIONE!

; Alt + j - Abrir ou focar Zen Browser
!j::
{
    if WinExist("ahk_class MozillaWindowClass")  ; Classe da janela do Zen Browser
        WinActivate
    else if WinExist("ahk_exe zen.exe")  ; Executável do Zen Browser
        WinActivate
    else
        Run("zen.exe")  ; Substitua pelo caminho real
}

; Alt + k - Abrir ou focar Warp terminal 
!k::
{
    if WinExist("ahk_class Window Class")  ; Classe da janela do Terminal
        WinActivate
    else if WinExist("ahk_exe warp.exe")  ; Executável do Windows Terminal
        WinActivate
    else
        Run("warp.exe")  ; Comando para abrir o Windows Terminal
}

; Alt + l - Abrir ou focar Obsidian
!l::
{
    if WinExist("ahk_class Chrome_WidgetWin_1")  ; Classe da janela do Obsidian
        WinActivate
    else if WinExist("ahk_exe Obsidian.exe")  ; Executável do Obsidian
        WinActivate
    else
        Run("Obsidian.exe")  ; Substitua pelo caminho real
}
; Alt + ç - Abrir ou focarWhatapp 
!ç::
{
    if WinExist("ahk_class ApplicationFrameWindow ahk_exe ApplicationFrameHost.exe") and WinExist("WhatsApp")
    {
        WinActivate  ; ativa a janela encontrada
    }
    else
    {
        Run("shell:AppsFolder\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App")
    }
}
return



F24 & j:: {
    if GetKeyState("Shift", "P")
        Send("+{Backspace}")  ; Shift + Backspace (geralmente não tem efeito diferente, mas mantido por consistência)
    else
        Send("{Backspace}")
}

F24 & k:: {
    if GetKeyState("Shift", "P")
        Send("+{Delete}")  ; Shift + Delete geralmente remove permanentemente
    else
        Send("{Delete}")
}

F24 & l:: {
    if GetKeyState("Shift", "P")
        Send("+{Home}")  ; Seleciona até o início da linha
    else
        Send("{Home}")
}

F24 & ç:: {
    if GetKeyState("Shift", "P")
        Send("+{End}")  ; Seleciona até o fim da linha
    else
        Send("{End}")
}


; Evita comportamento estranho ao soltar F24 sozinho
F24::Return

F24 & h:: {
    if GetKeyState("Shift", "P")
        Send("+{Esc}")
    else
        Send("{Esc}")
}

