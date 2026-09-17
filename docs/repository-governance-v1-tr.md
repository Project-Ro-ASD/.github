# Ro-ASD Repository Governance v1

Durum: ACTIVE IMPLEMENTATION
Tarih: 2026-09-17

Bu belge Project-Ro-ASD organization icindeki repository yonetim mimarisini tanimlar.
Amac, yeni repository'lerde guvenlik ve branch ayarlarini tekrar tekrar elle kurma
zorunlulugunu azaltmak, ancak application, component, kernel, distribution ve diger
repository siniflarini tek kaliba zorlamamaktir.

## 1. Mimari ayrim

Ro-ASD repository platformu iki ayri katmandan olusur:

1. Repository governance
   - repository nasil yonetilir?
   - hangi ruleset/policy uygulanir?
   - hangi security baseline uygulanir?
   - hangi template kullanilir?

2. Release trust
   - repository resmi paket producer'i mi?
   - hangi package adlarini uretebilir?
   - hangi release workflow'u trusted'dir?
   - artifact/provenance acceptance nasil yapilir?
   - signing ve promotion nasil yapilir?

`roasd_type` release trust VERMEZ. Sadece repository siniflandirmasidir.

## 2. Custom property: roasd_type

Organization custom property:

    roasd_type

Tip:

    single select

Degerler:

    unclassified
    application
    component
    kernel
    infrastructure
    distribution
    repository
    template

Yeni repository icin varsayilan deger `unclassified` olur.

## 3. Common Baseline

Hedef:

    normal Project-Ro-ASD repository'lerinin tamaminda ortak yonetim tabani

Minimum kurallar:

- default branch korunur,
- Pull Request zorunludur,
- branch deletion engellenir,
- non-fast-forward / force push engellenir,
- single-maintainer gercegi nedeniyle required approvals = 0,
- CODEOWNERS review requirement = off,
- stale approval dismissal = off.

Common security baseline hedefi:

- Secret Protection / secret scanning = on,
- push protection = on,
- Dependabot alerts = on,
- Dependabot security updates = on.

Repository-specific CI job adlari Common Baseline'a eklenmez.

### GitHub Free enforcement modeli

Organization-level ruleset canonical policy tanimidir. Mevcut GitHub Free planda
organization ruleset enforcement'i kullanilamadigi icin public repository'lerde
gercek enforcement repository-level branch protection ile yapilir.

Canonical bootstrap:

    scripts/bootstrap-repository-protection.sh Project-Ro-ASD/REPO

Script:

- organization disindaki repository'leri reddeder,
- archived/private repository'leri reddeder,
- mevcut protection'i overwrite etmez,
- PR required uygular,
- force push ve deletion'i engeller,
- admin bypass'i kapatir,
- `roasd_type=application` ise `ro-app-gate` required check'ini ekler.

Existing Phase 1 protected repository'lerde bu script zorla kullanilmaz.

## 4. Application Baseline

Hedef kosul:

    roasd_type = application

Application repository'leri Common Baseline'i de alir.

Application-specific hedefler:

- ortak application CI contract,
- canonical final required check: `ro-app-gate`,
- package/release workflow iskeleti icin `ro-app-template`,
- producer oldugunda immutable release ve Producer V2 contract.

`ro-app-gate` uygulamanin kendi test/build job'larinin ardindan calisan tek stabil
status-check interface'idir. Icerideki job adlari repository'ye gore degisebilir;
policy yalnizca `ro-app-gate` ismine baglanir.

Organization Application Baseline ruleset canonical olarak tanimlidir ancak existing
application repository migration'i tamamlanana kadar Disabled tutulur. Public new
application repository'lerde gerekli gate repository-level protection bootstrap ile
gercekten enforce edilir.

## 5. Component Baseline

Hedef kosul:

    roasd_type = component

Component; tema, printer support, system reporting gibi uygulama olmayan fakat
Ro-ASD sisteminin paketlenmis bir parcasini tasiyan repository sinifidir.

Component repository'leri Application Baseline'i ALMAZ. Ortak bir component CI
contract'i tanimlanana kadar Common Baseline disinda component-specific required
status check zorlanmaz.

## 6. Kernel Baseline

Hedef kosul:

    roasd_type = kernel

Kernel repository'leri Application Baseline'i ALMAZ.
Common Baseline'i alir.

Kernel-specific required checks ancak gercek kernel CI contract'i olusturuldugunda
ayri bir Kernel Baseline icinde tanimlanir. Baslangicta application workflow'lari
kernel repository'lerine uygulanmaz.

Gelecekte gerekirse `ro-kernel-template` olusturulur; bu v1 icin zorunlu degildir.

## 7. Diger repository tipleri

- `distribution`: ISO/image/compose/release dagitim altyapisi.
- `infrastructure`: organization, automation, deployment ve operasyon altyapisi.
- `repository`: Ro-Repo gibi package repository / trust / publication sistemi.
- `template`: yeni repository olusturmak icin kullanilan template repository'leri.
- `unclassified`: henuz sinifi secilmemis repository. Common Baseline uygulanir,
  type-specific policy uygulanmaz.

## 8. Template ve policy ayrimi

Template repository dosya ve workflow iskeletini tasir.
Organization ruleset canonical policy tanimidir.
Repository-level protection GitHub Free icin real enforcement katmanidir.
Custom property hangi policy'nin hangi repository'ye uygulanacagini belirler.

Application ornegi:

    ro-app-template
          -> ro-Music
          -> roasd_type=application
          -> project-specific metadata + CI hook
          -> repo-level protection bootstrap
          -> required ro-app-gate

Kernel repository'sinde `ro-app-template` kullanilmaz.

## 9. Release trust ayrimi

Bir repository'nin:

    roasd_type=application

olmasi onu trusted package producer yapmaz.

Resmi producer onboarding Ro-Repo'daki version-controlled registry ile yapilir:

    Ro-Repo/config/producers-v1.yaml

Producer kaydi en az su kimligi baglar:

- exact repository,
- allowed package names,
- Fedora release,
- architectures,
- risk class,
- required tests,
- trusted release workflow.

Producer onboarding branch -> PR -> CI -> merge ile yapilir.

Sonraki release akisi hedefi:

    application PR
      -> main
      -> exact vX.Y.Z tag
      -> trusted release workflow
      -> RPM/SRPM + SHA256SUMS + manifest + provenance
      -> Ro-Repo acceptance
      -> central signing
      -> immutable snapshot
      -> beta
      -> validation/dwell
      -> stable

Production signing private key material producer repository'lerine verilmez.

## 10. Application template v1

`Project-Ro-ASD/ro-app-template` GitHub Template Repository'dir.

Template su kontrati tasir:

- `.roasd/app.json` application metadata,
- `.github/workflows/ci.yml`,
- stable `ro-app-gate`,
- `.github/workflows/release.yml`,
- `tools/project-ci`,
- `tools/build-rpm`,
- Dependabot configuration.

Template repository self-check yapabilir. Template'ten tureyen gercek application
repository, metadata placeholder'lari ve project-specific CI/build hook'lari
konfigure edilmeden fail closed davranir.

Template producer V2 release contract'ina uyumlu iskelet tasir; yeni repository
producer registry'ye otomatik olarak trusted eklenmez.

## 11. Single-maintainer policy

Bugun:

- required approvals = 0,
- dismiss stale approvals = off,
- CODEOWNERS review requirement = off.

Ikinci guvenilir maintainer geldiginde hedef:

- required approvals = 1,
- dismiss stale approvals = on,
- CODEOWNERS review requirement = on,
- mumkun oldugunca self-review engeli.

## 12. Guvenlik sinirlari

Yapilmayacaklar:

- roasd_type ile production trust vermek,
- tum repo tiplerine ayni required CI check'i zorlamak,
- primary production secret'i GitHub'a koymak,
- producer repository'lerine production signing secret vermek,
- type-specific policy ile Common Baseline'i gevsetmek,
- direct main'i normal gelistirme modeli yapmak,
- existing protection'i bootstrap script ile overwrite etmek.

## 13. v1 uygulama durumu

Tamamlananlar:

1. Organization `roasd_type` custom property olusturuldu.
2. Existing repository'ler siniflandirildi.
3. `Ro-ASD Common Baseline` organization ruleset canonical policy olarak olusturuldu.
4. Organization security baseline public repository'ler icin kuruldu.
5. `Ro-ASD Application Baseline` ruleset canonical policy olarak olusturuldu ve
   migration tamamlanana kadar Disabled tutuluyor.
6. `Project-Ro-ASD/ro-app-template` olusturuldu ve template olarak isaretlendi.
7. Application CI/release contract'i template'e eklendi.
8. `Project-Ro-ASD/ro-app-smoke-test` ile fail-closed ve green `ro-app-gate` akisi
   dogrulandi.
9. GitHub Free repository-level protection bootstrap smoke repo'da uygulandi.

Kalan governance v1 isi:

1. existing application repository'leri kontrollu olarak `ro-app-gate` contract'ina migrate et,
2. security/protection final audit yap,
3. governance v1 kapanis kriterlerini dogrula.

Bu v1 mimaride repository governance ve release trust bilerek ayri tutulur.
