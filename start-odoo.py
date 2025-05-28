#!/usr/bin/env python3
import subprocess
import sys
import os

def drop_database(db_name):
    print(f"Suppression de la base de données '{db_name}'...")
    try:
        subprocess.run(
            ["dropdb", "-h", "db", "-U", "odoo", db_name],
            check=True
        )
        print("Base de données supprimée avec succès.")
    except subprocess.CalledProcessError as e:
        print(f"Échec de la suppression de la base : {e}")
        sys.exit(1)

def main():
    db_name = os.getenv("DB")
    if not db_name:
        print("Erreur : la variable d'environnement DB n'est pas définie.")
        sys.exit(1)

    args = sys.argv[1:]

    # Si "-d" est dans les arguments, supprimer la base
    if "-d" in args:
        drop_database(db_name)

    # Préparation de la commande Odoo
    command = [
        '/home/odoo/src/odoo/odoo-bin',
        '--dev=all',
        '-d', db_name,
        '--addons-path=/home/odoo/src/custom,/home/odoo/src/odoo/addons,/home/odoo/src/enterprise',
        '-i',
    ]

    # Trouver le paramètre d'installation (après -i)
    if "-i" in args:
        i_index = args.index("-i")
        try:
            install_param = args[i_index + 1]
        except IndexError:
            print("Erreur : aucun paramètre spécifié après -i.")
            sys.exit(1)
    else:
        install_param = args[0]  # fallback simple si -i n’est pas présent

    command.append(install_param)

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution d'Odoo : {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
