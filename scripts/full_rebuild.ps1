# full_rebuild.ps1 - 完整重建论文 Word（含引用角标上标 + TOC 域 + PAGE 域更新）
$ErrorActionPreference = "Continue"

$srcRoot = "c:\Users\76955\OneDrive\桌面\medical"
$tmpRoot = "$env:TEMP\thesis_work2"
$outDoc = "$srcRoot\论文\论文_含引用角标.docx"

Write-Host "=== 1. 准备临时目录 ===" -ForegroundColor Cyan
Remove-Item $tmpRoot -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path "$tmpRoot\论文" -Force | Out-Null
Copy-Item -LiteralPath "$srcRoot\论文\实验数据" -Destination "$tmpRoot\论文\" -Recurse -Force
Get-ChildItem "$srcRoot\论文\*.md" | Copy-Item -Destination "$tmpRoot\论文\" -Force
Write-Host "  临时目录 OK"

Write-Host "`n=== 2. 用 python-docx 重新生成 Word ===" -ForegroundColor Cyan
& "$srcRoot\.venv\Scripts\python.exe" -c @"
import sys
sys.path.insert(0, r'$srcRoot')
sys.path.insert(0, r'$srcRoot\scripts')
import export_thesis_docx as m
from pathlib import Path
tmp = Path(r'$tmpRoot')
m.ROOT = tmp
m.THESIS_MD = tmp / '论文' / '基于多源医学知识融合与混合检索的医疗智能问答系统设计与实现.md'
m.THESIS_DOCX = tmp / '论文' / 'thesis.docx'
m.FIG_DIR = tmp / '论文' / '实验数据' / 'figures'
print(f'Root = {tmp}')
print(f'MD exists: {m.THESIS_MD.exists()}')
print(f'FIG_DIR exists: {m.FIG_DIR.exists()}')
m.main()
"@
if ($LASTEXITCODE -ne 0) { Write-Host "生成失败!" -ForegroundColor Red; exit 1 }
$tmpDoc = "$tmpRoot\论文\thesis.docx"
Write-Host "  Word 已生成: $tmpDoc ($((Get-Item $tmpDoc).Length / 1MB -as [int]) MB)"

Write-Host "`n=== 3. Word COM 更新所有域 ===" -ForegroundColor Cyan
# 先杀残留
Get-Process | Where-Object { $_.ProcessName -match 'WINWORD' } | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
$doc = $word.Documents.Open($tmpDoc)
Start-Sleep -Seconds 3

$word.ActiveWindow.View.Type = 3  # wdPrintView
Start-Sleep -Seconds 2

# TOC
$tocEntries = 0
foreach ($toc in $doc.TablesOfContents) {
    $toc.Update()
    $toc.UpdatePageNumbers()
    $toc.Update()
    $tocEntries += $toc.Count
}
Write-Host "  TOC: $tocEntries 个条目"

# Footer PAGE 域
foreach ($sec in $doc.Sections) {
    try {
        $word.ActiveWindow.View.SeekView = 9  # Footer
        Start-Sleep -Milliseconds 300
        $sec.Footers.Item(1).Range.Fields.Update() | Out-Null
    } catch {}
}
$word.ActiveWindow.View.SeekView = 0

# 全量 Fields.Update
$word.Selection.WholeStory()
$total = $word.Selection.Fields.Update()
Write-Host "  全文档更新: $total 个域"

# 保存
$doc.Save()
Write-Host "  已保存"

# 输出文件（避开 OneDrive 锁）
Write-Host "`n=== 4. SaveAs 到目标位置 ===" -ForegroundColor Cyan
try { Remove-Item "$outDoc" -Force -ErrorAction SilentlyContinue } catch {}
$doc.SaveAs2($outDoc, 16)  # wdFormatXMLDocument
Write-Host "  SaveAs2 OK" -ForegroundColor Green

$doc.Close()
$word.Quit()
[void][System.Runtime.Interopservices.Marshal]::ReleaseComObject($doc)
[void][System.Runtime.Interopservices.Marshal]::ReleaseComObject($word)
Start-Sleep -Seconds 3

Write-Host "`n=== 5. 验证 ===" -ForegroundColor Cyan
$word2 = New-Object -ComObject Word.Application
$word2.Visible = $false
$word2.DisplayAlerts = 0
$doc2 = $word2.Documents.Open($outDoc)
Start-Sleep -Seconds 3

$word2.ActiveWindow.View.Type = 3
$word2.ActiveWindow.View.SeekView = 9
Start-Sleep -Milliseconds 300
$ftrText = ""
try { $ftrText = $doc2.Sections.Item(1).Footers.Item(1).Range.Text.Trim() } catch {}
$word2.ActiveWindow.View.SeekView = 0

$tocFirst = ($doc2.TablesOfContents.Item(1).Range.Text -split "`n") | Select-Object -First 8
Write-Host "  页脚: '$ftrText'"
Write-Host "  TOC 前 8 行:"
$tocFirst | ForEach-Object { Write-Host "    $_" }

# 检查正文引用角标：统计 superscript run 数
$superscriptCount = 0
for ($pIdx = 1; $pIdx -le [Math]::Min(200, $doc2.Paragraphs.Count); $pIdx++) {
    try {
        $p = $doc2.Paragraphs.Item($pIdx)
        foreach ($run in $p.Range.Runs) {
            if ($run.Font.Superscript) {
                $superscriptCount++
            }
        }
    } catch {}
}
Write-Host "  前 200 段 superscript run 数: $superscriptCount (期望 ~50+)"

$doc2.Close()
$word2.Quit()
[void][System.Runtime.Interopservices.Marshal]::ReleaseComObject($doc2)
[void][System.Runtime.Interopservices.Marshal]::ReleaseComObject($word2)

Write-Host "`n=== 完成! 打开 Word 查看 ===" -ForegroundColor Green
Start-Process winword.exe -ArgumentList "`"$outDoc`""
Write-Host "文件: $outDoc"
