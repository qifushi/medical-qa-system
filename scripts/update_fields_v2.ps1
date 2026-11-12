$tmpDoc = "C:\Users\76955\AppData\Local\Temp\thesis_work\论文\基于多源医学知识融合与混合检索的医疗智能问答系统设计与实现.docx"
Write-Host "=== Opening doc and forcing print view + footer seek ==="
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
$doc = $word.Documents.Open($tmpDoc)

# 切到打印视图
Write-Host "Switching to PrintView..."
$word.ActiveWindow.View.Type = 3  # wdPrintView

# 等待加载
Start-Sleep -Seconds 3

Write-Host "Sections count: $($doc.Sections.Count)"
Write-Host "ActiveWindow type: $($word.ActiveWindow.View.Type)"

foreach ($sec in $doc.Sections) {
    Write-Host "`n--- Section $($sec.Index) ---"
    Write-Host "  HasHeader: $($sec.HasHeader)"
    Write-Host "  HasFooter: $($sec.HasFooter)"
    Write-Host "  PageHeight: $($sec.PageHeight)"
    Write-Host "  PageWidth: $($sec.PageWidth)"
    
    # 激活当前页的页脚
    try {
        $word.ActiveWindow.View.SeekView = 9  # wdSeekCurrentPageFooter
        Start-Sleep -Milliseconds 500
        Write-Host "  After seek footer: Header=$($sec.Headers.Count), Footer=$($sec.Footers.Count)"
        $f = $sec.Footers.Item(1)
        Write-Host "  Footer(1) Range fields: $($f.Range.Fields.Count)"
        Write-Host "  Footer(1) text: '$($f.Range.Text.Trim())'"
        $word.ActiveWindow.View.SeekView = 0  # wdSeekMainDocument
    } catch {
        Write-Host "  Seek error: $_"
    }
}

# 切回主文档
$word.ActiveWindow.View.SeekView = 0

# 全选 + F9 等效：更新所有域
Write-Host "`n=== Force update all fields ==="
$word.Selection.WholeStory()
$updated = $word.Selection.Fields.Update()
Write-Host "  Selection.Fields.Update returned: $updated"

# 也对每个 Section 的 Footer 单独做
foreach ($sec in $doc.Sections) {
    try {
        $footer = $sec.Footers.Item(1)
        $n = $footer.Range.Fields.Update()
        Write-Host "  Section $($sec.Index) Footer update returned: $n"
    } catch {
        Write-Host "  Footer update error: $_"
    }
}

# 更新 TOC
foreach ($toc in $doc.TablesOfContents) {
    $toc.Update()
    Write-Host "  TOC updated, $($toc.Count) entries"
}

# 保存
$doc.Save()
Write-Host "`nSaved!"

# 重新打开确认
$doc.Close()
$word.Quit()
[void][System.Runtime.Interopservices.Marshal]::ReleaseComObject($doc)
[void][System.Runtime.Interopservices.Marshal]::ReleaseComObject($word)
Start-Sleep -Seconds 3

Write-Host "`n=== REOPEN ==="
$word2 = New-Object -ComObject Word.Application
$word2.Visible = $false
$word2.DisplayAlerts = 0
$doc2 = $word2.Documents.Open($tmpDoc)
Start-Sleep -Seconds 3

$word2.ActiveWindow.View.Type = 3  # wdPrintView
$word2.ActiveWindow.View.SeekView = 9  # wdSeekCurrentPageFooter
Start-Sleep -Milliseconds 500

foreach ($sec in $doc2.Sections) {
    try {
        $f = $sec.Footers.Item(1)
        Write-Host "Section $($sec.Index) Footer text: '$($f.Range.Text.Trim())'"
        Write-Host "Section $($sec.Index) Footer fields: $($f.Range.Fields.Count)"
    } catch {
        Write-Host "Footer error: $_"
    }
}
Write-Host "TOC entries: $($doc2.TablesOfContents.Item(1).Count)"

$word2.ActiveWindow.View.SeekView = 0
$doc2.Close()
$word2.Quit()
[void][System.Runtime.Interopservices.Marshal]::ReleaseComObject($doc2)
[void][System.Runtime.Interopservices.Marshal]::ReleaseComObject($word2)

Write-Host "`n=== Done. Now opening in visible Word ==="
Start-Sleep -Seconds 2
Start-Process winword.exe -ArgumentList "`"$tmpDoc`""
