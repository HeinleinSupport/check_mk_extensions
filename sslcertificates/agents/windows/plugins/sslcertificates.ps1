#!/usr/bin/pwsh

# (c) 2013 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  This file is distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.


function Get-CertificateTemplateName($certificate)
{
  # The template name is stored in the Extension data.
  # If available, the best is the extension named "Certificate Template Name", since it contains the exact name.
  $templateExt = $certificate.Extensions | Where-Object{ ( $cert.Oid.Value -eq '1.3.6.1.4.1.311.20.2' ) } | Select-Object -First 1
  if ($templateExt) {
    return [string]::join("", $templateExt.Format(1).Split("`r`n"))
  }

  # Our fallback option is the "Certificate Template Information" extension, it contains the name as part of a string like:
  # "Template=Web Server v2(1.3.6.1.4.1.311.21.8.2499889.12054413.13650051.8431889.13164297.111.14326010.6783216)"
  $templateExt = $certificate.Extensions | Where-Object{ ( $cert.Oid.Value -eq '1.3.6.1.4.1.311.21.7' ) } | Select-Object -First 1
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
  foreach ($cert in Get-ChildItem -Recurse $CertLocation) {
    If ($cert.DnsNameList) {$subject = $cert.DnsNameList}
    ElseIf ($cert.Subject) {$subject = $cert.Subject}
    Else {$subject = $cert.Thumbprint}

    # Reverse issuer, so it starts with e.g. C=US to match the output of the Linux agent.
    $issuer = $cert.Issuer -split ',' | ForEach-Object { $_.Trim() }
    [array]::Reverse($issuer)
    $issuer = $issuer -join ','

    $data = [ordered]@{
      starts = (New-TimeSpan -Start $UnixEpoch -End $cert.NotBefore).TotalSeconds ;
      expires = (New-TimeSpan -Start $UnixEpoch -End $cert.NotAfter).TotalSeconds ;
      subj = $subject.Unicode ;
      thumb = $cert.Thumbprint ;
      issuer = $issuer ;
      algosign = $cert.SignatureAlgorithm.FriendlyName ;
      template = Get-CertificateTemplateName($cert) ;
    }

    $data | ConvertTo-Json -Compress
  }
}
