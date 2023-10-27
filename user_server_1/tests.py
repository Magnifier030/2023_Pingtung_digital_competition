from django.test import TestCase

# Create your tests here.
import sys
from models import Card
my_model = Card()

total_size = sys.getsizeof(my_model) * Card.objects.count()
print(total_size)