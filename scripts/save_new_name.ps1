$tmpDoc = "$env:TEMP\thesis_work\论文\基于多源医学知识融合与混合检索的医疗智能问答系统设计与实现.docx"
$newDoc = "c:\Users\76955\OneDrive\桌面\medical\论文\论文_更新版.docx"

Write-Host "Kill all Word..."
Get-Process | Where-Object { $_.ProcessName -match 'WINWORD|OneDrive' } | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 5

Write-Host "Open temp doc..."
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
$doc = $word.Documents.Open($tmpDoc)
Start-Sleep -Seconds 3

$word.ActiveWindow.View.Type = 3
Start-Sleep -Seconds 1

# 全量更新
$doc.Fields.Update()
foreach ($toc in $doc.TablesOfContents) { $toc.Update(); $toc.UpdatePageNumbers() }
foreach ($sec in $doc.Sections) { try { $sec.Footers.Item(1).Range.Fields.Update() } catch {} }

Write-Host "SaveAs 到新文件名..."
try {
    $doc.SaveAs2($newDoc, 16)  # wdFormatXMLDocument
    Write-Host "SaveAs2 OK" -ForegroundColor Green
} catch {
    Write-Host "SaveAs2 failed: $_"
    try {
        $doc.SaveAs([ref]$newDoc, [ref]16)
        Write-Host "SaveAs OK" -ForegroundColor Green
    } catch {
        Write-Host "SaveAs also failed: $_"
    }
}

$doc.Close()
$word.Quit()
Start-Sleep -Seconds 3

if (Test-Path $newDoc) {
    Write-Host "新文件已生成: $newDoc ($((Get-Item $newDoc).Length / 1MB -as [int]) MB)" -ForegroundColor Green
}

Write-Host "`n打开查看..."
Start-Process winword.exe -ArgumentList "`"$newDoc`""
