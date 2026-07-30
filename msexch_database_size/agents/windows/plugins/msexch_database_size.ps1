## Load Exchange Management Powershell Plugin
try{ (Add-PSSnapin Microsoft.Exchange.Management.PowerShell.E2010 -ErrorAction:Stop) }

## exit without any output if this fails
catch{exit}

Write-Host '<<<msexch_database_size:sep(59)>>>'
Get-MailboxDatabase -Status -Server $env:COMPUTERNAME | Where-Object {$_.Mounted -eq $true -and $_.Server.Name -eq $env:COMPUTERNAME} | select Name,DatabaseSize,AvailableNewMailboxSpace | ConvertTo-CSV -NoTypeInformation -Delimiter ";"
