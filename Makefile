.PHONY: test api-test discover download analytics web compose-up compose-down

test:
	python -m unittest discover -s tests -v

api-test:
	cd services/api && npm test

discover:
	python scripts/discover_tse_catalog.py

download:
	python scripts/download_tse_resources.py

analytics:
	streamlit run apps/analytics/app.py

web:
	cd apps/web && npm run dev

compose-up:
	docker compose up --build

compose-down:
	docker compose down
