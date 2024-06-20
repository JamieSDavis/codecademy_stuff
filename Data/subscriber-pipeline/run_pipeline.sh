#!/bin/bash

# Caminho para o script Python
PYTHON_SCRIPT="/home/jampamatos/workspace/codecademy/Data/subscriber-pipeline/main.py"

# Caminho para a pasta de produção
PROD_DIR="/home/jampamatos/workspace/codecademy/Data/subscriber-pipeline/prod"

# Caminho para o changelog
CHANGELOG="/home/jampamatos/workspace/codecademy/Data/subscriber-pipeline/logs/changelog.txt"

# Versão atual do changelog
CURRENT_VERSION=$(grep -oP 'Version: \K.*' $CHANGELOG | tail -1)

# Executar o script Python
python3 $PYTHON_SCRIPT

# Verificar se a execução foi bem-sucedida
if [ $? -eq 0 ]; then
    echo "Pipeline executed successfully."

    # Nova versão do changelog
    NEW_VERSION=$(grep -oP 'Version: \K.*' $CHANGELOG | tail -1)

    # Verificar se houve uma atualização no changelog
    if [ "$CURRENT_VERSION" != "$NEW_VERSION" ]; then
        echo "Update detected. Moving files to production."

        # Mover arquivos atualizados para a pasta de produção
        mv /home/jampamatos/workspace/codecademy/Data/subscriber-pipeline/final_output.csv $PROD_DIR/
        mv /home/jampamatos/workspace/codecademy/Data/subscriber-pipeline/dev/clean_cademycode.db $PROD_DIR/

        echo "Files moved to production."
    else
        echo "No updates detected. No files moved to production."
    fi
else
    echo "Pipeline execution failed. Check logs for details."
fi
