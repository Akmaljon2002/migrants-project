import django_filters
from apps.users.choices import UserRoleChoice
from apps.users.models import CustomUser
from django.db.models import Q


class UserFilter(django_filters.FilterSet):
    role = django_filters.ChoiceFilter(
        field_name="role",
        choices=UserRoleChoice.choices
    )
    date = django_filters.CharFilter(method="filter_date")
    search = django_filters.CharFilter(method="filter_search")

    class Meta:
        model = CustomUser
        fields = ["role", "created_at"]

    def filter_date(self, queryset, value):
        """
        - Agar `YYYY-MM-DD` bo‘lsa, to‘liq sanani filtrlash
        - Agar `YYYY-MM` bo‘lsa, faqat yil va oyni filtrlash
        - Agar `YYYY` bo‘lsa, faqat yil bo‘yicha filtrlash
        """
        try:
            if len(value) == 10:
                year, month, day = map(int, value.split("-"))
                return queryset.filter(created_at__year=year, created_at__month=month, created_at__day=day)
            elif len(value) == 7:
                year, month = map(int, value.split("-"))
                return queryset.filter(created_at__year=year, created_at__month=month)
            elif len(value) == 4:
                return queryset.filter(created_at__year=int(value))
        except ValueError:
            return queryset.none()

        return queryset

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(full_name__icontains=value) |
            Q(phone__icontains=value)
        )