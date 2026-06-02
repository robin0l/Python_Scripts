#Requires AutoHotkey v2.0

^j:: {
    Loop 100 {
    Send "!{Tab}"  ; Alt+Tab to switch window
    Sleep 1000      
    Send "{Down}"  ; Press Down Arrow
    Sleep 1000
    Send "^c"       ; Press Ctrl+C to copy
    Sleep 1000
    Send "!{Tab}"  ;
    Sleep 2000
    MouseMove 320, 125 ; click to stock number in selection
    Click 2 ; Double-click at that point
    Sleep 500
    Send "^v"  ; paste new partnumber
    Sleep 500
    MouseMove 1220, 245 ; mouse click to search
    Click
    Sleep 25000
    MouseMove 288, 314 ; mouse clict to first list
    Click
    Sleep 5000
    MouseMove 246, 78 ; mouse clict to detale page
    Click
    Sleep 8000
    MouseMove 290, 100 ; mouse clict to stock number start
    Click
    Sleep 500
    Send "0"
    Sleep 500
    ;MouseMove 190, 78 ; mouse clict to selector
    ;Click
    ;Sleep 8000
    ;MouseMove 254, 125 ; mouse clict to stock number
    ;Click 
    ;Sleep 1000
    ;MouseMove 254, 125 ; mouse clict to stock number
    ;Click 
    ;Sleep 1000
    ;Send "0"
    ;Sleep 1000
    ;MouseMove 1220, 245 ; mouse click to search
    ;Click
    ;Sleep 15000
    ;MouseMove 288, 314 ; mouse clict to first list
    ;Click
    ;Sleep 2000
    ;MouseMove 246, 78 ; mouse clict to detale page
    ;Click
    ;Sleep 10000
    ;MouseMove 296, 100 ; mouse clict to stock number 0
    ;Click
    ;Sleep 1000
    ;Send "{Backspace}"
    ;Sleep 1000
    MouseMove 190, 78 ; mouse clict to selector
    Click
    Sleep 8000
    }
}

^q::ExitApp() ;Press Ctrl+Q to quit the script