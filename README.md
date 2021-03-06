# The Threat Hunting Environment

You are a Threat Hunter. While investigating, did you find yourself with more than 20 tabs opened in your browser, scattered .txt files with data and some terminals showing up in the background?

theTHE centralizes all the information on an investigation in a single project and shares its results with your team (and with nobody else). theTHE caches your API responses, so you don't need to repeat the requests. Don’t share your keys, let the users make calls to the services.

theTHE also contains some command-line tools integrated so you don't have to open a terminal and pipe the results in a .txt file.

Your feedback is welcome.

## Installation

First, clone this repository with:

```bash
git clone https://github.com/ElevenPaths/thethe.git
```

Then, build the images and run the containers

```bash
docker-compose up -d
```

You should see **thethe** in [https://localhost](https://localhost) after a :coffee:

## Default user

By default, there is a single user **admin** with password **admin**

Change the **admin** password as soon as you log into **thethe** the very first time.

---

## API keys

There are not API keys stored by default on the system.

To add an API key, there is an option in the user menu (upper-right corner).

All API keys (**a new API management system is being development**) must be written as CSV values:

```text
service_name_1,api_value_1
service_name_2,api_value_2
...
service_name_n,api_value_n

```

If a service must have more than one API key, secret, etc...

```text
secret,api_value
...
cookie,cookie_value

```

and so on...

---

## Database backups and restoration

Mongodb has a bind volume to ease external storage and backups in a folder **mongodb_data**

In any case, we have provided you with a couple of scripts to backup (a compressed file) and restore data from your mongo container.

Inside **utils** folder:

Make a backup

```bash
backup_thethe_db.sh <mongodb_container_name>
```

Restore from a backup

```bash
restore_thethe_db.sh <mongodb_container_name>
```

---

## Updating

**Make a database backup!** (check the section "Database Backups and Restoration")

```bash
git pull
```

If the source code has been changed all the mounted volumes should reflect such changes. However in certain cases (third party libraries, etc) the images will have to be rebuilt.

Stop the containers:

```bash
docker-compose stop
```

Rebuild images:

```bash
docker-compose build
```

Restart the system

```bash
docker-compose up -d
```

---

## Development environment

If you want to collaborate with the project, a development version is provided:

### Get the repository

```bash
git clone https://github.com/ElevenPaths/thethe.git
```

### Docker (don't forget your :coffee:)

```bash
docker-compose -f docker-compose_dev.yml up -d
```

### Run the frontend

```bash
cd frontend
npm install
npm run serve
```

---

## More info

Website: [https://thethe.e-paths.com](https://thethe.e-paths.com/)

License: [https://raw.githubusercontent.com/ElevenPaths/thethe/master/LICENSE](https://raw.githubusercontent.com/ElevenPaths/thethe/master/LICENSE)
