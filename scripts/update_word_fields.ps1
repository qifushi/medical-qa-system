# update_word_fields.ps1 - 更新 Word 文档中的目录(TOC)和页码(PAGE)域
# 用法: .\scripts\update_word_fields.ps1
$ErrorActionPreference = "Continue"

$docPath = Join-Path $PSScriptRoot "..\论文\基于多源医学知识融合与混合检索的医疗智能问答系统设计与实现.docx"
$docPath = [System.IO.Path]::GetFullPath($docPath)

if (-not (Test-Path $docPath)) {
    Write-Host "[错误] 文件不存在: $docPath" -ForegroundColor Red
    exit 1
}
Write-Host "目标文档: $docPath" -ForegroundColor Cyan

# ---------- 第一阶段：静默更新域 ----------
try {
    Write-Host "启动 Word COM..."
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0  # wdAlertsNone
    
    Write-Host "打开文档..."
    $doc = $word.Documents.Open($docPath, $false, $false)  # FileName, ConfirmConversions, ReadOnly
    Write-Host "已打开: $($doc.Name)"
    
    # 全选文档
    $word.Selection.WholeStory()
    
    # 更新所有域
    Write-Host "正在更新所有域..."
    $updated = $word.Selection.Fields.Update()
    Write-Host "已更新 $updated 个域 (TOC 目录 + PAGE 页码)" -ForegroundColor Green
    
    # 保存并关闭
    $doc.Save()
    $doc.Close()
    [void][System.Runtime.Interopservices.Marshal]::ReleaseComObject($doc)
    
    $word.Quit()
    [void][System.Runtime.Interopservices.Marshal]::ReleaseComObject($word)
    
    # 等待 Word 进程完全退出
    Write-Host "等待 COM 清理..."
    Start-Sleep -Seconds 3
    
    Write-Host "域更新完成！" -ForegroundColor Green
}
catch {
    Write-Host "[错误] $_" -ForegroundColor Red
    try { if ($word) { $word.Quit() } } catch {}
    exit 1
}

# ---------- 第二阶段：重新打开让用户查看 ----------
Write-Host "正在重新打开文档..."
Start-Process -FilePath "winword.exe" -ArgumentList "`"$docPath`""
Write-Host "完成！请检查目录和页码是否正确显示。" -ForegroundColor Cyan
