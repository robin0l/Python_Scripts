#Requires AutoHotkey v2.0

; Press j to run the full process once
q:: {
    RunProcess()
}

; Press w to run the same process again
o:: {
    RunProcess()
}

; Press Ctrl+C anytime to cancel/exit script
e::ExitApp

RunProcess() {
CoordMode "Mouse", "Window"
    MouseMove 337, 133 ;click to stock2
    Click "Left", 2  
  Sleep 1000

    Send "{Delete}"  
    Sleep 500

    Send "0"
    Sleep 500

    MouseMove 337, 148 ;click to warehouse
    Click "Left", 1
    Sleep 1000

    MouseMove 340, 300 ;click to adjust
    Click "Left", 1
    Sleep 1000

    MouseMove 196, 104 ;click to selection
    Click "Left", 1
    Sleep 2000

    MouseMove 259, 74 ;click to next key
    Click "Left", 1
    Sleep 1000

    MouseMove 670, 106 ;click to stocklevels
    Click "Left", 1
    Sleep 1000

    MouseMove 507, 207 ;click to stock 2
   Click "Left", 1
    Sleep 500

    MouseMove 1300, 703 ;click to adjust levels
    Click "Left", 1
    Sleep 500

    MouseMove 170, 60 ;click to adjust levels
    Click "Left", 1
    Sleep 500

    Send "{Backspace}"  
    Sleep 500
}
