# Project-Ro-ASD Organization Governance Setup

Bu belge GitHub Organization UI uzerinden bir defa uygulanacak repository governance
ayarlarini tanimlar. Organization administration endpoint'leri mevcut ChatGPT GitHub
baglantisi tarafindan yazilabilir olmadigi icin bu kisim organization owner tarafindan
manuel uygulanir.

## A. Custom property

GitHub:

    Project-Ro-ASD
      -> Settings
      -> Repository / Custom properties

Yeni property:

    Name: roasd_type
    Type: Single select
    Required: tercih edilirse ON
    Default: unclassified

Allowed values:

    unclassified
    application
    kernel
    infrastructure
    distribution
    repository
    template

Ilk atamalar icin `docs/repository-classification-v1-tr.md` kullanilir.

## B. Ro-ASD Common Baseline ruleset

GitHub:

    Project-Ro-ASD
      -> Settings
      -> Repository rulesets
      -> New branch ruleset

Name:

    Ro-ASD Common Baseline

Enforcement:

    Active

Target repositories:

    Tum normal Project-Ro-ASD repository'leri.

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

    COMMON RULESET'E EKLEME.

Neden: CI context isimleri repo tipine gore degisir.

Bypass:

    Normal gelistirme icin bypass tanimlama.

## C. Ro-ASD Application Baseline ruleset

Name:

    Ro-ASD Application Baseline

Enforcement:

    Active

Target repositories:

    Custom property filter:
        roasd_type = application

Target branches:

    Default branch

Required status check hedefi:

    ro-app-gate

NOT: `ro-app-gate` ancak application template/repository'lerinde ayni isimde gercek
CI job'u oldugunda enforce edilmelidir. Template hazir olmadan bu required check'i
aktiflestirmek yeni/current application repolarini kilitleyebilir.

Dolayisiyla uygulama sirasi:

    1. ro-app-template hazirla
    2. application repolarinda ro-app-gate workflow contract'ini uygula
    3. CI'in gercekten context urettigini dogrula
    4. sonra Application Baseline'da required check olarak etkinlestir

## D. Kernel Baseline

v1'de yalniz type sinifi tanimlanir.

    roasd_type = kernel

Kernel-specific CI contract kesinlesmeden required status check eklenmez.
Application Baseline kernel repolarina uygulanmaz.

## E. Organization security baseline

GitHub plan/UI destekliyorsa:

    Project-Ro-ASD
      -> Settings
      -> Advanced Security
      -> Configurations

Configuration name:

    Ro-ASD Security Baseline

Hedefler:

    Secret Protection / secret scanning: ON
    Push protection: ON
    Dependabot alerts: ON
    Dependabot security updates: ON

Mumkunse yeni repository'ler icin default security configuration yap.

Bu konfigurasyonun repo tipinden bagimsiz uygulanmasi hedeflenir.

## F. Existing producer repositories

Mevcut Ro-Repo/ro-Control/ro-Assist/Ro-Theme repository-level ruleset'leri Phase 1
sirasinda repo-specific CI check isimleriyle olusturulmustur. Organization baseline
kurulurken bunlari silme veya gevsetme.

Yeni common ruleset bunlarin uzerine ortak policy katmani olarak gelsin.
Repo-specific CI ruleset'leri migration tamamlanana kadar korunur.

## G. ro-app-template

Yeni repository:

    Project-Ro-ASD/ro-app-template

GitHub repository setting:

    Template repository: ON

Custom property:

    roasd_type = template

Bu repo application kod/release iskeletini tasir; production trust vermez.

## H. Dogrulama

Organization setup tamamlandiktan sonra yeni gecici/gercek bir application repo ile
su davranislar dogrulanir:

1. `roasd_type=application` secildiginde Common + Application ruleset gorunuyor mu?
2. Default branch deletion engelleniyor mu?
3. Force push engelleniyor mu?
4. PR required mi?
5. Security baseline uygulanmis mi?
6. `ro-app-gate` gercek CI context'i olusturduktan sonra required check calisiyor mu?

Kernel testinde:

1. `roasd_type=kernel` Common Baseline aliyor mu?
2. Application Baseline uygulanmiyor mu?
3. `ro-app-gate` kernel repo icin required hale gelmiyor mu?

Bu kontroller gecmeden repository governance v1 CLOSED sayilmaz.
