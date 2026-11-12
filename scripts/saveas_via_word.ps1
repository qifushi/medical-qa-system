$tmpDoc = "$env:TEMP\thesis_work\论文\基于多源医学知识融合与混合检索的医疗智能问答系统设计与实现.docx"
$origDoc = "c:\Users\76955\OneDrive\桌面\medical\论文\基于多源医学知识融合与混合检索的医疗智能问答系统设计与实现.docx"

Write-Host "Kill OneDrive..."
Get-Process | Where-Object { $_.ProcessName -match 'OneDrive|WINWORD' } | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 3

Write-Host "Open temp doc in Word..."
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
$doc = $word.Documents.Open($tmpDoc)
Start-Sleep -Seconds 2

# 确保视图是打印模式
$word.ActiveWindow.View.Type = 3

# 再更新一遍所有域确保最新
$doc.Fields.Update()
$doc.TablesOfContents | ForEach-Object { $_.Update(); $_.UpdatePageNumbers() }
$doc.Sections | ForEach-Object { 
    try { $_.Footers.Item(1).Range.Fields.Update() } catch {}
}
Start-Sleep -Milliseconds 500

Write-Host "SaveAs to original path..."
# wdFormatXMLDocument = 16 (.docx)
$doc.SaveAs([ref]$origDoc, [ref]16)
$doc.Close()
$word.Quit()
[void][System.Runtime.Interopservices.Marshal]::ReleaseComObject($doc)
[void][System.Runtime.Interopservices.Marshal]::ReleaseComObject($word)
Start-Sleep -Seconds 3

if (Test-Path $origDoc) {
    Write-Host "SaveAs 成功! 大小: $((Get-Item $origDoc).Length / 1MB -as [int]) MB" -ForegroundColor Green
} else {
    Write-Host "SaveAs 也失败了..." -ForegroundColor Red
}

Write-Host "`n打开 Word 查看..."
Start-Process winword.exe -ArgumentList "`"$origDoc`""
