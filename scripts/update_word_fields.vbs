' update_word_fields.vbs - 更新 Word 文档中的所有域（目录、页码等）
' 用法: cscript //nologo update_word_fields.vbs <docx完整路径>
Set args = WScript.Arguments
If args.Count < 1 Then
    WScript.Echo "Usage: update_word_fields.vbs <docx path>"
    WScript.Quit 1
End If

' 获取绝对路径（处理中文路径）
Dim fso, file
Set fso = CreateObject("Scripting.FileSystemObject")
docPath = fso.GetAbsolutePathName(args(0))

If Not fso.FileExists(docPath) Then
    WScript.Echo "文件不存在: " & docPath
    WScript.Quit 1
End If

WScript.Echo "目标文档: " & docPath

' ===== 第一阶段：静默更新域 =====
Dim word, doc, updatedCount
On Error Resume Next
Set word = CreateObject("Word.Application")
If Err.Number <> 0 Then
    WScript.Echo "[错误] 创建 Word COM 失败: " & Err.Description
    WScript.Quit 1
End If
On Error GoTo 0

word.Visible = False
word.DisplayAlerts = 0  ' wdAlertsNone = 0

On Error Resume Next
Set doc = word.Documents.Open(docPath, False, False)  ' Open(FileName, ConfirmConversions, ReadOnly)
If Err.Number <> 0 Then
    WScript.Echo "[错误] 打开文档失败: " & Err.Description
    word.Quit
    Set word = Nothing
    WScript.Quit 1
End If
On Error GoTo 0

If doc Is Nothing Then
    WScript.Echo "[错误] 文档对象为 Nothing"
    word.Quit
    Set word = Nothing
    WScript.Quit 1
End If

' 全选 → 更新所有域
word.Selection.WholeStory
On Error Resume Next
updatedCount = word.Selection.Fields.Update()
If Err.Number <> 0 Then
    WScript.Echo "[警告] 更新域时出错: " & Err.Description
    Err.Clear
End If
On Error GoTo 0

WScript.Echo "已更新 " & updatedCount & " 个域（含目录 TOC + 页码 PAGE）"

' 保存并关闭
On Error Resume Next
doc.Save()
doc.Close(False)
On Error GoTo 0
Set doc = Nothing

word.Quit
Set word = Nothing

' 等待 COM 进程完全退出
WScript.Sleep 2000

' ===== 第二阶段：重新打开让用户查看 =====
WScript.Echo "正在重新打开文档..."
Set word2 = CreateObject("Word.Application")
word2.Visible = True
word2.DisplayAlerts = 0

On Error Resume Next
Set doc2 = word2.Documents.Open(docPath)
If Err.Number <> 0 Then
    WScript.Echo "[警告] 重新打开失败: " & Err.Description
    Err.Clear
    ' 用 Shell 打开
    Dim shell
    Set shell = CreateObject("WScript.Shell")
    shell.Run """" & docPath & """"
    Set shell = Nothing
End If
On Error GoTo 0

WScript.Echo "完成！目录和页码已更新。"
