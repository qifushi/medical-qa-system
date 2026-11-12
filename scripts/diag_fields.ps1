$tmpDoc = "C:\Users\76955\AppData\Local\Temp\thesis_work\论文\基于多源医学知识融合与混合检索的医疗智能问答系统设计与实现.docx"
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
$doc = $word.Documents.Open($tmpDoc)

Write-Host "=== Main body fields: $($doc.Fields.Count) ==="

foreach ($sec in $doc.Sections) {
    Write-Host "`n--- Section ---"
    Write-Host "  Header fields: $($sec.Header.Range.Fields.Count)"
    Write-Host "  Footer fields: $($sec.Footer.Range.Fields.Count)"
    Write-Host "  Header TOCs: $($sec.Header.Range.TablesOfContents.Count)"
    Write-Host "  Footer TOCs: $($sec.Footer.Range.TablesOfContents.Count)"
}

Write-Host "`n=== TOCs in main doc: $($doc.TablesOfContents.Count) ==="
$idx = 0
foreach ($toc in $doc.TablesOfContents) {
    $idx++
    Write-Host "  TOC[$idx]: Count=$($toc.Count), Title=$($toc.Title)"
}

Write-Host "`n=== Listing main body fields ==="
for ($i = 1; $i -le $doc.Fields.Count; $i++) {
    $f = $doc.Fields.Item($i)
    Write-Host ("  Field {0}: Type={1}" -f $i, $f.Type)
    try { Write-Host ("    Code: {0}" -f $f.Code.Text) } catch { }
}

$doc.Close()
$word.Quit()
[void][System.Runtime.Interopservices.Marshal]::ReleaseComObject($doc)
[void][System.Runtime.Interopservices.Marshal]::ReleaseComObject($word)
