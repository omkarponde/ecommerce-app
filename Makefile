up:
	docker-compose -f docker-compose.yml up -d
dev_up:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
dev_logs:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml logs -f --tail 100 ${SERVICE_NAME}
init_db:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec app python -m app.init_db
