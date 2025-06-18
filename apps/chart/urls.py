from django.urls import path
from apps.chart.views import MigrantsByCountry, MigrantsByRegion, MigrationPurposeStats, TransportStats, LongTrips, \
    VeryLongTrips, ChartStatsAPIView

urlpatterns = [
    path('stats/countries/', MigrantsByCountry.as_view()),
    path('stats/regions/', MigrantsByRegion.as_view()),
    path('stats/purposes/', MigrationPurposeStats.as_view()),
    path('stats/transport/', TransportStats.as_view()),
    path('stats/long-trips/', LongTrips.as_view()),
    path('stats/very-long-trips/', VeryLongTrips.as_view()),
    path("charts/<str:stat_name>/", ChartStatsAPIView.as_view(), name="chart-stats"),
]