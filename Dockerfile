FROM python:3.12
WORKDIR /home/odoo

COPY ./odoo/requirements.txt /home/odoo/requirements.txt
COPY ./.odoorc /root/.odoorc
COPY ./start-odoo.py /usr/local/bin/odoo
RUN chmod +x /usr/local/bin/odoo
COPY ./.vscode /home/odoo/.vscode

RUN apt-get update && apt-get install -y libsasl2-dev libldap2-dev libssl-dev libpq-dev gcc build-essential postgresql-client curl
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
RUN apt-get install -y nodejs
RUN pip3 install -r /home/odoo/requirements.txt
RUN rm -rf /home/odoo/requirements.txt

VOLUME "/home/odoo/src"
