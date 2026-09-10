# Ro-ASD Repository Governance v1

Durum: ACTIVE DESIGN
Tarih: 2026-09-10

Bu belge Project-Ro-ASD organization icindeki repository yonetim mimarisini tanimlar.
Amac, yeni repository'lerde guvenlik ve branch ayarlarini tekrar tekrar elle kurma
zorunlulugunu azaltmak, ancak application, kernel, distribution ve diger farkli
repository siniflarini tek kaliba zorlamamaktir.

## 1. Mimari ayrim

Ro-ASD repository platformu iki ayri katmandan olusur:

1. Repository governance
   - repository nasil yonetilir?
   - hangi ruleset uygulanir?
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
    kernel
    infrastructure
    distribution
    repository
    template

Yeni repository icin varsayilan deger tercihen `unclassified` olur.

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
organization ruleset sadece `ro-app-gate` ismine baglanir.

## 5. Kernel Baseline

Hedef kosul:

    roasd_type = kernel

Kernel repository'leri Application Baseline'i ALMAZ.
Common Baseline'i alir.

Kernel-specific required checks ancak gercek kernel CI contract'i olusturuldugunda
ayri bir Kernel Baseline icinde tanimlanir. Baslangicta application workflow'lari
kernel repository'lerine uygulanmaz.

Gelecekte gerekirse `ro-kernel-template` olusturulur; bu v1 icin zorunlu degildir.

## 6. Diger repository tipleri

- `distribution`: ISO/image/compose/release dagitim altyapisi.
- `infrastructure`: organization, automation, deployment ve operasyon altyapisi.
- `repository`: Ro-Repo gibi package repository / trust / publication sistemi.
- `template`: yeni repository olusturmak icin kullanilan template repository'leri.
- `unclassified`: henuz sinifi secilmemis repository. Common Baseline uygulanir,
  type-specific ruleset uygulanmaz.

## 7. Template ve policy ayrimi

Template repository dosya ve workflow iskeletini tasir.
Organization ruleset policy tasir.
Custom property hangi policy'nin hangi repository'ye uygulanacagini belirler.

Application ornegi:

    ro-app-template
          -> ro-Music
          -> roasd_type=application
          -> Common Baseline + Application Baseline

Kernel ornegi:

    new repository
          -> ro-Kernel
          -> roasd_type=kernel
          -> Common Baseline + Kernel Baseline

Kernel repository'sinde `ro-app-template` kullanilmaz.

## 8. Release trust ayrimi

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

## 9. Application template v1 hedefi

`Project-Ro-ASD/ro-app-template` ayri bir GitHub Template Repository olacaktir.
Minimum iskelet:

    .github/workflows/ci.yml
    .github/workflows/release.yml
    .github/dependabot.yml
    packaging/
    src/
    tests/
    docs/
    .gitignore
    LICENSE
    README.md

Template producer V2 release contract'ina uygun olacak sekilde tasarlanir, fakat
yeni repository producer registry'ye otomatik olarak trusted eklenmez.

## 10. Single-maintainer policy

Bugun:

- required approvals = 0,
- dismiss stale approvals = off,
- CODEOWNERS review requirement = off.

Ikinci guvenilir maintainer geldiginde hedef:

- required approvals = 1,
- dismiss stale approvals = on,
- CODEOWNERS review requirement = on,
- mumkun oldugunca self-review engeli.

## 11. Guvenlik sinirlari

Yapilmayacaklar:

- roasd_type ile production trust vermek,
- tum repo tiplerine ayni required CI check'i zorlamak,
- primary production secret'i GitHub'a koymak,
- producer repository'lerine production signing secret vermek,
- type-specific ruleset ile Common Baseline'i gevsetmek,
- direct main'i normal gelistirme modeli yapmak.

## 12. v1 uygulama sirasi

1. Organization `roasd_type` custom property olustur.
2. Existing repository'leri siniflandir.
3. `Ro-ASD Common Baseline` organization ruleset olustur.
4. `Ro-ASD Security Baseline` organization security configuration olustur/uygula.
5. `Ro-ASD Application Baseline` ruleset olustur (`roasd_type=application`).
6. `Project-Ro-ASD/ro-app-template` repository'sini olustur ve template olarak isaretle.
7. Template'e common application CI/release contract'i ekle.
8. Yeni application repository'lerinde `roasd_type=application` sec.
9. Resmi paket olacagi zaman Ro-Repo producer onboarding yap.

Bu v1 mimaride repository governance ve release trust bilerek ayri tutulur.
