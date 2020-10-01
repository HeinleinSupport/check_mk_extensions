
Write-Host '<<<msexch_database_size:sep(59)>>>'
Get-MailboxDatabase -Status | select Name,DatabaseSize | ConvertTo-CSV -NoTypeInformation -Delimiter ";"
