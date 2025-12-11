#Introduction


## Database

-   Initialize alembic
```
alembic init migrations
```
-   Run revision migration
```bash
alembic revision --autogenerate -m "Update models"

```
-   Apply changes after reviewing migration file
```py
alembic upgrade head
```