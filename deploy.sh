#!/usr/bin/env bash

[ -z "$ANSIBLE_VAULT_PASSWORD_FILE" ] && echo "error: environment variable 'ANSIBLE_VAULT_PASSWORD_FILE' required but not set." && return 1
[ -z "$SSL_CERT_FILE" ] && echo "error: environment variable 'SSL_CERT_FILE' required but not set." && return 1

export ANSIBLE_CONFIG="$(pwd)/.ansible/ansible.cfg"

ansible-galaxy install \
    -r .ansible/roles/requirements.yaml \
    -p .ansible/roles \
    --force

ansible-playbook .ansible/deploy.yaml \
    -i .ansible/inventories/production \
    --extra-vars 'repository=drone-discord version=production'
