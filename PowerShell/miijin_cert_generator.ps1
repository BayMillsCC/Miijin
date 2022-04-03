# Define where OpenSSL is installed
$openSSLDir = "C:\Program Files\OpenSSL-Win64\bin"

# Define the domain we're generating the CSR for
$commonName = Read-Host -Prompt "Provide the domain you're generating a certificate for"
$password = Read-Host -Prompt "Provide a password you want to secure the private key with"
$fileName = Read-Host -Prompt "Provide a filename you want to save the keys and certs as"
$daysExpired = Read-Host -Prompt "How many days do you want the cert to be valid for? "

# Define the default parameters on the certificate
$email = Read-Host -Prompt "Email Address"
$country = Read-Host -Prompt "2-Letter Country Code"
$state = Read-Host -Prompt "State"
$locality = Read-Host -Prompt "City"
$orgUnit = Read-Host -Prompt "Organizational Unit"
$org = Read-Host -Prompt "Company Name"
$wwwSAN = "www.$commonName"

# Build the config file
$configFile = @"
# -------------- BEGIN CONFIG --------------
HOME = .
oid_section = new_oids
[ new_oids ]
[ req ]
default_days = 1095
distinguished_name = req_distinguished_name
encrypt_key = yes
string_mask = nombstr
req_extensions = v3_req # Extensions to add to certificate request
[ req_distinguished_name ]
countryName = Country Name (2 letter code)
countryName_default = $country
stateOrProvinceName = State or Province Name (full name)
stateOrProvinceName_default = $state
localityName = Locality Name (eg, city)
localityName_default = $locality
organizationalUnitName  = Organizational Unit Name (eg, section)
organizationalUnitName_default  = $orgUnit
organizationName = Organization Name (eg, company)
organizationName_default = $org
commonName = Your common name (eg, domain name)
commonName_default = $commonName
emailAddress = Contact email address
emailAddress_default = $email
commonName_max = 64
[ v3_req ]
subjectAltName= @alt_names
[alt_names]
DNS.1 = $wwwSAN
DNS.2 = $commonName
# -------------- END CONFIG --------------
"@

# Write it out to the temp folder
$configFile | Out-File -FilePath $env:TEMP\csrconf.cnf -Force -Encoding ascii

# Change directory
Set-Location -Path $openSSLDir

# Generate the key and csr
Start-Process .\openssl.exe -Argumentlist "genrsa -des3 -passout pass:$password -out C:\Temp\$fileName.pass.key 2048" -Wait
Start-Process .\openssl.exe -Argumentlist "rsa -passin pass:$password -in C:\Temp\$fileName.pass.key -out C:\Temp\$fileName.key" -Wait
Start-Process .\openssl.exe -ArgumentList "req -new -key C:\Temp\$fileName.pass.key -out C:\Temp\$fileName.csr -config $env:TEMP\csrconf.cnf" -Wait
Start-Process .\openssl.exe -ArgumentList "x509 -req -sha256 -days $daysExpired -in C:\Temp\$fileName.csr -signkey C:\Temp\$fileName.key -out C:\Temp\$fileName.crt" -Wait
Start-Process .\openssl.exe -ArgumentList "pkcs12 -export -out C:\Temp\$fileName.p12 -inkey C:\Temp\$fileName.key -in C:\Temp\$fileName.crt" -Wait