
# MatshidisoBellaBooks
Initial commit

## Adding Django

### Security

`manage.py check --deploy`

## Deployment

- Docker

`docker-compose up -d`

go to `localhost:8003`

## Staging


`mkdir /var/git/ -p`

`git init --bare bellabooks.git`

`git remote add bellabooks ssh://root@178.128.171.157/var/git/bellabooks.git`

`git push --set-upstream bellabooks master`

### Hooks

mkdir /var/www/bellabooks -p

`/var/git/bellabooks.git/hooks`

`cat > post-receive`


```
#!/bin/sh

dest=/var/www/bellabooks
echo "Deploying to $dest"

GIT_WORK_TREE=$dest git checkout --force
cd $dest

docker-compose up -d --force-recreate

```

chmod +x post-receive


