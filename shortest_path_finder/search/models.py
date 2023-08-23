from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class District(models.Model):
    name = models.CharField(max_length=100)
    parent_districts = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='child_districts')
    
    def __str__(self):
        return self.name

class Distance(models.Model):
    source_district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='source_distances')
    destination_district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='destination_distances')
    distance = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return f'{self.source_district} to {self.destination_district}: {self.distance} km'
    

@receiver(post_save, sender=Distance)
def create_or_update_reverse_distance(sender, instance, created, **kwargs):
    if created:
        reverse_distance, _ = Distance.objects.get_or_create(
            souce_district = instance.destination_district,
            destination_district = instance.source_district,
            defaults={'distance': instance.distance}
        )
    else:
        reverse_distance = Distance.objects.get(
            souce_district = instance.destination_district,
            destination_district = instance.source_district
        )
        reverse_distance.distance = instance.distance
        reverse_distance.save()
