# 最终步骤：杀掉 OneDrive → 复制 → 打开
$srcRoot = "c:\Users\76955\OneDrive\桌面\medical"
$origDoc = "$srcRoot\论文\基于多源医学知识融合与混合检索的医疗智能问答系统设计与实现.docx"
$tmpDoc = "$env:TEMP\thesis_work\论文\基于多源医学知识融合与混合检索的医疗智能问答系统设计与实现.docx"

Write-Host "=== 杀进程 ==="
Get-Process | Where-Object { $_.ProcessName -match 'WINWORD|OneDrive' } | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 3
Write-Host "  已清理"

Write-Host "`n=== 验证临时 docx 的 TOC + Footer ==="
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
$doc = $word.Documents.Open($tmpDoc)
Start-Sleep -Seconds 2
$word.ActiveWindow.View.Type = 3  # PrintView
Start-Sleep -Seconds 2

# 检查 TOC
$tocText = $doc.TablesOfContents.Item(1).Range.Text.Trim()
$firstLines = ($tocText -split "`n") | Select-Object -First 10
Write-Host "  TOC 前 10 行:"
foreach ($line in $firstLines) { Write-Host "    $line" }

# 检查 Footer
$word.ActiveWindow.View.SeekView = 9  # Footer
Start-Sleep -Milliseconds 500
$footerText = $doc.Sections.Item(1).Footers.Item(1).Range.Text.Trim()
Write-Host "`n  Footer 文本: '$footerText'"

$doc.Close()
$word.Quit()
[void][System.Runtime.Interopservices.Marshal]::ReleaseComObject($doc)
[void][System.Runtime.Interopservices.Marshal]::ReleaseComObject($word)
Start-Sleep -Seconds 2

Write-Host "`n=== 备份旧文件 + 复制新文件 ==="
if (Test-Path $origDoc) {
    Copy-Item -LiteralPath $origDoc -Destination "$origDoc.bak" -Force
    Write-Host "  备份完成"
}

# 重试复制（可能 OneDrive 很快重开）
$copied = $false
for ($retry = 0; $retry -lt 10; $retry++) {
    try {
        Copy-Item -LiteralPath $tmpDoc -Destination $origDoc -Force -ErrorAction Stop
        $copied = $true
        Write-Host "  复制成功!"
        break
    } catch {
        Write-Host "  重试 $($retry+1)/10 ..."
        Start-Sleep -Seconds 2
        Get-Process | Where-Object { $_.ProcessName -match 'OneDrive' } | Stop-Process -Force -ErrorAction SilentlyContinue
    }
}

if (-not $copied) {
    Write-Host "复制失败，临时文件在: $tmpDoc" -ForegroundColor Red
    Write-Host "请手动复制或关闭 OneDrive 后重试" -ForegroundColor Red
} else {
    Write-Host "`n=== 打开 Word 查看 ===" -ForegroundColor Green
    Start-Process winword.exe -ArgumentList "`"$origDoc`""
}
