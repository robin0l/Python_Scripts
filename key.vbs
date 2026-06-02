set wsc = CreateObject("WScript.Shell")
Do
    'one minute
    WScript.Sleep(60*1000)
    wsc.SendKeys("{NUMLOCK}")
Loop