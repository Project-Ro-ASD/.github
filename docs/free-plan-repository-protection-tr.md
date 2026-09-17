# Ro-ASD GitHub Free Repository Protection

Durum: v1

Project-Ro-ASD organization-level ruleset'leri canonical policy olarak tutulur. Ancak
GitHub Free organization planinda organization-wide ruleset enforcement kullanilamadigi
icin public repository'lerde gercek enforcement repository seviyesinde uygulanir.

## Yeni repository akisi

Yeni repository olusturulduktan ve `roasd_type` atandiktan sonra:

```bash
git clone https://github.com/Project-Ro-ASD/.github.git
cd .github
bash scripts/bootstrap-repository-protection.sh Project-Ro-ASD/REPOSITORY
```

Script mevcut `gh` oturumunu kullanir. Token veya credential script'e verilmez.

## Uygulanan Common Baseline

- default branch Pull Request olmadan degistirilemez,
- required approvals = 0 (single-maintainer policy),
- admins icin de protection uygulanir,
- force push kapali,
- branch deletion kapali,
- bypass eklenmez.

## Application ek kurali

Repository custom property degeri:

```text
roasd_type = application
```

ise Common Baseline'a ek olarak:

```text
ro-app-gate
```

required status check olur ve branch'in guncel olmasi (`strict`) gerekir.

Application repository'sinin CI workflow'u `ro-app-gate` context'ini gercekten
uretmeden protection bootstrap calistirilmamalidir. `ro-app-template` bu contract'i
varsayilan olarak tasir.

## Fail-closed davranis

Script:

- Project-Ro-ASD disindaki repository'leri reddeder,
- archived repository'leri reddeder,
- default branch yoksa durur,
- default branch zaten protected ise DURUR ve mevcut policy'yi degistirmez.

Bu nedenle mevcut Phase 1 producer repository'lerinde korumayi otomatik olarak
replace etmek icin kullanilmaz. Existing repository migration ayri PR ve inceleme ile
yapilir.

## Smoke test

`Project-Ro-ASD/ro-app-smoke-test` icin beklenen sonuc:

1. `roasd_type=application`,
2. `ro-app-gate` CI context'i mevcut,
3. bootstrap script uygulanir,
4. GitHub `main isn't protected` uyarisi kaybolur,
5. direct main push reddedilir,
6. PR + basarili `ro-app-gate` ile merge mumkundur.
