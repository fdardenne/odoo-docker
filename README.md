This environment allows to launch Odoo instances with Docker easily.

## Disclaimer

This repo is tailored to my need and environment. Scripts are not polished/clean,
is only tested on macOS and may not work on other operating systems.

## Installation

1. Install Docker.
2. Build the image with `docker build -t odoo .`
3. Place your cloned Odoo folder at the root of this directory.
4. (Optional) Place your cloned Odoo Enterprise folder at the root of 
   this directory.
5. You can add your project addons in `project/{project_name}`.

## Run the Auxiliary Services

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

## Run a Container

Use the command:
```bash
odoocker -v {odoo_branch_name} -i {addons_to_install} --code
```
This will run Odoo on the specified branch, install the selected
addons and launch vscode on the instance folder.

`odoocker` also accepts the `--debug` flag to run odoo with debugpy
```bash
odoocker -v {branch_name} --debug --code
```
With this, we can attach to the odoo debugger with vscode 
(Run & Debug in the vscode sidebar -> Attach to Odoo debug container)

## Known Limitations

- Git commands in the Odoo folders are not available inside the
  container, as worktrees are managed from the host.
