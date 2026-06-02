#Requires AutoHotkey v2.0

^j:: {
    Loop 10000000000000 {
    Send "0"  
    sleep 60000
    }
}

^q::ExitApp() ;Press Ctrl+Q to quit the script