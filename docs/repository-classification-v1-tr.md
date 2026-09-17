# Project-Ro-ASD Repository Classification v1

Bu tablo `roasd_type` custom property icin canonical repository siniflandirmasidir.
Kesin olmayan repository'ler `unclassified` birakilir; yanlis bir type-specific
policy uygulamaktansa fail-safe davranmak tercih edilir.

Allowed values:

    unclassified
    application
    component
    kernel
    infrastructure
    distribution
    repository
    template

| Repository | roasd_type | Not |
|---|---|---|
| `.github` | infrastructure | Organization policy/contracts/workflows |
| `Ro-Repo` | repository | Merkezi package repository ve trust zinciri |
| `ro-Control` | application | Ro-ASD uygulamasi / package producer |
| `ro-Assist` | application | Ro-ASD uygulamasi / package producer |
| `Ro-Terminal` | application | Ro-ASD terminal uygulamasi |
| `Ro-Settings` | application | Ro-ASD settings uygulamasi |
| `Ro-Store` | application | Ro-ASD store uygulamasi |
| `Ro-MediaWriter` | application | Ro-ASD media writer uygulamasi |
| `ro-ScreenShot` | application | Ro-ASD screenshot uygulamasi |
| `ro-Installer` | application | Ro-ASD installer uygulamasi |
| `Ro-Theme` | component | Desktop/theme package component |
| `Ro-Theme-Alt` | component | Alternatif theme component |
| `Ro-Printer` | component | Printer/scanner packaging component |
| `Ro-Report` | component | System report component |
| `Ro-Kernel` | kernel | Kernel calismasi |
| `ro-Kernel-S` | kernel | Kernel calismasi |
| `ro-Kernel-H` | kernel | Kernel calismasi |
| `Ro-Kernel-Stable` | kernel | Stable kernel repository |
| `Ro-Kernel-Experimental` | kernel | Experimental kernel repository |
| `Ro-ASD-release` | distribution | Distribution release/compose alani |
| `Ro-image-compose` | distribution | Image compose alani |
| `ro-website` | infrastructure | Project web/infrastructure; package producer degil |
| `Ro-Main` | unclassified | Amaci teyit edilmeden type-specific policy uygulanmasin |
| `ro-app-template` | template | Canonical application repository template |
| `ro-app-smoke-test` | application | Gecici governance/application smoke-test repository |

`component` uygulama olmayan fakat Ro-ASD sisteminin parcasini veya paketini ureten
repository'ler icindir. Component repository'leri Application Baseline'i otomatik
olarak ALMAZ; kendi CI/release contract'lari ayri tanimlanabilir.

Yeni ve henuz sinifi belirlenmemis repository'lerde:

    roasd_type = unclassified

kullanilir. Common Baseline uygulanir; Application/Kernel/Distribution gibi
second-layer policy'ler uygulanmaz.

`roasd_type` sadece governance siniflandirmasidir. Production package publisher
trust'i vermez; resmi producer onboarding ayrica `Ro-Repo/config/producers-v1.yaml`
uzerinden review edilen bir PR ile yapilir.
