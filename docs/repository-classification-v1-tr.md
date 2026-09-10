# Project-Ro-ASD Repository Classification v1

Bu tablo `roasd_type` custom property ilk kez uygulanirken kullanilacak baslangic
siniflandirmasidir. Kesin olmayan repository'ler `unclassified` birakilir; yanlis
bir type-specific ruleset uygulamaktansa fail-safe davranmak tercih edilir.

| Repository | roasd_type | Not |
|---|---|---|
| `.github` | infrastructure | Organization policy/contracts/workflows |
| `Ro-Repo` | repository | Merkezi package repository ve trust zinciri |
| `ro-Control` | application | Ro-ASD uygulamasi / package producer |
| `ro-Assist` | application | Ro-ASD uygulamasi / package producer |
| `Ro-Theme` | application | Desktop/theme package producer; application baseline v1 altinda |
| `Ro-Terminal` | application | Ro-ASD terminal uygulamasi |
| `Ro-Settings` | application | Ro-ASD settings uygulamasi |
| `Ro-Store` | application | Ro-ASD store uygulamasi |
| `Ro-MediaWriter` | application | Ro-ASD media writer uygulamasi |
| `ro-ScreenShot` | application | Ro-ASD screenshot uygulamasi |
| `ro-Installer` | application | Ro-ASD installer uygulamasi |
| `Ro-Printer` | application | Ro-ASD printer UI/application; ilk atama oncesi proje amaci teyit edilebilir |
| `Ro-Report` | application | Ro-ASD report uygulamasi; ilk atama oncesi proje amaci teyit edilebilir |
| `Ro-Kernel` | kernel | Kernel calismasi |
| `ro-Kernel-S` | kernel | Kernel calismasi |
| `ro-Kernel-H` | kernel | Kernel calismasi |
| `Ro-Kernel-Stable` | kernel | Stable kernel repository |
| `Ro-Kernel-Experimental` | kernel | Experimental kernel repository |
| `Ro-ASD-release` | distribution | Distribution release/compose alani |
| `Ro-image-compose` | distribution | Image compose alani |
| `ro-website` | infrastructure | Project web/infrastructure; package producer degil |
| `Ro-Main` | unclassified | Amaci teyit edilmeden type-specific ruleset uygulanmasin |
| `Ro-Theme-Alt` | unclassified | Tarihsel/alternatif amaci teyit edilmeden application sayilmasin |

Yeni `ro-app-template` repository'si olusturuldugunda:

    roasd_type = template

atanir.

Yeni ve henuz sinifi belirlenmemis repository'lerde:

    roasd_type = unclassified

kullanilir. Common Baseline uygulanir; Application/Kernel/Distribution gibi
second-layer ruleset'ler uygulanmaz.
