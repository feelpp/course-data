.PHONY: setup check site serve clean

setup:
	uv sync --locked --all-groups
	npm ci

check:
	npm run check

site:
	npm run build

serve:
	npm run serve

clean:
	npm run clean

