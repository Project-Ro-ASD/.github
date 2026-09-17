# Project-Ro-ASD Organization Governance Setup

Bu belge organization-level canonical policy ile GitHub Free uzerindeki gercek
repository-level enforcement modelini birlikte tanimlar.

## A. Custom property

GitHub:

    Project-Ro-ASD
      -> Settings
      -> Repository / Custom properties

Property:

    Name: roasd_type
    Type: Single select
    Required: ON
    Default: unclassified

Allowed values:

    unclassified
    application
    component
    kernel
    infrastructure
    distribution
    repository
    template

Repository actors property degerini degistiremez. Explicit user-specified value
zorunlulugu kapali tutulur; default `unclassified` fail-safe degeridir.

Canonical atamalar icin `docs/repository-classification-v1-tr.md` kullanilir.

## B. Ro-ASD Common Baseline ruleset

Name:

    Ro-ASD Common Baseline

Enforcement:

    Active

Target repositories:

    Tum Project-Ro-ASD repository'leri

Target branches:

    Default branch

Rules:

    Restrict deletions: ON
    Block force pushes / non-fast-forward: ON
    Require a pull request before merging: ON

Pull request policy (single-maintainer):

    Required approvals: 0
    Dismiss stale approvals: OFF
    Require CODEOWNERS review: OFF
    Require approval of most recent push: OFF

Required status checks:

    Common Baseline'a eklenmez.

Bypass:

    Normal gelistirme icin bypass tanimlanmaz.

Not: Organization-level ruleset canonical policy tanimidir. Mevcut GitHub Free
planinda organization ruleset enforcement'i aktif olmadigi icin public repository'lerde
gercek enforcement repository-level branch protection ile yapilir.

## C. Ro-ASD Application Baseline ruleset

Name:

    Ro-ASD Application Baseline

Enforcement:

    Disabled (migration tamamlanana kadar)

Target repositories:

    Custom property filter:
        roasd_type = application

Target branches:

    Default branch

Required status check hedefi:

    ro-app-gate

Branch up-to-date requirement:

    ON

Bu ruleset existing application repository migration'i tamamlandiktan ve org plan
enforcement desteklediginde Active edilebilir. GitHub Free public application
repository'lerde ayni `ro-app-gate` requirement repository-level protection bootstrap
tarafindan gercekten enforce edilir.

## D. GitHub Free repository-level enforcement

Canonical script:

    scripts/bootstrap-repository-protection.sh Project-Ro-ASD/REPO

Bu script yeni public repository'ler icindir.

Uyguladigi minimum policy:

    PR required: ON
    required approvals: 0
    admins enforced: ON
    force pushes: OFF
    deletion: OFF

`roasd_type=application` ise ek olarak:

    required status: ro-app-gate
    strict/up-to-date: ON

Safety:

- Project-Ro-ASD disindaki repository'leri reddeder,
- archived/private repository'leri reddeder,
- default branch yoksa durur,
- default branch zaten protected ise overwrite etmeyi reddeder.

Bu nedenle existing Phase 1 protected producer repository'lerinde korumayi degistirmek
icin bu script kullanilmaz.

## E. Kernel / Component baseline

Kernel:

    roasd_type = kernel

Component:

    roasd_type = component

v1'de bu iki sinif icin ortak required status check tanimlanmaz. Application Baseline
bu repository'lere uygulanmaz.

## F. Organization security baseline

Public repository'ler icin hedef:

    Secret Protection / secret scanning: ON
    Push protection: ON
    Dependabot alerts: ON
    Dependabot security updates: ON

Code scanning v1 baseline'da zorunlu degildir.

Private repository'lerde GitHub Advanced Security lisansi gerektiren ozellikler
`Not purchased` donerse bunu enforcement basarisi sayma. Free destekli ozellikler
ayrica uygulanir/audit edilir.

## G. Existing producer repositories

Mevcut `Ro-Repo`, `ro-Control`, `ro-Assist`, `Ro-Theme` repository-level ruleset'leri
Phase 1 sirasinda repo-specific CI check isimleriyle olusturulmustur.

Bunlari silme, gevsetme veya bootstrap script ile overwrite etme.
Application migration gerekli oldugunda branch -> PR -> CI -> merge ile yeni
`ro-app-gate` interface'i eklenir; mevcut protection ancak ayrica review edilerek
guncellenir.

## H. ro-app-template

Repository:

    Project-Ro-ASD/ro-app-template

Settings:

    Template repository: ON
    roasd_type = template

Template application CI/release iskeletini tasir; production trust vermez.

Yeni application baslatma akisi:

    Use this template
      -> Project-Ro-ASD organization altinda repo olustur
      -> roasd_type=application
      -> .roasd/app.json placeholder'larini doldur
      -> tools/project-ci gercek build/test/lint hook'u yap
      -> tools/build-rpm gercek Fedora 44 RPM hook'u yap
      -> repository-level protection bootstrap uygula
      -> PR ac
      -> ro-app-gate green olmadan merge etme

Resmi package producer olacaksa ayrica `Ro-Repo/config/producers-v1.yaml` onboarding
PR'i gerekir.

## I. Dogrulama

Application smoke test icin `Project-Ro-ASD/ro-app-smoke-test` kullanildi.
Dogrulanan davranislar:

- template placeholder'lari ile CI fail closed,
- metadata + project CI hook konfigure edilince `ro-app-contract` green,
- `ro-app-project-ci` green,
- `ro-app-gate` green,
- repository-level branch protection uygulandi,
- `main` protected,
- required status context `ro-app-gate`.

Governance v1 CLOSED olmadan once ayrica:

1. existing application repository migration durumu audit edilir,
2. security baseline audit edilir,
3. representative application repo'da direct main push reddi teyit edilir,
4. representative kernel/component repo'da `ro-app-gate` zorunlu olmadigi teyit edilir.
