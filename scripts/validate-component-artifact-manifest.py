#!/usr/bin/env python3
"""Dependency-free validator for the Ro-ASD component artifact contract."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
COMPONENT_NAME = re.compile(r"^[a-z0-9][a-z0-9+.-]*$")
REPOSITORY = re.compile(
    r"^https://github\.com/Project-Ro-ASD/[A-Za-z0-9_.-]+$"
)
TAG = re.compile(r"^v[0-9][0-9A-Za-z.+_-]*$")
RELEASE_URL = re.compile(
    r"^https://github\.com/Project-Ro-ASD/[A-Za-z0-9_.-]+/releases/tag/.+$"
)
RUN_URL = re.compile(
    r"^https://github\.com/Project-Ro-ASD/[A-Za-z0-9_.-]+/actions/runs/[0-9]+$"
)
BUILDER = re.compile(
    r"^registry\.fedoraproject\.org/fedora:44@sha256:[0-9a-f]{64}$"
)
RPM_RELEASE = re.compile(r"^[A-Za-z0-9+_.~]+\.fc44$")

ROOT_KEYS = {"schema_version", "component", "source", "build", "artifacts"}
COMPONENT_KEYS = {"name", "version"}
SOURCE_KEYS = {"repository", "commit", "tag", "release_url"}
BUILD_KEYS = {
    "kind",
    "fedora_release",
    "workflow_run_id",
    "workflow_run_url",
    "builder_image",
}
ARTIFACT_KEYS = {
    "type",
    "filename",
    "name",
    "source_name",
    "epoch",
    "version",
    "release",
    "arch",
    "size",
    "sha256",
}


def exact_keys(value: Any, expected: set[str], path: str, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append(f"{path}: nesne olmalı")
        return
    missing = expected - value.keys()
    extra = value.keys() - expected
    if missing:
        errors.append(f"{path}: eksik alanlar: {', '.join(sorted(missing))}")
    if extra:
        errors.append(f"{path}: bilinmeyen alanlar: {', '.join(sorted(extra))}")


def require_text(value: Any, path: str, errors: list[str]) -> bool:
    if not isinstance(value, str) or not value:
        errors.append(f"{path}: boş olmayan metin olmalı")
        return False
    return True


def validate(data: Any, require_release: bool = False) -> list[str]:
    errors: list[str] = []
    exact_keys(data, ROOT_KEYS, "$", errors)
    if not isinstance(data, dict):
        return errors

    if data.get("schema_version") != "component-artifact-manifest-v1":
        errors.append("$.schema_version: component-artifact-manifest-v1 olmalı")

    component = data.get("component")
    exact_keys(component, COMPONENT_KEYS, "$.component", errors)
    if isinstance(component, dict):
        name = component.get("name")
        if not require_text(name, "$.component.name", errors) or not COMPONENT_NAME.fullmatch(name):
            errors.append("$.component.name: kanonik RPM paket adı olmalı")
        require_text(component.get("version"), "$.component.version", errors)

    source = data.get("source")
    exact_keys(source, SOURCE_KEYS, "$.source", errors)
    if isinstance(source, dict):
        repository = source.get("repository")
        if not isinstance(repository, str) or not REPOSITORY.fullmatch(repository):
            errors.append("$.source.repository: Project-Ro-ASD GitHub repo URL'si olmalı")
        commit = source.get("commit")
        if not isinstance(commit, str) or not HEX40.fullmatch(commit):
            errors.append("$.source.commit: tam 40 karakterli git commit'i olmalı")
        tag = source.get("tag")
        release_url = source.get("release_url")
        if tag is not None and (not isinstance(tag, str) or not TAG.fullmatch(tag)):
            errors.append("$.source.tag: v ile başlayan sürüm etiketi veya null olmalı")
        if release_url is not None and (
            not isinstance(release_url, str) or not RELEASE_URL.fullmatch(release_url)
        ):
            errors.append("$.source.release_url: GitHub Release URL'si veya null olmalı")
        if isinstance(tag, str) and isinstance(component, dict):
            component_version = component.get("version")
            if isinstance(component_version, str) and tag != f"v{component_version}":
                errors.append("$.source.tag: component.version ile aynı sürümü göstermeli")
        if (
            isinstance(repository, str)
            and isinstance(tag, str)
            and isinstance(release_url, str)
            and release_url != f"{repository}/releases/tag/{tag}"
        ):
            errors.append("$.source.release_url: repository ve tag ile birebir uyuşmalı")

    build = data.get("build")
    exact_keys(build, BUILD_KEYS, "$.build", errors)
    if isinstance(build, dict):
        kind = build.get("kind")
        if kind not in {"ci", "release"}:
            errors.append("$.build.kind: ci veya release olmalı")
        if build.get("fedora_release") != 44:
            errors.append("$.build.fedora_release: 44 olmalı")
        run_id = build.get("workflow_run_id")
        if run_id is not None and (
            not isinstance(run_id, str) or not run_id.isdigit()
        ):
            errors.append("$.build.workflow_run_id: sayısal metin veya null olmalı")
        run_url = build.get("workflow_run_url")
        if run_url is not None and (
            not isinstance(run_url, str) or not RUN_URL.fullmatch(run_url)
        ):
            errors.append("$.build.workflow_run_url: GitHub Actions URL'si veya null olmalı")
        if (
            isinstance(source, dict)
            and isinstance(source.get("repository"), str)
            and isinstance(run_id, str)
            and isinstance(run_url, str)
            and run_url != f"{source['repository']}/actions/runs/{run_id}"
        ):
            errors.append("$.build.workflow_run_url: repository ve run ID ile uyuşmalı")
        builder = build.get("builder_image")
        if not isinstance(builder, str) or not BUILDER.fullmatch(builder):
            errors.append("$.build.builder_image: digest ile sabit Fedora 44 imajı olmalı")

        if kind == "release" or require_release:
            if not isinstance(source, dict) or source.get("tag") is None:
                errors.append("$.source.tag: yayın alımı için zorunlu")
            if not isinstance(source, dict) or source.get("release_url") is None:
                errors.append("$.source.release_url: yayın alımı için zorunlu")
            if run_id is None or run_url is None:
                errors.append("$.build: yayın alımı için workflow kimliği ve URL'si zorunlu")
        if kind == "ci" and isinstance(source, dict):
            if source.get("tag") is not None or source.get("release_url") is not None:
                errors.append("$.build.kind: tag/Release içeren manifest release olmalı")

    artifacts = data.get("artifacts")
    if not isinstance(artifacts, list):
        errors.append("$.artifacts: dizi olmalı")
        return errors
    if len(artifacts) < 2:
        errors.append("$.artifacts: en az bir RPM ve eşleşen bir SRPM içermeli")

    binary_keys: set[tuple[str, int, str, str]] = set()
    source_keys: set[tuple[str, int, str, str]] = set()
    filenames: set[str] = set()
    for index, artifact in enumerate(artifacts):
        path = f"$.artifacts[{index}]"
        exact_keys(artifact, ARTIFACT_KEYS, path, errors)
        if not isinstance(artifact, dict):
            continue
        kind = artifact.get("type")
        if kind not in {"rpm", "srpm"}:
            errors.append(f"{path}.type: rpm veya srpm olmalı")
        name = artifact.get("name")
        source_name = artifact.get("source_name")
        version = artifact.get("version")
        release = artifact.get("release")
        arch = artifact.get("arch")
        filename = artifact.get("filename")
        epoch = artifact.get("epoch")
        size = artifact.get("size")
        digest = artifact.get("sha256")

        for key, value in (
            ("name", name),
            ("source_name", source_name),
            ("version", version),
            ("release", release),
        ):
            require_text(value, f"{path}.{key}", errors)
        if not isinstance(epoch, int) or isinstance(epoch, bool) or epoch < 0:
            errors.append(f"{path}.epoch: sıfır veya pozitif tam sayı olmalı")
        if not isinstance(size, int) or isinstance(size, bool) or size < 1:
            errors.append(f"{path}.size: pozitif tam sayı olmalı")
        if not isinstance(digest, str) or not HEX64.fullmatch(digest):
            errors.append(f"{path}.sha256: 64 karakterli küçük harf hex olmalı")
        if not isinstance(release, str) or not RPM_RELEASE.fullmatch(release):
            errors.append(f"{path}.release: .fc44 ile bitmeli")
        if arch not in {"x86_64", "noarch", "src"}:
            errors.append(f"{path}.arch: x86_64, noarch veya src olmalı")
        if kind == "srpm" and arch != "src":
            errors.append(f"{path}.arch: SRPM için src olmalı")
        if kind == "rpm" and arch not in {"x86_64", "noarch"}:
            errors.append(f"{path}.arch: ikili RPM için x86_64 veya noarch olmalı")

        if all(isinstance(value, str) for value in (name, version, release, arch)):
            expected_filename = f"{name}-{version}-{release}.{arch}.rpm"
            if filename != expected_filename:
                errors.append(
                    f"{path}.filename: kanonik ad {expected_filename!r} olmalı"
                )
        if isinstance(filename, str):
            if filename in filenames:
                errors.append(f"{path}.filename: yinelenen dosya adı")
            filenames.add(filename)
        if (
            isinstance(name, str)
            and isinstance(source_name, str)
            and isinstance(epoch, int)
            and isinstance(version, str)
            and isinstance(release, str)
        ):
            key = (source_name, epoch, version, release)
            if kind == "rpm":
                binary_keys.add(key)
            elif kind == "srpm":
                if source_name != name:
                    errors.append(f"{path}.source_name: SRPM için name ile aynı olmalı")
                source_keys.add((name, epoch, version, release))

    if not binary_keys:
        errors.append("$.artifacts: en az bir ikili veya noarch RPM gerekli")
    missing_sources = binary_keys - source_keys
    if missing_sources:
        missing = ", ".join(
            f"{name}-{version}-{release}" for name, _epoch, version, release in sorted(missing_sources)
        )
        errors.append(f"$.artifacts: eşleşen SRPM eksik: {missing}")

    return errors


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_path(path: Path, require_release: bool) -> bool:
    try:
        data = load_json(path)
    except (OSError, json.JSONDecodeError) as error:
        print(f"HATA {path}: {error}", file=sys.stderr)
        return False
    errors = validate(data, require_release=require_release)
    if errors:
        print(f"HATA {path}", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return False
    print(f"OK   {path}")
    return True


def check_fixtures(repo_root: Path) -> bool:
    schema = repo_root / "contracts/component-artifact-manifest-v1.schema.json"
    example = repo_root / "contracts/examples/component-artifact-manifest-v1.valid.json"
    invalid_dir = repo_root / "contracts/fixtures/invalid"
    try:
        load_json(schema)
    except (OSError, json.JSONDecodeError) as error:
        print(f"HATA {schema}: {error}", file=sys.stderr)
        return False

    ok = validate_path(example, require_release=True)
    for fixture in sorted(invalid_dir.glob("*.json")):
        try:
            fixture_errors = validate(load_json(fixture), require_release=True)
        except (OSError, json.JSONDecodeError) as error:
            print(f"HATA {fixture}: {error}", file=sys.stderr)
            ok = False
            continue
        if not fixture_errors:
            print(f"HATA {fixture}: geçersiz fixture kabul edildi", file=sys.stderr)
            ok = False
        else:
            print(f"OK   {fixture} beklenen şekilde reddedildi")
    return ok


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifests", nargs="*", type=Path)
    parser.add_argument(
        "--require-release",
        action="store_true",
        help="Ro-Repo alımı için tag, Release URL'si ve workflow kanıtını zorunlu kıl",
    )
    parser.add_argument(
        "--check-fixtures",
        action="store_true",
        help="Repo içindeki geçerli örneği ve geçersiz fixture'ları denetle",
    )
    args = parser.parse_args()

    if not args.manifests and not args.check_fixtures:
        parser.error("en az bir manifest veya --check-fixtures gerekli")

    repo_root = Path(__file__).resolve().parents[1]
    ok = True
    if args.check_fixtures:
        ok = check_fixtures(repo_root) and ok
    for manifest in args.manifests:
        ok = validate_path(manifest, require_release=args.require_release) and ok
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
