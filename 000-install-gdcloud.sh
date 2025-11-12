
mv ~/Downloads/gdcloud_cli.tar.gz .
tar -xf gdcloud_cli.tar.gz

echo 'export PATH=$PATH:~/GDC-SANDBOX-WORKSHOP/google-distributed-cloud-hosted-cli/bin' >> ~/.bashrc
source ~/.bashrc

gdcloud config set core/organization_console_url https://console.org-1.zone1.google.gdch.test
gdcloud components install gdcloud-k8s-auth-plugin
gdcloud components install storage-cli-dependencies

echo -n | openssl s_client -showcerts -connect console.org-1.zone1.google.gdch.test:443 | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' > org-1-web-tls-ca.cert

curl -k https://console.org-1.zone1.google.gdch.test/.well-known/login-config | grep certificateAuthorityData | head -1 | cut -d : -f 2 | awk '{print $1}' | sed 's/"//g' | base64 --decode > trusted_certs.crt