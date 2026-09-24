param(
    [string]$Root = (Split-Path -Parent $PSScriptRoot),
    [string]$Destination = "",
    [string]$TaskName = 'ClassicTavern-BackupReceiver'
)
$ErrorActionPreference='Stop'
if (!$Destination) {$Destination=Join-Path $Root 'backups'}
$python=(Get-Command python.exe).Source
$pythonw=Join-Path (Split-Path $python) 'pythonw.exe'
$script=Join-Path $Root 'deploy\pull_backups.py'
$key=Join-Path $Root 'secrets\deploy.pem'
$arguments='"'+$script+'" --key "'+$key+'" --destination "'+$Destination+'"'
$action=New-ScheduledTaskAction -Execute $pythonw -Argument $arguments -WorkingDirectory $Root
$hourly=New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(2) -RepetitionInterval (New-TimeSpan -Hours 1)
$logon=New-ScheduledTaskTrigger -AtLogOn -User ([System.Security.Principal.WindowsIdentity]::GetCurrent().Name)
$settings=New-ScheduledTaskSettingsSet -StartWhenAvailable -RunOnlyIfNetworkAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit (New-TimeSpan -Minutes 15) -MultipleInstances IgnoreNew
$principal=New-ScheduledTaskPrincipal -UserId ([System.Security.Principal.WindowsIdentity]::GetCurrent().Name) -LogonType Interactive -RunLevel Limited
Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger @($hourly,$logon) -Settings $settings -Principal $principal -Description 'Pull and verify encrypted daily game-account backups; catch up when this computer is online.' -Force | Select-Object TaskName,State
Start-ScheduledTask -TaskName $TaskName
