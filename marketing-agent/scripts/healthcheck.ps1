# Marketing Agent MCP Saglik Kontrolu
# Kullanim: .\scripts\healthcheck.ps1
# Cikti: Her MCP sunucusu icin OK/FAIL + versiyon

$ErrorActionPreference = "Continue"
$Root = Split-Path -Parent $PSScriptRoot

Write-Output "========================================"
Write-Output " Marketing Agent MCP Health Check"
Write-Output " $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Write-Output "========================================"
Write-Output ""

$all_ok = $true

# --- mcp-appstore ---
Write-Output "--- mcp-appstore ---"
$appstore_server = Join-Path $Root "vendor\mcp-appstore\server.js"
if (Test-Path $appstore_server) {
    Write-Output "  Dosya: OK ($appstore_server)"
    try {
        $ver = node -e "console.log(require('$($Root.Replace('\','/'))/vendor/mcp-appstore/package.json').version)" 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Output "  Version: $ver"
            Write-Output "  Node.js: $(node --version)"
            Write-Output "  Durum: OK"
        } else {
            Write-Output "  Durum: FAIL — node calismadi. Node.js 18+ gerekli."
            $all_ok = $false
        }
    } catch {
        Write-Output "  Durum: FAIL — $_"
        $all_ok = $false
    }
} else {
    Write-Output "  Durum: FAIL — $appstore_server bulunamadi."
    Write-Output "  Fix: git clone https://github.com/appreply-co/mcp-appstore vendor/mcp-appstore"
    Write-Output "       npm install --prefix vendor/mcp-appstore"
    $all_ok = $false
}

Write-Output ""

# --- Webwright ---
Write-Output "--- webwright ---"
$webwright_dir = Join-Path $Root "vendor\webwright"
if (Test-Path $webwright_dir) {
    Write-Output "  Dosya: OK ($webwright_dir)"
    try {
        $py_ver = python --version 2>&1
        Write-Output "  Python: $py_ver"
        Write-Output "  Durum: OK (manuel install gerektirir: pip install -e vendor/webwright; playwright install chromium)"
    } catch {
        Write-Output "  Durum: WARN — Python bulunamadi. pip install yapilamaz."
    }
} else {
    Write-Output "  Durum: WARN — vendor/webwright bulunamadi (opsiyonel)."
    Write-Output "  Fix: git clone https://github.com/microsoft/Webwright vendor/webwright"
    Write-Output "       pip install -e vendor/webwright"
    Write-Output "       playwright install chromium"
}

Write-Output ""

# --- Python Scripts ---
Write-Output "--- Python Scripts ---"
$scripts = @("google_trends.py", "reddit_scraper.py", "estimate_revenue.py", "analyze_page.py", "competitor_scanner.py", "generate_pdf_report.py", "social_calendar.py", "roi_calculator.py")
foreach ($s in $scripts) {
    $path = Join-Path $Root "scripts\$s"
    if (Test-Path $path) {
        Write-Output "  $s : OK"
    } else {
        Write-Output "  $s : MISSING"
        $all_ok = $false
    }
}

Write-Output ""

# --- Dependencies ---
Write-Output "--- Python Bagimliliklari ---"
$deps = @("pytrends", "reportlab")
foreach ($d in $deps) {
    try {
        $result = python -c "import $d; print($d.__version__)" 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Output "  $d : $result"
        } else {
            Write-Output "  $d : MISSING — pip install $d"
        }
    } catch {
        Write-Output "  $d : MISSING — pip install $d"
    }
}

Write-Output ""

# --- Skills ---
Write-Output "--- Skills ---"
$skills_dir = Join-Path $Root "skills"
$skill_count = (Get-ChildItem $skills_dir -Directory).Count
Write-Output "  Toplam skill: $skill_count"
if ($skill_count -lt 30) {
    Write-Output "  WARN: 36 skill bekleniyor, $skill_count bulundu."
    $all_ok = $false
}

Write-Output ""

# --- Templates ---
Write-Output "--- Templates ---"
$templates_dir = Join-Path $Root "templates"
$template_count = (Get-ChildItem $templates_dir -File).Count
Write-Output "  Toplam template: $template_count"

Write-Output ""
Write-Output "========================================"
if ($all_ok) {
    Write-Output " SONUC: TUM SISTEM HAZIR"
} else {
    Write-Output " SONUC: EKSIKLER VAR — yukaridaki FAIL/WARN satirlarina bak"
}
Write-Output "========================================"
