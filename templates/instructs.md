Chaque fois que tu génères un rapport de veille médicale au format HTML, tu dois suivre STRICTEMENT les consignes architecturales suivantes. Tu ne dois appliquer AUCUN style CSS en ligne (interdiction d'utiliser l'attribut style="...") et tu ne dois pas insérer de balise <style>. Tout le design repose sur le fichier de style externe.

### 1. Structure Globale de la Page
- La page doit obligatoirement inclure cette liaison CSS dans le <head> : 
  <link rel="stylesheet" href="style.css">
- Tout le contenu de la page doit être enveloppé dans une unique division principale : 
  <div class="container"> ... </div>

### 2. Organisation des Rubriques
- Pour le titre principal de la page, utilise la balise <h1>.
- Pour les titres des rubriques standards (ex: "VIDAL.fr", "ANSM"), utilise la balise <h2>.
- Pour la rubrique des urgences ou actualités critiques, utilise obligatoirement la classe "priority" : 
  <h2 class="priority">🔴 Nouveautés prioritaires</h2>

### 3. Structure d'un Article (Composant Card)
Chaque actualité ou article trouvé doit être structuré exactement selon le modèle suivant :

<div class="article-card">
    <h3>[Titre de l'article]</h3>
    <p class="article-text">[Texte de description ou résumé de l'article]</p>
    <div class="article-meta">
        <span class="badge">[Type d'alerte ou Nom de la source]</span>
        <a href="[URL_DU_LIEN]" class="btn-link">[Texte du bouton, ex: "Lire l'article →"]</a>
    </div>
</div>

*Règle cruciale pour les Priorités :* Si l'article fait partie de la section "Nouveautés prioritaires", ajoute obligatoirement la classe "is-priority" sur l'enveloppe de la carte : 
<div class="article-card is-priority">

### 4. Pied de page
En fin de document, insère le bloc de clôture suivant pour afficher la date et les sources :
<div class="footer">
    <p>Résumé généré automatiquement le [DATE] | Sources : [LISTE_DES_SOURCES]</p>
</div>
