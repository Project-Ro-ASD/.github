# Fedora 44 bileşen çıktısı: geliştirici teslim notu

Bu belge, Ro-ASD bileşen deposu sahiplerinin Fedora 44 için teslim etmesi
gereken asgari yayın çıktısını tanımlar. Amaç yalnızca bir `.rpm` dosyası
üretmek değil; kaynağı, derleme ortamı ve bütünlüğü doğrulanabilen bir yayın
seti oluşturmaktır.

## Mevcut sorun

Depoların yayın biçimleri bugün aynı değil. Bazıları yalnızca ikili RPM
yayımlıyor, bazıları SRPM'i GitHub Release'e eklemiyor, bazıları kanonik RPM
dosya adını değiştiriyor ve bazı iş akışları Fedora 43'e sabitlenmiş durumda.
Ro-Repo bu çıktıları `latest` mantığıyla toplarsa hangi kaynak ve derlemenin
depoya girdiği güvenilir biçimde kanıtlanamaz.

## Genel çözüm

Her bileşen aynı teslim sözleşmesini uygular:

1. Özellik değişikliği pull request üzerinden test edilir ve `main` dalına
   alınır.
2. Korunan bir `vX.Y.Z` etiketi Fedora 44 derlemesini başlatır.
3. Aynı iş akışı ikili/noarch RPM'i ve onu üreten eşleşen SRPM'i oluşturur.
4. GitHub Release aşağıdaki kanonik dosyaları değiştirmeden taşır:
   - `paket-adı-sürüm-release.fc44.mimari.rpm`
   - `paket-adı-sürüm-release.fc44.src.rpm`
   - `SHA256SUMS`
   - `component-artifact-manifest-v1.json`
5. Manifest tam kaynak commit'ini, etiketi, GitHub Release adresini, iş akışı
   kanıtını, digest ile sabit Fedora 44 builder imajını ve her dosyanın NEVRA,
   kaynak paket adı, boyut ve SHA-256 bilgisini içerir. Alt paket üreten
   projelerde ikili RPM'in `source_name` alanı onu üreten SRPM'in paket adına
   işaret eder.

`x86_64` ilk beta için zorunludur. Bileşen gerçekten mimariden bağımsızsa
`noarch` RPM kabul edilir. `aarch64` ek bir çıktı olabilir ancak `x86_64`
tesliminin yerine geçmez.

## Yapılmaması gerekenler

- Yalnızca ikili `.rpm` yayımlamayın; eşleşen `.src.rpm` zorunludur.
- `ro-assist-x86_64.rpm` gibi kısa adlar üretmeyin. `rpmbuild` tarafından
  üretilen kanonik dosya adını koruyun.
- Aynı etiketteki varlıkları `--clobber` ile sessizce değiştirmeyin. Hatalı
  yayın için yeni bir sürüm etiketi çıkarın.
- Fedora 43 ve Fedora 44 çıktılarını aynı dizin veya manifest içinde
  karıştırmayın.
- Geliştirici anahtarlarıyla resmî repo imzası atmayın. Resmî RPM ve repodata
  imzası Ro-Repo yayın katmanında, erişimi kontrollü proje anahtarıyla
  yapılacaktır.
- GitHub Release oluşmasını paketin `stable` kanala kabulü saymayın.

## Ro-Repo'ya geçiş

GitHub Release yalnızca aday girdidir. Otomasyon exact etiket, commit, dosya adı
ve SHA-256 değerlerini taşıyan bir Ro-Repo alım pull request'i açar. İnsan
onayından sonra aynı dosyalar önce `testing` kanalına girer. Test ve bekleme
kapıları geçildiğinde otomasyon `stable` terfi pull request'i açar; insan onayı
olmadan stable terfi yapılmaz ve terfi sırasında paket yeniden derlenmez.

Sözleşmenin kanonik şeması
`contracts/component-artifact-manifest-v1.schema.json`, geçerli örneği ise
`contracts/examples/component-artifact-manifest-v1.valid.json` dosyasındadır.
Ro-Repo alımı manifesti `--require-release` seçeneğiyle doğrulamalıdır.
