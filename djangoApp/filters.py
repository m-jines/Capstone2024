import django_filters
from django_filters import DateFilter, CharFilter, NumberFilter
from .models import *

class TrainingLogFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="Date_Added", lookup_expr='gte')
    end_date = DateFilter(field_name="Date_Added", lookup_expr='lte')
    Notes = CharFilter(field_name='Notes', lookup_expr='icontains')
    Techniques = CharFilter(field_name='Techniques', lookup_expr='icontains')
    Training_Date =  DateFilter(field_name='Training_Date', lookup_expr='exact')
    Duration_min = NumberFilter(field_name="Duration", lookup_expr='gte', label='Min Duration')
    Duration_max = NumberFilter(field_name="Duration", lookup_expr='lte', label='Max Duration')

    class Meta:
        model=TrainingLogEntry
        fields = ['Training_Date','Techniques','Notes']

class TechniqueLibraryFilter(django_filters.FilterSet):
    Technique_Name = CharFilter(field_name='Technique_Name', lookup_expr='icontains')
    Description = CharFilter(field_name='Description', lookup_expr='icontains')
    Status = CharFilter(field_name='Status', lookup_expr='icontains')

    class Meta:
        model=TechniqueLibraryEntry
        fields = ['Technique_Name', 'Description', 'Status']

class TechniqueSeriesFilter(django_filters.FilterSet):
    SeriesName = CharFilter(field_name='SeriesName', lookup_expr='icontains', label='Series Name')
    Description = CharFilter(field_name='Description', lookup_expr='icontains', label='Description')
    # Placeholder for technique-based filtering, actual method to be defined below
    Techniques = CharFilter(method='filter_by_technique', label='Techniques')

    class Meta:
        model = TechniqueSeriesEntry
        fields = ['SeriesName', 'Description']

    def filter_by_technique(self, queryset, name, value):
        """
        This method will filter the TechniqueSeriesEntry queryset based on technique name.
        """
        if value:
            return queryset.filter(
                techniqueserieslinking__TechniqueLibraryEntry__Technique_Name__icontains=value
            ).distinct()
        return queryset
