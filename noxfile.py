"""Development automation
"""
import glob
import os

import nox

PACKAGE_NAME = "stmaterial"
nox.options.sessions = ["lint", "test"]
KWARGS = dict(level1=None, level2=9, level3=5)


#
# Helpers
#
def _versions_bump_helper(version_number, max_version=None):
    if not (max_version) or int(version_number) <= max_version:
        return 0, int(version_number)
    else:
        return 1, 0


def _determine_versions(current_version, **kwargs):
    """Returns (version_in_release, version_after_release)"""
    version_in_release = current_version.rsplit(".dev", 1)[0]
    version_split = version_in_release.split(".")

    plus, version_after_release = 1, []
    for idx, vs in enumerate(version_split[::-1]):
        vs = int(vs) + plus
        max_version = kwargs[f"level{len(version_split)-idx}"]
        plus, version_number = _versions_bump_helper(vs, max_version)
        version_after_release.insert(0, str(version_number))

    return (
        version_in_release,
        ".".join(version_after_release) + ".dev",
    )


# fmt: off
assert (
    _determine_versions("0.9.1.dev", **KWARGS)
    == ("0.9.1", "0.9.2.dev")
), "bump 1"
assert (
    _determine_versions("0.9.5.dev", **KWARGS)
    == ("0.9.5", "1.0.0.dev")
), "bump 2"
assert (
    _determine_versions("0.1.5.dev", **KWARGS)
    == ("0.1.5", "0.2.0.dev")
), "bump 3"
assert (
    _determine_versions("0.1.1.dev", **KWARGS)
    == ("0.1.1", "0.1.2.dev")
), "bump 4"
assert (
    _determine_versions("1.1.1.dev", **KWARGS)
    == ("1.1.1", "1.1.2.dev")
), "bump 5"
assert (
    _determine_versions("1.9.1.dev", **KWARGS)
    == ("1.9.1", "1.9.2.dev")
), "bump 6"
assert (
    _determine_versions("1.9.5.dev", **KWARGS)
    == ("1.9.5", "2.0.0.dev")
), "bump 7"
# fmt: on


def get_release_versions(version_file):
    marker = "__version__ = "

    with open(version_file) as f:
        for line in f:
            if line.startswith(marker):
                current_version = line[len(marker) + 1 : -2]
                break
        else:
            raise RuntimeError("Could not find current version.")

    return _determine_versions(current_version, **KWARGS)


#
# Development Sessions
#
@nox.session(reuse_venv=True)
def docs(session):
    session.install("-r", "docs/requirements.txt")
    session.install(".")

    # Generate documentation into `build/docs`
    session.run("sphinx-build", "-b", "dirhtml", "-v", "docs/", "build/docs")


@nox.session(name="docs-live", reuse_venv=True)
def docs_live(session):
    session.install("-r", "docs/requirements.txt")
    session.install("-e", ".", "sphinx-theme-builder[cli]")

    # Generate documentation into `build/docs`
    session.run("stb", "serve", "docs/", *session.posargs)


@nox.session(name="docs-deploy", reuse_venv=True)
def docs_deploy(session):
    session.install("-r", "docs/requirements.txt")
    session.install(".")

    # Generate documentation into `build/docs`
    session.run("make", "build", external=True)


@nox.session(reuse_venv=True)
def lint(session):
    session.install("pre-commit")

    args = list(session.posargs)
    args.append("--all-files")
    if "CI" in os.environ:
        args.append("--show-diff-on-failure")

    session.run("pre-commit", "run", *args)


@nox.session
def test(session):
    session.install("-e", ".[test]")

    args = session.posargs or ["-n", "auto", "--cov", PACKAGE_NAME]
    session.run("pytest", *args)


@nox.session
def release(session):
    version_file = f"src/{PACKAGE_NAME}/__init__.py"
    allowed_upstreams = [f"git@github.com:zclab/{PACKAGE_NAME.replace('_', '-')}.git"]

    release_version, next_version = get_release_versions(version_file)

    session.install(
        "keyring",
        "release-helper",
        "sphinx-theme-builder[cli]",
        "twine",
    )

    # Sanity Checks
    session.run("release-helper", "version-check-validity", release_version)
    session.run("release-helper", "version-check-validity", next_version)
    session.run("release-helper", "directory-check-empty", "dist")

    session.run("release-helper", "git-check-branch", "main")
    session.run("release-helper", "git-check-clean")
    session.run("release-helper", "git-check-tag", release_version, "--does-not-exist")
    session.run("release-helper", "git-check-remote", "origin", *allowed_upstreams)

    # Prepare release commit
    session.run("release-helper", "version-bump", version_file, release_version)
    session.run("git", "add", version_file, external=True)

    session.run(
        "git", "commit", "-m", f"Prepare release: {release_version}", external=True
    )

    # Build the package
    session.run("stb", "package")
    session.run("twine", "check", *glob.glob("dist/*"))

    # Tag the commit
    session.run(
        # fmt: off
        "git", "tag", release_version, "-m", f"Release {release_version}", "-s",
        external=True,
        # fmt: on
    )

    # Prepare back-to-development commit
    session.run("release-helper", "version-bump", version_file, next_version)
    session.run("git", "add", version_file, external=True)
    session.run("git", "commit", "-m", "Back to development", external=True)

    # Push the commits and tag.
    session.run("git", "push", "origin", "main", release_version, external=True)

    # Upload the distributions.
    session.run("twine", "upload", *glob.glob("dist/*"))
