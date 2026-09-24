param(
    [string]$GamePath = 'D:\ai\codex\classic-tavern-service-game',
    [string]$KeyPath = (Join-Path (Split-Path -Parent $PSScriptRoot) 'secrets\deploy.pem')
)
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $root
$engine=Join-Path $root 'artifacts\engine\Godot_v4.6.1-stable_linux.x86_64'
if (!(Test-Path -LiteralPath $engine)) {throw 'Download and verify the official Godot 4.6.1 Linux editor binary in artifacts/engine first; export templates do not support the raw-script server.'}
foreach($name in 'ClassicTavern-Service.exe','ClassicTavern-Service.apk') {
    if (!(Test-Path -LiteralPath (Join-Path $GamePath "build\$name"))) {throw "Missing tested client: $name"}
}
python deploy/bundle.py $GamePath $engine
if ($LASTEXITCODE -ne 0) {throw 'Bundle failed'}
scp -i $KeyPath artifacts/service.tar.gz ubuntu@bjckwrn.xyz:/home/ubuntu/service.tar.gz
if ($LASTEXITCODE -ne 0) {throw 'Upload failed'}
ssh -i $KeyPath ubuntu@bjckwrn.xyz 'mkdir -p /home/ubuntu/tavern-install && tar -xzf /home/ubuntu/service.tar.gz -C /home/ubuntu/tavern-install deploy/install.sh && sudo bash /home/ubuntu/tavern-install/deploy/install.sh'
if ($LASTEXITCODE -ne 0) {throw 'Install refused or failed; existing rooms may need draining'}
ssh -i $KeyPath ubuntu@bjckwrn.xyz 'sudo certbot --nginx -d bjckwrn.xyz --non-interactive --agree-tos --register-unsafely-without-email --redirect --keep-until-expiring'
if ($LASTEXITCODE -ne 0) {throw 'TLS setup failed'}
foreach($name in 'ClassicTavern-Service.exe','ClassicTavern-Service.apk') {
    scp -i $KeyPath (Join-Path $GamePath "build\$name") "ubuntu@bjckwrn.xyz:/home/ubuntu/$name"
    if ($LASTEXITCODE -ne 0) {throw "Client upload failed: $name"}
    ssh -i $KeyPath ubuntu@bjckwrn.xyz "sudo install -m 644 /home/ubuntu/$name /var/www/classic-tavern/downloads/$name.new && sudo mv /var/www/classic-tavern/downloads/$name.new /var/www/classic-tavern/downloads/$name"
    if ($LASTEXITCODE -ne 0) {throw "Client publication failed: $name"}
}
Invoke-RestMethod https://bjckwrn.xyz/api/health
