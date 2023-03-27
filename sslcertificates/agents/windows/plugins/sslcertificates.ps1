
Write-Host '<<<sslcertificates:sep(0)>>>'

$UnixEpoch = (Get-Date -Date "01/01/1970") ;

foreach ($_ in Get-ChildItem -Recurse Cert:\LocalMachine\My) {
  If ($_.DnsNameList) {$subject = $_.DnsNameList}
  ElseIf ($_.Subject) {$subject = $_.Subject}
  Else {$subject = $_.Thumbprint}

  $data = [ordered]@{
    starts = (New-TimeSpan -Start $UnixEpoch -End $_.NotBefore).TotalSeconds ;
    expires = (New-TimeSpan -Start $UnixEpoch -End $_.NotAfter).TotalSeconds ;
    subj = $subject.Unicode ;
    thumb = $_.Thumbprint ;
    algosign = $_.SignatureAlgorithm.FriendlyName ;
  }

  $data | ConvertTo-Json -Compress
}

foreach ($_ in Get-ChildItem -Recurse Cert:\CurrentUser\My) {
  If ($_.DnsNameList) {$subject = $_.DnsNameList}
  ElseIf ($_.Subject) {$subject = $_.Subject}
  Else {$subject = $_.Thumbprint}

  $data = [ordered]@{
    starts = (New-TimeSpan -Start $UnixEpoch -End $_.NotBefore).TotalSeconds ;
    expires = (New-TimeSpan -Start $UnixEpoch -End $_.NotAfter).TotalSeconds ;
    subj = $subject.Unicode ;
    thumb = $_.Thumbprint ;
    algosign = $_.SignatureAlgorithm.FriendlyName ;
  }

  $data | ConvertTo-Json -Compress
}
