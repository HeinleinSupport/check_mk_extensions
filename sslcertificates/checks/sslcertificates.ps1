
Write-Host '<<<sslcertificates>>>'

foreach ($_ in Get-ChildItem -Recurse Cert:\LocalMachine\My) {
  $expires = (New-TimeSpan -Start (Get-Date -Date "01/01/1970") -End $_.NotAfter).TotalSeconds

  If ($_.DnsNameList) {$subject = $_.DnsNameList}
  ElseIf ($_.Subject) {$subject = $_.Subject}
  Else {$subject = $_.Thumbprint}

  Write-Host $_.Thumbprint $expires $_.SignatureAlgorithm.FriendlyName $subject
}

foreach ($_ in Get-ChildItem -Recurse Cert:\CurrentUser\My) {
  $expires = (New-TimeSpan -Start (Get-Date -Date "01/01/1970") -End $_.NotAfter).TotalSeconds

  If ($_.DnsNameList) {$subject = $_.DnsNameList}
  ElseIf ($_.Subject) {$subject = $_.Subject}
  Else {$subject = $_.Thumbprint}

  Write-Host $_.Thumbprint $expires $_.SignatureAlgorithm.FriendlyName $subject
}
