Write-Host '<<<sslcertificates:sep(0)>>>'

$UnixEpoch = (Get-Date -Date "01/01/1970") ;

$CertLocations = "Cert:\LocalMachine\My", "Cert:\CurrentUser\My"

foreach ($CertLocation in $CertLocations) {
  foreach ($_ in Get-ChildItem -Recurse $CertLocation) {
    If ($_.DnsNameList) {$subject = $_.DnsNameList}
    ElseIf ($_.Subject) {$subject = $_.Subject}
    Else {$subject = $_.Thumbprint}

    # Reverse issuer, so it starts with e.g. C=US to match the output of the Linux agent.
    $issuer = $_.Issuer -split ',' | ForEach-Object { $_.Trim() }
    [array]::Reverse($issuer)
    $issuer = $issuer -join ','

    $data = [ordered]@{
      starts = (New-TimeSpan -Start $UnixEpoch -End $_.NotBefore).TotalSeconds ;
      expires = (New-TimeSpan -Start $UnixEpoch -End $_.NotAfter).TotalSeconds ;
      subj = $subject.Unicode ;
      thumb = $_.Thumbprint ;
      issuer = $issuer ;
      algosign = $_.SignatureAlgorithm.FriendlyName ;
    }

    $data | ConvertTo-Json -Compress
  }
}
