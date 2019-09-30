# epiroom_lil

## Requirement
- Docker
- docker-compose

## Launch

```bash
docker-compose up -d --build
```

## CronJob

```cron
*/15 * * * *	bash -c "<path to project>/manage.py get_planning"
```
