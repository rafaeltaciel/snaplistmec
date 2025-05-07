name: Python application

on:
  push:
    branches:
      - "main"
  pull_request:
    branches:
      - "main"

permissions:
  contents: read

jobs:
  build:
    runs-on: macos-latest  # Importante! Mude para macOS!

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python 3.10
      uses: actions/setup-python@v3
      with:
        python-version: "3.10"

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt || true  # Ignora se não tiver
        pip install py2app

    - name: Build macOS app
      run: |
        python setup.py py2app

    - name: Upload build artifact
      uses: actions/upload-artifact@v3
      with:
        name: MeuAppMac
        path: dist/*.app
