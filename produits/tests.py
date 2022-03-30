from django.test import TestCase
from produits import models


p = models.Provenance()
prix = models.Prix()
produit =models.Produit() 
p.url="fjsqkmfq"
p.save
prix.montant=214
prix.save
produit.reference="lait soja"
produit.reference=p
produit.save
