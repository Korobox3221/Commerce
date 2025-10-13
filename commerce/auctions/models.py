from django.contrib.auth.models import AbstractUser
from django.db import models

class Category(models.Model):
    categoryName = models.CharField(max_length=50 )

    def __str__(self):
        return f"{self.categoryName}"

class User(AbstractUser):
    pass
class Listings(models.Model):
    name = models.CharField(max_length = 64)
    price = models.FloatField()
    image = models.CharField(max_length = 1000)
    description = models.CharField(max_length = 300)
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, null=True, related_name = 'user')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name = 'category')
    highest_bid = models.FloatField(blank=True, null=True,)

    def __str__(self):
        return f"{self.name}"

class Bids(models.Model):
    bider_Name = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, null=True, related_name = 'bider')
    bid = models.FloatField()
    listing_Name = models.ForeignKey(Listings, on_delete=models.CASCADE, blank=True, null=True, related_name = 'listing_Name')
    def __str__(self):
        return f"Bider : {self.bider_Name} Bid: {self.bid} $ Listing: {self.listing_Name}"

class Watchlist(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, null=True, related_name = 'watchlist_items')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'listing')  # Prevents exact duplicates
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user.username}'s watchlist: {self.listing.name}"

class Comments(models.Model):
    lot = models.ForeignKey(Listings, on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, null=True, related_name = 'commenters')
    comment = models.CharField(max_length = 1000)

    def __str__(self):
        return f'{self.lot}: {self.commenter} commented: {self.comment}'
