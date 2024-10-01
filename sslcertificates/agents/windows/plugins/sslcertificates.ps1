function Get-CertificateTemplateName($certificate)
{
  # The template name is stored in the Extension data.
  # If available, the best is the extension named "Certificate Template Name", since it contains the exact name.
  $templateExt = $certificate.Extensions | Where-Object{ ( $_.Oid.Value -eq '1.3.6.1.4.1.311.20.2' ) } | Select-Object -First 1
  if ($templateExt) {
    return [string]::join("", $templateExt.Format(1).Split("`r`n"))
  }

  # Our fallback option is the "Certificate Template Information" extension, it contains the name as part of a string like:
  # "Template=Web Server v2(1.3.6.1.4.1.311.21.8.2499889.12054413.13650051.8431889.13164297.111.14326010.6783216)"
  $templateExt = $certificate.Extensions | Where-Object{ ( $_.Oid.Value -eq '1.3.6.1.4.1.311.21.7' ) } | Select-Object -First 1
  if ($templateExt) {
    $information = $templateExt.Format(1)

    # Extract just the template name in $Matches[1]
    if($information -match "^\w+=(.+)\([0-9\.]+\)") {
      return [string]::join("", $Matches[1].Split("`r`n"))
    } else {
      # No regex match, just return the complete information then
      return [string]::join("", $information.Split("`r`n"))
    }
  } else {
    # No template name found
    return $null
  }
}

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
      template = Get-CertificateTemplateName($_) ;
    }

    $data | ConvertTo-Json -Compress
  }
}
