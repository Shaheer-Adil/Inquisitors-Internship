# TEMPORARY: Diagnostic test script to measure latency
$BaseUrl = "http://127.0.0.1:8000/chat"
$SessionId = "diag-session-$(Get-Date -Format 'yyyyMMddHHmmss')"
$UserId = "diag-user"

$TestMessages = @(
    "Hi",
    "I am feeling stressed today and I have so much work to finish.",
    "I did really well today and I am very happy about it.",
    "I feel sad and lonely today."
)

Write-Host "`n$('='*80)" -ForegroundColor Cyan
Write-Host "LATENCY DIAGNOSTIC TEST - Starting" -ForegroundColor Cyan
Write-Host "$('='*80)`n" -ForegroundColor Cyan

foreach ($i in 0..3) {
    $Message = $TestMessages[$i]
    $TestNum = $i + 1
    
    Write-Host "TEST $TestNum - Message: '$Message'" -ForegroundColor Yellow
    Write-Host "Sending request..." -ForegroundColor Gray
    
    $Body = @{
        message = $Message
        session_id = $SessionId
        user_id = $UserId
    } | ConvertTo-Json
    
    $RequestStart = Get-Date
    
    try {
        $Response = Invoke-WebRequest -Uri $BaseUrl `
            -Method Post `
            -Body $Body `
            -ContentType "application/json" `
            -UseBasicParsing `
            -TimeoutSec 60
        
        $RequestEnd = Get-Date
        $TotalTime = ($RequestEnd - $RequestStart).TotalMilliseconds
        
        Write-Host "✓ Response received in $([Math]::Round($TotalTime, 2)) ms" -ForegroundColor Green
        Write-Host "Status Code: $($Response.StatusCode)" -ForegroundColor Green
        
        $ResponseObj = $Response.Content | ConvertFrom-Json
        Write-Host "Response length: $($ResponseObj.response.Length) chars" -ForegroundColor Gray
        
    } catch {
        Write-Host "✗ Error: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "-" * 80
    Write-Host ""
    
    # Give server a brief moment between requests
    Start-Sleep -Milliseconds 500
}

Write-Host "$('='*80)" -ForegroundColor Cyan
Write-Host "LATENCY DIAGNOSTIC TEST - Complete" -ForegroundColor Cyan
Write-Host "$('='*80)`n" -ForegroundColor Cyan
Write-Host "Note: Check the backend terminal for detailed timing breakdowns" -ForegroundColor Yellow
