$tmpDoc = "C:\Users\76955\AppData\Local\Temp\thesis_work2\论文\thesis.docx"
$outDoc = "c:\Users\76955\OneDrive\桌面\medical\论文\论文_含引用角标.docx"

Write-Host "Kill WinWord..."
Get-Process | Where-Object { $_.ProcessName -match 'WINWORD' } | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 3

Write-Host "Open: $tmpDoc"
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
$doc = $word.Documents.Open($tmpDoc)
Start-Sleep -Seconds 3

# Print view
$word.ActiveWindow.View.Type = 3
Start-Sleep -Seconds 2

# TOC
$tocEntries = 0
foreach ($toc in $doc.TablesOfContents) {
    $toc.Update()
    $toc.UpdatePageNumbers()
    $toc.Update()
    $tocEntries += $toc.Count
}
Write-Host "TOC entries: $tocEntries"

# Footer PAGE
foreach ($sec in $doc.Sections) {
    try {
        $word.ActiveWindow.View.SeekView = 9
        Start-Sleep -Milliseconds 300
        $sec.Footers.Item(1).Range.Fields.Update() | Out-Null
    } catch {}
}
$word.ActiveWindow.View.SeekView = 0

# All fields
$word.Selection.WholeStory()
$total = $word.Selection.Fields.Update()
Write-Host "All fields updated: $total"

# SaveAs
Write-Host "SaveAs2 to: $outDoc"
try { Remove-Item "$outDoc" -Force -ErrorAction SilentlyContinue } catch {}
$doc.SaveAs2($outDoc, 16)
Write-Host "SaveAs OK ($((Get-Item $outDoc).Length / 1MB -as [int]) MB)"

$doc.Close()
$word.Quit()
Start-Sleep -Seconds 3

Write-Host "Open Word..."
Start-Process winword.exe -ArgumentList "`"$outDoc`""
