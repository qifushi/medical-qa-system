# update_thesis_fields.ps1 - 完整流程：重新生成 Word → COM 更新所有域 → 打开查看
$ErrorActionPreference = "Stop"

$srcRoot = "c:\Users\76955\OneDrive\桌面\medical"
$tmpRoot = "$env:TEMP\thesis_work"
$origDoc = "$srcRoot\论文\基于多源医学知识融合与混合检索的医疗智能问答系统设计与实现.docx"
$tmpDoc = "$tmpRoot\论文\基于多源医学知识融合与混合检索的医疗智能问答系统设计与实现.docx"

Write-Host "=== Step 1: 准备临时目录 ===" -ForegroundColor Cyan
Remove-Item "$tmpRoot" -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path "$tmpRoot\论文" -Force | Out-Null
Copy-Item -LiteralPath "$srcRoot\论文\实验数据" -Destination "$tmpRoot\论文\" -Recurse -Force
Get-ChildItem "$srcRoot\论文\*.md" | Copy-Item -Destination "$tmpRoot\论文\" -Force
Write-Host "  临时目录就绪"

Write-Host "`n=== Step 2: 用 python-docx 重新生成 Word ===" -ForegroundColor Cyan
& "$srcRoot\.venv\Scripts\python.exe" -c @"
import sys
sys.path.insert(0, r'$srcRoot')
sys.path.insert(0, r'$srcRoot\scripts')
import export_thesis_docx as m
from pathlib import Path
tmp = Path(r'$tmpRoot')
m.ROOT = tmp
m.THESIS_MD = tmp / '论文' / '基于多源医学知识融合与混合检索的医疗智能问答系统设计与实现.md'
m.THESIS_DOCX = tmp / '论文' / '基于多源医学知识融合与混合检索的医疗智能问答系统设计与实现.docx'
m.FIG_DIR = tmp / '论文' / '实验数据' / 'figures'
m.main()
print('REGENERATED OK')
"@
if ($LASTEXITCODE -ne 0) { Write-Host "生成失败!" -ForegroundColor Red; exit 1 }
Write-Host "  Word 重新生成成功"

Write-Host "`n=== Step 3: Word COM 更新所有域 ===" -ForegroundColor Cyan
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
$doc = $word.Documents.Open($tmpDoc)
Start-Sleep -Seconds 2

Write-Host "  视图切到打印模式..."
$word.ActiveWindow.View.Type = 3  # wdPrintView
Start-Sleep -Seconds 2

# 更新 TOC
$tocCount = 0
foreach ($toc in $doc.TablesOfContents) {
    $toc.Update()
    $tocCount++
}
Write-Host "  TOC 域更新完成 ($tocCount 个 TOC)"

# 切换到页脚视图更新 PAGE 域
$word.ActiveWindow.View.SeekView = 9  # wdSeekCurrentPageFooter
Start-Sleep -Milliseconds 500
$pageFieldCount = 0
foreach ($sec in $doc.Sections) {
    try {
        $f = $sec.Footers.Item(1)
        $pageFieldCount += $f.Range.Fields.Update()
    } catch {}
}
Write-Host "  PAGE 页码域更新完成"

# 切回主文档，全选再更新一遍确保无遗漏
$word.ActiveWindow.View.SeekView = 0  # wdSeekMainDocument
$word.Selection.WholeStory()
$totalUpdated = $word.Selection.Fields.Update()
Write-Host "  全文档 Fields.Update(): $totalUpdated 个域"

# 保存
$doc.Save()
$doc.Close()
$word.Quit()
[void][System.Runtime.Interopservices.Marshal]::ReleaseComObject($doc)
[void][System.Runtime.Interopservices.Marshal]::ReleaseComObject($word)
Start-Sleep -Seconds 3
Write-Host "  COM 更新完毕，已保存"

# 验证一下
Write-Host "`n=== Step 4: 验证 ===" -ForegroundColor Cyan
$word2 = New-Object -ComObject Word.Application
$word2.Visible = $false
$word2.DisplayAlerts = 0
$doc2 = $word2.Documents.Open($tmpDoc)
Start-Sleep -Seconds 2

$word2.ActiveWindow.View.Type = 3
$word2.ActiveWindow.View.SeekView = 9
Start-Sleep -Milliseconds 500

foreach ($sec in $doc2.Sections) {
    try {
        $footerText = $sec.Footers.Item(1).Range.Text.Trim()
        Write-Host "  Footer text: '$footerText'"
    } catch {}
}

$tocEntryCount = 0
foreach ($toc in $doc2.TablesOfContents) {
    $tocEntryCount += $toc.Count
}
Write-Host "  TOC entries: $tocEntryCount"

$doc2.Close()
$word2.Quit()
[void][System.Runtime.Interopservices.Marshal]::ReleaseComObject($doc2)
[void][System.Runtime.Interopservices.Marshal]::ReleaseComObject($word2)

Write-Host "`n=== Step 5: 复制回原位置 ===" -ForegroundColor Cyan
# 先关闭任何占用原文件的进程
Get-Process | Where-Object { $_.ProcessName -match 'WINWORD' } | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# 备份旧文件
if (Test-Path $origDoc) {
    $bak = "$origDoc.bak"
    Copy-Item -LiteralPath $origDoc -Destination $bak -Force
    Write-Host "  备份原文件 → $bak"
}

# 复制新文件
Copy-Item -LiteralPath $tmpDoc -Destination $origDoc -Force
Write-Host "  已复制到: $origDoc"

Write-Host "`n=== Step 6: 打开 Word 查看 ===" -ForegroundColor Green
Start-Process winword.exe -ArgumentList "`"$origDoc`""

Write-Host "`n=== 全部完成 ===" -ForegroundColor Green
Write-Host "请检查：目录是否有章节条目 + 页脚页码是否正确"
