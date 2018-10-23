"""
Parliament filters
"""

from django.db.models import Q
from django.utils import timezone
import django_filters

from parliament.models import Member, MemberChange, Period, VotingVote


class MemberFilterSet(django_filters.FilterSet):

    is_active = django_filters.DateFilter(field_name='is_active', method='filter_is_active')

    def filter_is_active(self, queryset, name, value):
        queryset = queryset.filter(
            Q(active__start__lte=value),
            Q(active__end__gt=value) | Q(active__end__isnull=True)
        )
        return queryset


    class Meta:
        model = Member
        fields = {
            'id': ('exact',),
            'stood_for_party': ('exact',),
            'period__period_num': ('exact',),
            'person__id': ('exact',)
        }


class VotingVoteFilterSet(django_filters.FilterSet):

    exclude_for = django_filters.BooleanFilter(
        field_name='exclude_for', method='filter_exclude_for')
    exclude_against = django_filters.BooleanFilter(
        field_name='exclude_against', method='filter_exclude_against')
    exclude_abstain = django_filters.BooleanFilter(
        field_name='exclude_abstain', method='filter_exclude_abstain')
    exclude_dnv = django_filters.BooleanFilter(
        field_name='exclude_dnv', method='filter_exclude_dnv')
    exclude_absent = django_filters.BooleanFilter(
        field_name='exclude_absent', method='filter_exclude_absent')

    def filter_exclude_for(self, queryset, name, value):
        if value is True:
            queryset = queryset.exclude(vote=VotingVote.FOR)
        return queryset

    def filter_exclude_against(self, queryset, name, value):
        if value is True:
            queryset = queryset.exclude(vote=VotingVote.AGAINST)
        return queryset

    def filter_exclude_abstain(self, queryset, name, value):
        if value is True:
            queryset = queryset.exclude(vote=VotingVote.ABSTAIN)
        return queryset

    def filter_exclude_dnv(self, queryset, name, value):
        if value is True:
            queryset = queryset.exclude(vote=VotingVote.DNV)
        return queryset

    def filter_exclude_absent(self, queryset, name, value):
        if value is True:
            queryset = queryset.exclude(vote=VotingVote.ABSENT)
        return queryset

    class Meta:
        model = VotingVote
        fields = {
            'id': ('exact',),
            'voting__voting_num': ('exact',),
            'voting__session__session_num': ('exact',),
            'voting__session__period__period_num': ('exact',),
            'person': ('exact',)
        }

    @property
    def qs(self):
        parent = super().qs
        return parent
