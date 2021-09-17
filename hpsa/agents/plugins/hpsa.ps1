# check_mk check f. HP Smart Array Controller

#
# WINDOWS VERSION
#

# 09/2021 Gianluca Stella

# Based on the work of
# 			Christophe Robert - christophe °dot° robert °at° cocoche °dot° fr
#			Daniel Beardsmore [DGB] - daniel °at° trustnetworks °dot° co °dot° uk
# on check_smartarray.ps1 nagios plugin
# https://exchange.nagios.org/directory/Plugins/Hardware/Server-Hardware/HP-%28Compaq%29/NRPE-script-for-HP-SmartArray-checks/details

# sample output
#
# hpssacli controller all show config
# 
# Smart Array P410i in Slot 0 (Embedded)    (sn: 50014380230B12F0)
# 
# 
# 
#    Internal Drive Cage at Port 1I, Box 1, OK
# 
# 
# 
#    Internal Drive Cage at Port 2I, Box 1, OK
# 
# 
#    Port Name: 1I
# 
#    Port Name: 2I
# 
#    Array A (SAS, Unused Space: 0  MB)
# 
#       logicaldrive 1 (558.73 GB, RAID 1+0, OK)
# 
#       physicaldrive 1I:1:1 (port 1I:box 1:bay 1, SAS HDD, 300 GB, OK)
#       physicaldrive 1I:1:2 (port 1I:box 1:bay 2, SAS HDD, 300 GB, OK)
#       physicaldrive 1I:1:3 (port 1I:box 1:bay 3, SAS HDD, 300 GB, OK)
#       physicaldrive 1I:1:4 (port 1I:box 1:bay 4, SAS HDD, 300 GB, OK)
# 
#    SEP (Vendor ID PMCSIERA, Model  SRC 8x6G) 250  (WWID: 50014380230B12FF)
# 

Function Get-Storage-Executable-Path () {
    $programPaths = (
    	'C:\Program Files\HP\HPSSACLI\bin\hpssacli.exe',
        'C:\Program Files\HP\HPACUCLI\Bin\hpacucli.exe',
        'C:\Program Files\Compaq\HPACUCLI\Bin\hpacucli.exe',
        'C:\Program Files (x86)\HP\HPACUCLI\Bin\hpacucli.exe',
        'C:\Program Files (x86)\Compaq\HPACUCLI\Bin\hpacucli.exe'
    );
    
    foreach ($path in $programPaths) {
        if (Test-Path $path) {
            return $path
        }
    }
    
    return $false
}


$prg = Get-Storage-Executable-Path
if ($prg -eq $false) {
    Write-Host "HP RAID check tool not installed."
    exit 0
}


Write-Host "<<<hpsa>>>"
try
{
	$exec = & $prg ' controller all show config'
	$output = $exec -join "`r`n"
	Write-Host $output	
}
catch
{
	Write-Host  $_.Exception.Message
}
