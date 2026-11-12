$tmpDoc = "C:\Users\76955\AppData\Local\Temp\thesis_work\论文\基于多源医学知识融合与混合检索的医疗智能问答系统设计与实现.docx"
Write-Host "Opening fresh doc..."
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
$doc = $word.Documents.Open($tmpDoc)

# 等 Word 完全加载
Write-Host "Waiting for Word initialization..."
Start-Sleep -Seconds 3

Write-Host "`n=== Before any update ==="
Write-Host "  Main fields: $($doc.Fields.Count)"
foreach ($sec in $doc.Sections) {
    Write-Host "  Header.Fields: $($sec.Header.Range.Fields.Count)"
    Write-Host "  Footer.Fields: $($sec.Footer.Range.Fields.Count)"
}

# 1) 更新 TOC
Write-Host "`n=== Updating TOC ==="
foreach ($toc in $doc.TablesOfContents) {
    $toc.Update()
    Write-Host "  TOC updated, now has $($toc.Count) entries"
}

# 2) 更新页眉页脚的域（手动遍历 Section）
Write-Host "`n=== Updating Header/Footer fields ==="
foreach ($sec in $doc.Sections) {
    $hdrCnt = $sec.Header.Range.Fields.Update()
    Write-Host "  Header.Fields.Update() returned: $hdrCnt"
    $ftrCnt = $sec.Footer.Range.Fields.Update()
    Write-Host "  Footer.Fields.Update() returned: $ftrCnt"
}

# 3) 全文档 Fields.Update
Write-Host "`n=== Full doc update ==="
$word.Selection.WholeStory()
$all = $word.Selection.Fields.Update()
Write-Host "  Selection.Fields.Update() returned: $all"

# 4) 保存
$doc.Save()
Write-Host "`nSaved!"

# 5) 重新打开检查
$doc.Close()
$word.Quit()
[void][System.Runtime.Interopservices.Marshal]::ReleaseComObject($doc)
[void][System.Runtime.Interopservices.Marshal]::ReleaseComObject($word)
Start-Sleep -Seconds 3

Write-Host "`n=== REOPENING TO VERIFY ==="
$word2 = New-Object -ComObject Word.Application
$word2.Visible = $false
$word2.DisplayAlerts = 0
$doc2 = $word2.Documents.Open($tmpDoc)
Start-Sleep -Seconds 2

Write-Host "  Main fields: $($doc2.Fields.Count)"
foreach ($sec in $doc2.Sections) {
    Write-Host "  Header.Fields: $($sec.Header.Range.Fields.Count)"
    Write-Host "  Footer.Fields: $($sec.Footer.Range.Fields.Count)"
    # 读取页脚实际文本
    $footerText = $sec.Footer.Range.Text.Trim()
    Write-Host "  Footer text: '$footerText'"
}

Write-Host "`n  TOC entries: $($doc2.TablesOfContents.Item(1).Count)"

$doc2.Close()
$word2.Quit()
[void][System.Runtime.Interopservices.Marshal]::ReleaseComObject($doc2)
[void][System.Runtime.Interopservices.Marshal]::ReleaseComObject($word2)
