import re
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app import create_app


def get_app_endpoints():
    app = create_app()
    with app.app_context():
        return {rule.endpoint for rule in app.url_map.iter_rules()}


def find_template_endpoints(templates_dir: Path):
    pattern = re.compile(r"url_for\(\s*['\"]([^'\"]+)['\"]")
    usage = {}

    for html_file in templates_dir.rglob("*.html"):
        text = html_file.read_text(encoding="utf-8")
        matches = pattern.findall(text)
        if matches:
            usage[html_file] = matches

    return usage


def main():
    project_root = Path(__file__).resolve().parents[1]
    templates_dir = project_root / "app" / "templates"

    print(f"\nScanning templates in: {templates_dir}\n")

    app_endpoints = get_app_endpoints()
    template_usage = find_template_endpoints(templates_dir)

    print("=== APP ENDPOINTS ===")
    for ep in sorted(app_endpoints):
        print(" ", ep)

    print("\n=== TEMPLATE ENDPOINT USAGE ===")
    unknown = {}

    for html_file, endpoints in sorted(template_usage.items()):
        print(f"\nFile: {html_file.relative_to(project_root)}")
        seen = set()
        for ep in endpoints:
            if ep in seen:
                continue
            seen.add(ep)
            if ep in app_endpoints:
                print(f"  {ep}  [OK]")
            else:
                print(f"  {ep}  [MISSING]")
                unknown.setdefault(ep, []).append(html_file)

    print("\n=== MISSING ENDPOINTS ===")
    if not unknown:
        print("None.")
    else:
        for ep, files in unknown.items():
            print(f"\n{ep}:")
            for f in files:
                print(" ", f.relative_to(project_root))


if __name__ == "__main__":
    main()
