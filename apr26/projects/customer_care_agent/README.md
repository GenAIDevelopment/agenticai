## Setting up the customer care database

* Ensure Docker Desktop is installed
    * [Windows](https://docs.docker.com/desktop/setup/install/windows-install/) 
    * [Mac](https://docs.docker.com/desktop/setup/install/mac-install/)
* Now lets start the postgres container with sample schema in it
* Run the container
```bash
docker run --name customer-care-db \
  -e POSTGRES_USER=myuser \
  -e POSTGRES_PASSWORD=mypassword \
  -e POSTGRES_DB=mydb \
  -p 5432:5432 \
  -d postgres:16
```

* Windows
```
docker run --name customer-care-db `
  -e POSTGRES_USER=myuser `
  -e POSTGRES_PASSWORD=mypassword `
  -e POSTGRES_DB=mydb `
  -p 5432:5432 `
  -d postgres:16
```

* To access this db we need db clients like pgadmin etc or we can use a visual studio extension `Postgres`
* To remove the contianer
```
docker rm -f customer-care-db
```