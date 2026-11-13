' Starts ocr_tool.py silently (no console window).
' Works from wherever this file lives, so a shortcut to it can go in the Startup folder.
Set fso = CreateObject("Scripting.FileSystemObject")
folder = fso.GetParentFolderName(WScript.ScriptFullName)
CreateObject("Wscript.Shell").Run "pythonw """ & folder & "\ocr_tool.py""", 0, False
