$tmpDoc = "C:\Users\76955\AppData\Local\Temp\thesis_work\论文\基于多源医学知识融合与混合检索的医疗智能问答系统设计与实现.docx"

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
$doc = $word.Documents.Open($tmpDoc)
Start-Sleep -Seconds 3

$word.ActiveWindow.View.Type = 3  # wdPrintView
Start-Sleep -Seconds 2

Write-Host "=== Document Stats ==="
Write-Host "  Paragraphs: $($doc.Paragraphs.Count)"

# 列出所有 Heading 段落的 outline level
$headingCount = 0
for ($i = 1; $i -le $doc.Paragraphs.Count; $i++) {
    $p = $doc.Paragraphs.Item($i)
    $ol = $p.OutlineLevel
    # 1-9 = Heading levels, 10 = BodyText
    if ($ol -ge 1 -and $ol -le 9) {
        $headingCount++
        if ($headingCount -le 20) {
            Write-Host "  P[$i] Level=$ol Style=$($p.Style.NameLocal): $($p.Range.Text.Trim().Substring(0, [Math]::Min(40, $p.Range.Text.Trim().Length)))"
        }
    }
}
Write-Host "  Total headings (outline level 1-9): $headingCount"

Write-Host "`n=== TOC Update ==="
foreach ($toc in $doc.TablesOfContents) {
    Write-Host "  TOC before: Count=$($toc.Count)"
    Write-Host "  TOC.Range.Text (first 200 chars): $($toc.Range.Text.Substring(0, [Math]::Min(200, $toc.Range.Text.Length)))"
    
    # 强制更新域 + 更新页码
    $toc.Update()
    $toc.UpdatePageNumbers()
    $toc.Update()  # 再更新一遍
    
    Write-Host "  TOC after: Count=$($toc.Count)"
    
    # 强制将 TOC 转换为普通文本看看内容
    # 不行，那会破坏域
}

# 对所有 Heading 段落检查是否真的被标了 outline level
Write-Host "`n=== Force outline level check ==="
for ($i = 1; $i -le $doc.Paragraphs.Count; $i++) {
    $p = $doc.Paragraphs.Item($i)
    $styleName = $p.Style.NameLocal
    if ($styleName -match 'Heading') {
        $ol = $p.OutlineLevel
        Write-Host "  P[$i] Style='$styleName' OutlineLevel=$ol Text=$($p.Range.Text.Trim().Substring(0, [Math]::Min(40, $p.Range.Text.Trim().Length)))"
    }
}

# 再保存
$doc.Save()
$doc.Close()
$word.Quit()
[void][System.Runtime.Interopservices.Marshal]::ReleaseComObject($doc)
[void][System.Runtime.Interopservices.Marshal]::ReleaseComObject($word)
Start-Sleep -Seconds 3

Write-Host "`n=== DONE, now opening visible Word ==="
Start-Process winword.exe -ArgumentList "`"$tmpDoc`""
