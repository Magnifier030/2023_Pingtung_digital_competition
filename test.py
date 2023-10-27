import sys
from user_server_1.models import Card
my_model = Card()

total_size = sys.getsizeof(my_model) * Card.objects.count()
print(total_size)