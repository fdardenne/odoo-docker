This environment allows to launch Odoo instances with Docker easily.

## Disclaimer

This repo is tailored to my need and environment. Scripts are not polished/clean,
is only tested on macOS and may not work on other operating systems.

## Installation

1. Install Docker.
2. Place your cloned Odoo folder at the root of this directory. This folder must be cloned from
   github.com/odoo/odoo . `odoocker` will use this folder to create a worktree for the needed Odoo
   version.
4. (Optional) Place your cloned Odoo Enterprise folder at the root of this directory.
3. Build the image with `docker build -t odoo .`
5. You can add your project addons in `project/{project_name}`.
6. Make sure the command `code` from vscode is in your path ([Launch vscode from the command line](https://code.visualstudio.com/docs/setup/mac#_launch-vs-code-from-the-command-line))
6. Modify `./odoocker` absolute path to where your folder is.

## Run the Auxiliary Services
- Create the docker network: `docker network create onetwork`
- To launch the database, run:
   ```bash
   docker run --name db --network onetwork -e POSTGRES_PASSWORD=odoo -e POSTGRES_USER=odoo -e POSTGRES_DB=postgres -d postgres
   ```
- To launch Traefik and access the Odoo container at 
  `http://{container_name}.localhost`, run:
   ```bash
   docker run -d \
       --name traefik \
       --network onetwork \
       -p 80:80 -p 8080:8080 \
       -v /var/run/docker.sock:/var/run/docker.sock \
       traefik:v2.11 \
       --api.insecure=true \
       --providers.docker \
       --entrypoints.web.address=:80 \
       --providers.docker.exposedbydefault=false
   ```
- To launch a web service listing the containers, run `./dashboard.py`.

## Run a Container & Odoo

Use the command:
```bash
./odoocker -v {odoo_version} --code
```
This will run Odoo on the specified branch and launch vscode on the instance folder.

`odoocker` also accepts the `--debug` flag to run odoo with debugpy
```bash
./odoocker -v {odoo_version} --debug --code
```
With this, we can attach to the odoo debugger with vscode 
(Run & Debug in the vscode sidebar -> Attach to Odoo debug container)

You can specify a project addons folder, it will be mounted in the container
and run by Odoo. The project is fetched in the `./projects` folder.
```bash
./odoocker -v {odoo_version} -p my_project
```
Here `./projects/my_project` is a folder with addons

## Debug

- When the container is run with `--debug`, the debug mode is activated.
- Open `./instances/{container_name}/src` in vscode (or specify --code in the command)
- Then you can attach the debugger with "Run & Debug" in the vscode sidebar and "Attach to Odoo debug container"
