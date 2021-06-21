rm -rf dist
python3 -m build
twine upload --repository testpypi dist/* --username quakerdocs --password "quakerdocs123!"