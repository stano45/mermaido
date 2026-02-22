import subprocess
import sys

import mermaido


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "install":
        print("Installing mermaid-cli and Chromium (this may take a minute)...")
        mermaido.install()
        return

    mermaido._require_mmdc()
    sys.exit(subprocess.call(
        [str(mermaido._MMDC), "-p", str(mermaido._PUPPETEER_CFG), *sys.argv[1:]],
    ))


if __name__ == "__main__":
    main()
