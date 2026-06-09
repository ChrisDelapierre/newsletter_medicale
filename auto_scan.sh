#!/bin/bash

# ==============================================================================
# SCRIPT DE MISE À JOUR ET DE DÉPLOIEMENT AUTOMATIQUE POUR GITHUB PAGES
# ==============================================================================

echo "🔍 Étape 1 : Analyse du dossier et listing des fichiers HTML..."

# On liste tous les fichiers .html en excluant index.html
# On formate le résultat pour le JavaScript (ex: 'page1.html', 'page2.html')
LISTE=$(ls *.html 2>/dev/null | grep -v index.html | sed "s/.*/'&',/" | tr '\n' ' ' | sed 's/,$//')

# Vérification si des fichiers ont été trouvés
if [ -z "$LISTE" ]; then
    echo "⚠️ Aucun autre fichier HTML trouvé à part index.html."
    # On vide le tableau dans le fichier au cas où des fichiers auraient été supprimés
    LISTE=""
else
    echo "✅ Fichiers trouvés : $LISTE"
fi

echo "📝 Étape 2 : Injection de la liste dans index.html..."

# On remplace la ligne du tableau dans index.html par la nouvelle liste mise à jour
sed -i "s/const mesPages = \[.*\];/const mesPages = \[$LISTE\];/" index.html
