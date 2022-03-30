from djongo import models


class Provenance(models.Model):
    raisonSociale = models.CharField(max_length=100)
    url = models.URLField()
    #image = models.ImageField(upload_to='imgs_provenance')
    email = models.EmailField(max_length=100)
    telephone = models.BigIntegerField


class Categorie(models.Model):
    label = models.CharField(max_length=100)
    description = models.TextField()


class HistAjout(models.Model):
    date = models.DateTimeField(auto_now_add=True)


class Produit(models.Model):
    reference = models.CharField(max_length=30)
    # image = models.ImageField(upload_to='imgs_produits')
    description = models.TextField()
    label = models.CharField(max_length=200)
    unite = models.CharField(max_length=30)
    quantite = models.IntegerField()
    prix = models.DecimalField(max_digits=7,decimal_places=2)
    marque = models.CharField(max_length=200, null=True)
    provenance = models.ForeignKey(Provenance, on_delete=models.CASCADE, null=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.DO_NOTHING, null=True)
    creation = models.ForeignKey('HistAjout', on_delete=models.DO_NOTHING, null=True, related_name='cree_le')
    mise_a_jour = models.ForeignKey(HistAjout, on_delete=models.DO_NOTHING, null=True, related_name='m_a_j_les')
