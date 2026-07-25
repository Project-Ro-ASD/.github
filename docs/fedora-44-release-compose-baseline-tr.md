# Fedora 44 release ve compose başlangıç planı

Durum: kabul edilen ilk iskelet
Hedef: gereksiz yayın altyapısı veya ISO işi açmadan Ro-ASD 44 için doğrulanabilir
temeli kurmak

## Repo sahipliği

- `.github`: organizasyon çapındaki artifact sözleşmeleri ve geliştirici teslim
  kuralları için kanonik kaynak.
- `Ro-ASD-release`: dağıtım kimliği, repo istemci politikası, marka,
  varsayılanlar, çekirdek politikası ve standart masaüstü meta-paketlerinin RPM
  kaynakları.
- `Ro-image-compose`: Fedora tabanı, profil ve ilerideki image/package/payload
  tanımları.
- `Ro-Repo`: ayrı ekip üyesinin sahip olduğu imzalı yayın, snapshot, testing ve
  stable terfi katmanı.
- `Ro-Main`: bu çalışmanın parçası değildir; tanıtım/ana sayfa rolünde kalır.

## Bu aşamada yapılacaklar

### Ortak sözleşme

- `component-artifact-manifest-v1` şeması
- geçerli yayın örneği ve reddedilmesi gereken fixture'lar
- Fedora 44, tam kaynak commit'i, korunan sürüm etiketi, workflow kanıtı,
  digest ile sabit builder, kanonik RPM adı, SHA-256 ve eşleşen SRPM kuralları
- bileşen sahiplerine gönderilecek Türkçe genel teslim notu

### Ro-ASD-release

- Fedora 44 ve Ro-ASD 44 için tek `VERSION.yaml`
- altı ayrı SRPM ailesinin sorumluluk dizinleri
- yalnızca `ro-asd-release` için çalışan `noarch` metadata RPM'i
- ikili RPM, SRPM, checksum ve geliştirme manifesti üreten Fedora 44 CI
- Fedora kimliği, repo URL'si, anahtar ve çekirdek politikasına erken müdahale
  edilmemesi

### Ro-image-compose

- `release.yaml` ve `Ro-ASD-release/VERSION.yaml` içerik hash'i
- `standard-live`, `qemu-ci`, `hardware-rc` için contract-only profiller
- şema, fixture ve CI doğrulaması
- gerçek ISO/KIWI build'i veya paket listesi olmaması

## Bileşen geçiş sırası

Ortak Fedora 44 teslim standardı bütün depo sahipleriyle paylaşılır. İlk uygulama
önceliği:

1. `ro-Assist`
2. `Ro-Theme`
3. `ro-Installer`

Diğer bileşenlerde bu aşamada zorunlu kod değişikliği yapılmaz. `ro-Control` ve
`Ro-Store` güvenlik engelleri giderilmeden standart profile alınmaz.

## Bilinçli bekleme noktaları

- Ro-Repo V2: kanal yolları, repo ID/base URL, snapshot biçimi, anahtar dosya
  adları, alım ve terfi sözleşmesi
- proje domaininin canlı kullanımı, Cloudflare R2 ve imzalama operasyonu
- Fedora Remix/marka incelemesi
- Fedora 44 kararlı/fallback çekirdek ve Secure Boot kanıtı
- imzalı candidate snapshot oluşmadan ilk gerçek KIWI compose
- gerçek compose snapshot'ından üretilecek merkezi SPDX JSON SBOM

## Sonraki kapı

İlk gerçek görüntü çalışması ancak `repository_snapshot` null olmaktan çıkıp
imzalı ve değişmez bir Fedora 44 candidate kimliğine bağlandığında başlar.
`candidate` veya `release` aşamasında null snapshot sözleşme tarafından
reddedilir.
