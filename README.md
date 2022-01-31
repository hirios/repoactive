# repoactive
Search the last commit in forks 


**NOTE:** code is very slow as it works synchronously<br>
**OBS:** código é muito lento já que ele funciona de maneira síncrona

## Exemplo
``` Python
from repoactive import RepoActive


url = 'https://github.com/Anorov/cloudflare-scrape'
repo = RepoActive()
lista = repo.search(url)
print(lista)
```
