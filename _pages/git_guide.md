---
layout: default
title: GIT Návod
permalink: /git-guide/
---

# GIT návod
## Základy
Vygeneruju si SSH klíč
``` bash
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

```bash
# Spuštění ssh-agenta
eval $(ssh-agent -s)
# Přidání vygenerovaného klíče do ssh-agenta 
ssh-add ~/.ssh/id_rsa
```
Pokud bash furt chce ověření
```bash
chmod 600 C:/Users/josef/.ssh
chmod 700 C:/Users/josef/.ssh
# cesta samozřejmě tam kde je ssh klíč
chmod 600 ~/.ssh/id_rsa # takhle třeba 
chmod 700 ~/.ssh
```
Konfigurace jména a mailu
```bash
git config --global user.name "Tvoje Jméno" 
git config --global user.email "tvuj@email.com"
```
## Přidání aliasů
```bash
nano ~/.bashrc

#tím se otevře bashrc kde můžu editovat 

alias gs='git status'

#pro cestu se můsí takhle

mycd() {
    cd "C:/Users/josef/OneDrive/Vysoka_skola/MAM/Semestralka" "$@"
}
#tohle je super na rychlý přepínání mezi projekty

#aby si nemusel resetovat cmd
source ~/.bashrc

```
## Dobrý commandy
```bash
git reset HEAD <file> # Resetuje změny v konkrétním souboru 
git reset --hard HEAD # Vymaže všechny lokální změny
git reset HEAD~1 # Pokud chceš resetovat pouze poslední commit a zachovat změny, které jsi v něm provedl.
git status
git stash
git stash pop
git fetch
git remote #zobrazí na jaký remote je to napojeno

git branch #vypsání branchů
git branch -d <název_větve> #smaže branch lokálně
git push <jméno originu> --delete <název_větve> #smaže branch v originu

```
https://rtime.felk.cvut.cz/gitweb/hubacji1/oneflow.git/blob/refs/heads/master:/intro.md

## Klonování repozitáře

```bash
git init #inicializace gitu
git clone url #stažení
git remote add <name> <url> #přiřazení remote
git push --set-upstream <name>
```


## Zavádění repozitáře
```bash
cd existing_repo #cd do projektu
git remote add origin https://gitlab.com/monkey265/test.git #origin je jmeno 
git branch -M master
git add . # přidá celý adresář do commitu
git commit -m "init" # inicializační commit
git push -uf origin master

```

## Merge
```bash
git merge --strategy-option ours #přijaty všechny změny přicházející z sloučení
```
# Tipy do práce

```bash
git add -u .
# Přidá vše rozpracované trackované
git pull -- rebase -- autostash
# udělá git stash a git stash pop a mezitím git pull -- rebase

```