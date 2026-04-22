from django.contrib import admin
# Table және Reservation импорттары жойылды
from .models import MenuCategory, Dish, Order, OrderItem, Profile

@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name',)

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')

# TableAdmin класы толығымен жойылды

# ReservationAdmin класы толығымен жойылды

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','full_name','phone','created_at','status','total_cost')
    inlines = [OrderItemInline]
    list_filter = ('status','created_at')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','phone')




from django.contrib import admin
# 🔥 Models.py файлынан ChatHistory және ClearPoint модельдерін импорттаймыз 🔥
from .models import ChatHistory, ClearPoint


# 1. ChatHistory моделіне арналған әкімші класы
@admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):
    """
    Чат тарихын әкімші панелінде көрсету және басқару.
    is_archived өрісі жоқ болғандықтан, ол бұл жерден алынып тасталды.
    """
    # Тізімде көрсетілетін өрістер
    # is_archived алынып тасталды
    list_display = ('id', 'user_query_snippet', 'ai_response_snippet', 'created_at')

    # Сүзу (фильтрлеу) опциялары
    # is_archived алынып тасталды
    list_filter = ('created_at',)

    # Іздеу өрістері
    search_fields = ('user_query', 'ai_response')

    # Уақыт бойынша навигация
    date_hierarchy = 'created_at'

    # Жазбаларды тек оқуға арналған (өзгертуге тыйым салу)
    # is_archived алынып тасталды
    readonly_fields = ('user_query', 'ai_response', 'created_at')

    # Ұзын мәтіндерді қысқарту үшін функциялар (өзгеріссіз)
    def user_query_snippet(self, obj):
        return obj.user_query[:50] + '...' if len(obj.user_query) > 50 else obj.user_query

    user_query_snippet.short_description = "Клиент сұрағы"

    def ai_response_snippet(self, obj):
        return obj.ai_response[:50] + '...' if len(obj.ai_response) > 50 else obj.ai_response

    ai_response_snippet.short_description = "ЖИ жауабы"


# 2. ClearPoint моделіне арналған әкімші класы (өзгеріссіз)
@admin.register(ClearPoint)
class ClearPointAdmin(admin.ModelAdmin):
    """
    Тазалау нүктесін басқару.
    """
    list_display = ('id', 'last_cleared')
    readonly_fields = ('last_cleared',)

    # Ешкім жаңа жазба қоса алмауы үшін
    def has_add_permission(self, request):
        return False