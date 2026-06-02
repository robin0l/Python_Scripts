#Requires AutoHotkey v2.0   
     c:: {
    Send "^c" ; Simulate Ctrl+C
}

v:: {
    Send "^v" ; Simulate Ctrl+V
}

x:: {
    Send "!{Tab}" ; Simulate Alt+Tab
}

z:: {
    Send "0" ; Simulate 0
}

b:: {
    Send "{Backspace}" ; Simulate backspace
}
^q::ExitApp ; Press Ctrl+Q to quit the script