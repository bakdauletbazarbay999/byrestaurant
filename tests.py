from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# Категория блюд (Супы, Салаты, Негізгі т.б.)
class MenuCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Атауы")
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Бөлім"
        verbose_name_plural = "Бөлімдер"

    def __str__(self):
        return self.name

# Блюдо
class Dish(models.Model):
    category = models.ForeignKey(MenuCategory, on_delete=models.SET_NULL, null=True, related_name='dishes', verbose_name="Бөлім")
    name = models.CharField(max_length=200, verbose_name="Атауы")
    description = models.TextField(blank=True, verbose_name="Сипаттамасы")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Бағасы")
    image = models.ImageField(upload_to='dishes/', null=True, blank=True, verbose_name="Сурет")
    is_active = models.BooleanField(default=True, verbose_name="Белсенді")

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюдалар"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('dish_detail', args=[self.id])

# Стол/место (егер бөлмелер/столдар болса)
class Table(models.Model):
    number = models.PositiveIntegerField(unique=True, verbose_name="Стол нөмірі")
    capacity = models.PositiveIntegerField(default=4, verbose_name="Сыйымдылығы")
    description = models.CharField(max_length=200, blank=True, verbose_name="Ескертпе")

    class Meta:
        verbose_name = "Стол"
        verbose_name_plural = "Столдар"

    def __str__(self):
        return f"Стол №{self.number} ({self.capacity})"

# Бронирование столика
class Reservation(models.Model):
    STATUS_CHOICES = [
        ('new', 'Жаңа'),
        ('confirmed', 'Расталды'),
        ('canceled', 'Бас тартылды'),
        ('completed', 'Аяқталды'),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations', verbose_name="Клиент")
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Стол")
    full_name = models.CharField(max_length=200, verbose_name="Толық аты")
    phone = models.CharField(max_length=50, verbose_name="Телефон")
    date = models.DateField(verbose_name="Күні")
    time = models.TimeField(verbose_name="Уақыты")
    guests = models.PositiveIntegerField(default=2, verbose_name="Адам саны")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Бронь"
        verbose_name_plural = "Броньдар"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} — {self.date} {self.time}"



# Заказ арқылы тапсырыс (Order + OrderItem)
class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Жаңа'),
        ('preparing', 'Дайындалып жатыр'),
        ('ready', 'Дайын'),
        ('delivered', 'Жеткізілген'),
        ('canceled', 'Бас тартылды'),
    ]

    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    full_name = models.CharField(max_length=200, verbose_name="Аты")
    phone = models.CharField(max_length=50, verbose_name="Телефон")
    address = models.CharField(max_length=300, blank=True, null=True, verbose_name="Мекен-жай")  # егер жеткізу керек болса
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Тапсырыс"
        verbose_name_plural = "Тапсырыстар"
        ordering = ['-created_at']

    def __str__(self):
        return f"#{self.id} — {self.full_name}"

    def calculate_total(self):
        total = sum([item.subtotal() for item in self.items.all()])
        self.total_cost = total
        self.save()
        return self.total_cost

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2) # 👈 Осы жолды қосыңыз

    def __str__(self):
        return f"{self.dish} x {self.quantity}"

    def subtotal(self):
        if self.dish:
            return self.dish.price * self.quantity
        return 0
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.user.username




from django.db import models

class Car(models.Model):
    model_name = models.CharField(max_length=100)
    year = models.IntegerField()
    engine = models.CharField(max_length=100)
    price = models.IntegerField()
    loan_terms = models.TextField()
    test_drive_available = models.BooleanField(default=True)
    service_info = models.TextField()

    def __str__(self):
        return self.model_name

class Chat(models.Model):
    user_input = models.TextField()
    assistant_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_input[:20]}..."

from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total(self):
        return self.quantity * self.product.price


# calculator/models.py

from django.db import models


# Бұрынғы ChatHistory моделі (өзгеріссіз қалады)
class ChatHistory(models.Model):
    user_query = models.TextField(verbose_name="Клиент сұрағы")
    ai_response = models.TextField(verbose_name="ЖИ жауабы")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Уақыты")

    class Meta:
        verbose_name = "Чат тарихы"
        verbose_name_plural = "Чат тарихы"
        ordering = ['-created_at']

    def __str__(self):
        return f"Сұрақ: {self.user_query[:50]}"


# 🔥 ЖАҢА МОДЕЛЬ: Тазалау нүктесін сақтау үшін 🔥
class ClearPoint(models.Model):
    """
    Басты беттегі чат тарихының соңғы рет қашан тазаланғанын сақтайды.
    """
    last_cleared = models.DateTimeField(auto_now=True, verbose_name="Соңғы тазалау уақыты")

    # Бұл модельдің тек бір жазбасы болуы керек
    def save(self, *args, **kwargs):
        if self._state.adding and ClearPoint.objects.exists():
            # Екінші жазбаны сақтауға тырысса, қате жібереміз немесе өткізіп жібереміз
            return
        super(ClearPoint, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Тазалау нүктесі"
        verbose_name_plural = "Тазалау нүктесі"


# In models.py
class Calculation(models.Model):
    def save(self, *args, **kwargs):
        # Deferred/Local Import
        from .ai_logic import process_calculation
        process_calculation(self) # Call the imported function
        super().save(*args, **kwargs)

