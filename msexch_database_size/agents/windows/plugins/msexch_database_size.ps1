## Load Exchange Management Powershell Plugin
try{ (Add-PSSnapin Microsoft.Exchange.Management.PowerShell.E2010 -ErrorAction:Stop) }

## exit without any output if this fails
catch{exit}

Write-Host '<<<msexch_database_size:sep(59)>>>'
Get-MailboxDatabase -Status | select Name,DatabaseSize | ConvertTo-CSV -NoTypeInformation -Delimiter ";"
