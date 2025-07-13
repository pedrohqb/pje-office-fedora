Name:           pje-office
Version:        2.5.16u
Release:        1%{?dist}
Summary:        PJeOffice é um software disponibilizado pelo CNJ para assinatura eletrônica de documentos no sistema PJe
License:        Custom
URL:            https://pjeoffice.trf3.jus.br
Source0:        https://pje-office.trf3.jus.br/pro/pjeoffice-pro-v%{version}-linux_x64.zip
BuildArch:      x86_64
BuildRequires:  unzip
BuildRequires:  desktop-file-utils
Requires:       bash, zulu-11

%description
PJeOffice é um software disponibilizado pelo CNJ (Conselho Nacional de Justiça)
para assinatura eletrônica de documentos dentro do sistema PJe (Processo Judicial Eletrônico).
Ele fornece as ferramentas necessárias para gestão de certificados digitais e
assinatura de documentos para processos judiciais no Brasil.

%prep
mkdir -p %{_builddir}/pje-office-%{version}
unzip %{SOURCE0} -d %{_builddir}/pje-office-%{version}

# Navega para o diretório fonte extraído.
cd %{_builddir}/pje-office-%{version}/pjeoffice-pro

# Remove o JRE empacotado, pois o pacote agora dependerá de um Java fornecido pelo sistema.
rm -rf jre

# Remove arquivos de controle de versão e documentação indesejada. O ffmpeg.exe será mantido.
rm -f .gitignore LEIA-ME.TXT

%build
# Altera para o diretório onde os arquivos fonte e scripts gerados estão localizados.
cd %{_builddir}/pje-office-%{version}/pjeoffice-pro

# Cria o script de inicialização principal para o PJeOffice.
cat > pjeoffice-pro.sh << EOF
#!/bin/bash
# Script de inicialização do PJeOffice

echo "Iniciando o PJeOffice!"

# Executa o JAR do PJeOffice usando o Zulu.
export PATH="/usr/lib/jvm/zulu-11/bin"
exec java \
-XX:+UseG1GC \
-XX:MinHeapFreeRatio=3 \
-XX:MaxHeapFreeRatio=3 \
-Xms20m \
-Xmx2048m \
-Dpjeoffice_home="/usr/share/pjeoffice-pro/" \
-Dffmpeg_home="/usr/share/pjeoffice-pro/" \
-Dpjeoffice_looksandfeels="Metal" \
-Dcutplayer4j_looksandfeels="Nimbus" \
-jar \
/usr/share/pjeoffice-pro/pjeoffice-pro.jar
EOF

# Cria o arquivo .desktop para integração com o ambiente de área de trabalho.
cat > pje-office.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=PJeOffice
GenericName=PJeOffice
Exec=/usr/bin/pjeoffice-pro
Type=Application
Terminal=false
Categories=Office;
Comment=PJeOffice
Icon=pjeoffice
EOF

# Extrai o ícone da aplicação do arquivo JAR principal.
unzip -p pjeoffice-pro.jar images/pje-icon-pje-feather.png > pjeoffice.png

%install
# Cria os diretórios de instalação de destino na raiz da construção (build root).
mkdir -p %{buildroot}/usr/share/pjeoffice-pro/
mkdir -p %{buildroot}/usr/share/applications/
mkdir -p %{buildroot}/usr/bin/
mkdir -p %{buildroot}/usr/share/icons/

# Altera para o diretório de construção contendo arquivos preparados e gerados.
cd %{_builddir}/pje-office-%{version}/pjeoffice-pro

# Copia todos os arquivos da aplicação (excluindo o JRE, que foi removido em %prep).
cp -a . %{buildroot}/usr/share/pjeoffice-pro/

# Define as permissões de execução para o ffmpeg.exe.
chmod +x %{buildroot}/usr/share/pjeoffice-pro/ffmpeg.exe

# Remove cópias temporárias de arquivos que serão colocados em locais de sistema.
rm -f %{buildroot}/usr/share/pjeoffice-pro/pje-office.desktop
rm -f %{buildroot}/usr/share/pjeoffice-pro/pjeoffice.png

# Copia o arquivo .desktop para o diretório padrão de aplicações.
cp pje-office.desktop %{buildroot}/usr/share/applications/pje-office.desktop
# Copia o script de inicialização para o diretório principal da aplicação.
cp pjeoffice-pro.sh %{buildroot}/usr/share/pjeoffice-pro/pjeoffice-pro.sh

# Copia o ícone para o diretório padrão de ícones.
cp pjeoffice.png %{buildroot}/usr/share/icons/pjeoffice.png

# Torna o script de inicialização executável.
chmod 755 %{buildroot}/usr/share/pjeoffice-pro/pjeoffice-pro.sh

# Cria um link simbólico para o executável em /usr/bin/.
ln -sf /usr/share/pjeoffice-pro/pjeoffice-pro.sh %{buildroot}/usr/bin/pjeoffice-pro

%files
# Nenhum arquivo de licença ou documentação é empacotado.

# Arquivos principais da aplicação.
/usr/share/pjeoffice-pro/

# Arquivos de integração com o ambiente de área de trabalho.
/usr/share/applications/pje-office.desktop
/usr/bin/pjeoffice-pro

# Ícone da aplicação.
/usr/share/icons/pjeoffice.png
