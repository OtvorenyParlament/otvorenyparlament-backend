"""
Parliament Models
"""

from datetime import datetime

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from djchoices import DjangoChoices, ChoiceItem


class Period(models.Model):
    period_num = models.PositiveIntegerField(verbose_name=_('Period number'))
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    snap_end = models.BooleanField(default=False)

    class Meta:
        ordering = ('-period_num',)

    def __str__(self):
        return '{}: {} - {}'.format(
            self.period_num, self.start_date, self.end_date or '')


class ClubManaber(models.Manager):

    def get_queryset(self):
        return super().get_queryset().select_related('period')

class Club(models.Model):
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    external_id = models.IntegerField(unique=True, null=True)
    url = models.URLField(null=True)

    objects = ClubManaber()

    class Meta:
        unique_together = (('period', 'name'),)

    def __str__(self):
        return self.name

    @property
    def current_member_count(self):
        today = datetime.utcnow().date()
        return self.members.filter(
            models.Q(start__lte=today),
            models.Q(end__gt=today) | models.Q(end__isnull=True)
        ).count()
        return self.members.count()


class Party(models.Model):
    """
    Parliament Party
    """
    # TODO(Jozef): Parties are duplicated in some periods with different
    # names, also some changed name in time. Improve this model
    name = models.CharField(max_length=255, verbose_name=_('Party'), unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('Parties')


class MemberManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().select_related(
            'person', 'person__residence', 'period', 'stood_for_party'
        ).prefetch_related('active')


class Member(models.Model):
    """
    Member of parliament during election period
    """
    person = models.ForeignKey(
        'person.Person', on_delete=models.CASCADE, related_name='memberships')
    period = models.ForeignKey('Period', on_delete=models.CASCADE)
    stood_for_party = models.ForeignKey('Party', on_delete=models.CASCADE)
    url = models.URLField()

    objects = MemberManager()

    class Meta:
        unique_together = (('person', 'period'),)

    def __str__(self):
        return '{}, {}, {}'.format(self.person, self.stood_for_party, self.period)


class MemberActive(models.Model):
    """
    Member active periods
    """
    member = models.ForeignKey(
        'Member', on_delete=models.CASCADE, related_name='active')
    start = models.DateField()
    end = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = (('member', 'start'),)
        ordering = ('member', 'start',)


class MemberChange(models.Model):
    """
    Membership changes
    """

    MANDATE_NOT_APPLIED = 'mandatenotapplied'
    ACTIVE = 'active'
    SUBSTITUTE_FOLDED = 'substitutefolded'
    SUBSTITUTE_ACTIVE = 'substituteactive'
    SUBSTITUTE_GAINED = 'substitutegained'
    FOLDED = 'folded'
    GAINED = 'gained'

    CHANGE_TYPES = (
        (MANDATE_NOT_APPLIED, "Mandát sa neuplatňuje"),
        (ACTIVE, "Mandát vykonávaný (aktívny poslanec)"),
        (SUBSTITUTE_FOLDED, "Mandát náhradníka zaniknutý"),
        (SUBSTITUTE_ACTIVE, "Mandát náhradníka vykonávaný"),
        (SUBSTITUTE_GAINED, "Mandát náhradníka získaný"),
        (FOLDED, "Mandát zaniknutý"),
        (GAINED, "Mandát nadobudnutý vo voľbách")
    )

    person = models.ForeignKey(
        'person.Person', on_delete=models.CASCADE, related_name='changes')
    period = models.ForeignKey('Period', on_delete=models.CASCADE)
    date = models.DateField()
    change_type = models.CharField(max_length=64, choices=CHANGE_TYPES)
    change_reason = models.TextField()

    class Meta:
        unique_together = (('person', 'period', 'date', 'change_type'),)


class ClubMemberManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().select_related('club', 'member', 'member__person')


class ClubMember(models.Model):

    CHAIRMAN = 'chairman'
    VICECHAIRMAN = 'vice-chairman'
    MEMBER = 'member'
    NONE = ''

    MEMBERSHIPS = (
        (NONE, 'Žiadny'),
        (CHAIRMAN, 'Predsedníčka/predseda'),
        (VICECHAIRMAN, 'Pod-predsedníčka/predseda'),
        (MEMBER, 'Členka/člen')
    )

    club = models.ForeignKey('Club', on_delete=models.CASCADE, related_name='members')
    member = models.ForeignKey('Member', on_delete=models.CASCADE, related_name='club_memberships')
    membership = models.CharField(max_length=24, db_index=True, choices=MEMBERSHIPS, default=NONE)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)
    objects = ClubMemberManager()

    class Meta:
        unique_together = (('club', 'member', 'start'),)
        ordering = ('club', 'member', 'start')

    def __str__(self):
        return '{} - {}'.format(self.club, self.member)

    def end_membership(self):
        """
        Mark current membership as ended
        """
        self.end = timezone.now()
        self.save()
        return True


class Press(models.Model):
    """
    Parliament press
    """
    TYPE_OTHER = 'other'
    TYPE_INT_AGREEMENT = 'intag'
    TYPE_PETITION = 'petition'
    TYPE_INFORMATION = 'information'
    TYPE_BILL = 'bill'
    TYPE_REPORT = 'report'
    TYPES = (
        (TYPE_OTHER, _('Other type')),
        (TYPE_INT_AGREEMENT, _('International agreement')),
        (TYPE_PETITION, _('Petition')),
        (TYPE_INFORMATION, _('Information')),
        (TYPE_BILL, _('Bill')),
        (TYPE_REPORT, _('Report')),
    )
    press_type = models.CharField(max_length=24, choices=TYPES, db_index=True)
    title = models.TextField()
    press_num = models.CharField(max_length=24, db_index=True)
    date = models.DateField(db_index=True)
    period = models.ForeignKey(Period, on_delete=models.CASCADE, related_name='presses')
    url = models.URLField()

    class Meta:
        verbose_name = _('press')
        verbose_name_plural = _('presses')
        unique_together = (('press_num', 'period'),)

    def __str__(self):
        return self.title


class PressAttachment(models.Model):
    title = models.TextField(max_length=512, default='missing title')
    press = models.ForeignKey(Press, on_delete=models.CASCADE, related_name='attachments')
    url = models.URLField()
    file = models.FilePathField(null=True, blank=True)

    def __str__(self):
        return self.title


class Session(models.Model):
    """
    Parliament Sessions
    """
    name = models.CharField(max_length=255)
    external_id = models.PositiveIntegerField(unique=True)
    period = models.ForeignKey('Period', on_delete=models.CASCADE, related_name='sessions')
    session_num = models.PositiveIntegerField(null=True, blank=True)
    url = models.URLField()

    class Meta:
        ordering = ('-period', '-session_num')

    def __str__(self):
        return self.name


class SessionProgram(models.Model):
    """
    Parliament Session Program
    """
    DISCUSSED = 'discussed'
    NOTDISCUSSED = 'notdiscussed'
    MOVED = 'moved'
    WITHDRAWN = 'withdrawn'
    INTERRUPTED = 'interrupted'

    STATES = (
        (DISCUSSED, "Prerokovaný bod programu"),
        (NOTDISCUSSED, "Neprerokovaný bod programu"),
        (MOVED, "Presunutý bod programu"),
        (WITHDRAWN, "Stiahnutý bod programu"),
        (INTERRUPTED, "Prerušené rokovanie o bode programu")
    )

    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='points')
    press = models.ForeignKey(Press, on_delete=models.CASCADE, null=True, blank=True)
    point = models.PositiveIntegerField(null=True, blank=True)
    state = models.CharField(max_length=24, choices=STATES)
    text1 = models.TextField(default='', blank=True)
    text2 = models.TextField(default='', blank=True)
    text3 = models.TextField(default='', blank=True)

    class Meta:
        ordering = ('session', 'point')

    def __str__(self):
        return '{}. {}'.format(self.point, self.text1)


class SessionAttachment(models.Model):
    """
    Parliament Session Attachments
    """
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='attachments')
    title = models.TextField(max_length=512, default='missing title')
    url = models.URLField()

    def __str__(self):
        return '{} {}'.format(self.session, self.title)


class VotingManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().select_related('session', 'press')


class Voting(models.Model):
    PASSED = 'passed'
    DID_NOT_PASS = 'did_not_pass'
    PARLIAMENT_UNABLE = 'parliament_unable'
    RESULTS = (
        (PASSED, 'Návrh prešiel'),
        (DID_NOT_PASS, 'Návrh neprešiel'),
        (PARLIAMENT_UNABLE, 'Parlament nebol uznášaniaschopný')
    )
    external_id = models.PositiveIntegerField(unique=True)
    session = models.ForeignKey(
        Session, on_delete=models.CASCADE, related_name='votings')
    press = models.ForeignKey(
        Press,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='votings')
    voting_num = models.PositiveIntegerField()
    topic = models.TextField()
    timestamp = models.DateTimeField()
    result = models.CharField(max_length=24, choices=RESULTS)
    url = models.URLField()
    objects = VotingManager()

    class Meta:
        ordering = ('-voting_num',)

    # @property
    def chart_series(self):
        display = {
            x[0]: x[1]
            for x in VotingVote._meta.get_field('vote').flatchoices
        }
        sums = self.votes.values('vote').annotate(total=models.Count('vote'))
        series = []
        labels = []
        for dct in sums:
            labels.append(display[dct['vote']])
            series.append(dct['total'])
        return {'series': series, 'labels': labels}


class VotingVoteManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().select_related(
            'person', 'voting', 'voting__session', 'voting__press')


class VotingVote(models.Model):
    FOR = 'Z'
    AGAINST = 'P'
    ABSTAIN = '?'
    DNV = 'N'
    ABSENT = '0'

    OPTIONS = (
        (FOR, 'Za'),
        (AGAINST, 'Proti'),
        (ABSTAIN, 'Zdržal(a) sa'),
        (DNV, 'Nehlasoval(a)'),
        (ABSENT, 'Neprítomná/ý')
        # (FOR, _('for')),
        # (AGAINST, _('against')),
        # (ABSTAIN, _('abstained')),
        # (DNV, _('did not vote')),
        # (ABSENT, _('absent'))
    )

    voting = models.ForeignKey(
        Voting, on_delete=models.CASCADE, related_name='votes')
    person = models.ForeignKey(
        'person.Person',
        on_delete=models.CASCADE,
        related_name='votes',
        null=True,
        blank=True)
    vote = models.CharField(max_length=4, choices=OPTIONS)
    objects = VotingVoteManager()

    class Meta:
        ordering = ('-voting__session__session_num', '-voting__voting_num',)
        unique_together = (('voting', 'person'),)

    def __str__(self):
        return '{} {} {}'.format(self.voting, self.person, self.vote)


class Bill(models.Model):

    class Category(DjangoChoices):
        act_amendment = ChoiceItem(0, "Novela zákona")
        bill = ChoiceItem(1, "Návrh nového zákona")
        other = ChoiceItem(2, "Iný typ")
        petition = ChoiceItem(3, "Petícia")
        international_treaty = ChoiceItem(4, "Medzinárodná zmluva")
        report = ChoiceItem(5, "Správa")
        constitutional_law = ChoiceItem(6, "Ústavný zákon")
        information = ChoiceItem(7, "Informácia")
        budget_law = ChoiceItem(8, "Návrh zákona o štátnom rozpočte")
        presidential_veto = ChoiceItem(9, "Zákon vrátený prezidentom")

    class State(DjangoChoices):
        evidence = ChoiceItem(0, "Evidencia")
        closed_task = ChoiceItem(1, "Uzavretá úloha")
        reading_1 = ChoiceItem(2, "I. čítanie")
        reading_2 = ChoiceItem(3, "II. čítanie")
        reading_3 = ChoiceItem(4, "III. čítanie")
        redaction = ChoiceItem(5, "Redakcia")
        committee_discussion = ChoiceItem(6, "Rokovanie výboru")
        standpoint = ChoiceItem(7, "Stanovisko k NZ")
        council_discussion = ChoiceItem(8, "Rokovanie NR SR")
        coordinator_discussion = ChoiceItem(9, "Rokovanie gestorského výboru")
        advisor_selection = ChoiceItem(10, "Výber poradcov k NZ")

    class Result(DjangoChoices):
        wont_continue = ChoiceItem(0, "NR SR nebude pokračovať v rokovaní o návrhu zákona")
        taken_back = ChoiceItem(1, "NZ vzal navrhovateľ späť")
        resolution_writing = ChoiceItem(2, "Zápis uznesenia NR SR")
        in_redaction = ChoiceItem(3, "NZ postúpil do redakcie")
        committees_report = ChoiceItem(4, "Zápis spoločnej správy výborov")
        wasnot_approved = ChoiceItem(5, "NZ nebol schválený")
        info_ready = ChoiceItem(6, "Pripravená informácia k NZ")
        published = ChoiceItem(7, "Zákon vyšiel v Zbierke zákonov")
        presidential_veto = ChoiceItem(8, "Zákon bol vrátený prezidentom")
        committee_resolution_writing = ChoiceItem(9, "Zapísané uznesenie výboru")
        legal_selection = ChoiceItem(10, "Výber právneho poradcu")
        reading_2 = ChoiceItem(11, "NZ postúpil do II. čítania")

    external_id = models.PositiveIntegerField(unique=True)
    category = models.SmallIntegerField(choices=Category.choices)
    press = models.ForeignKey(Press, on_delete=models.CASCADE)
    delivered = models.DateField()
    proposer_nonmember = models.CharField(max_length=255, default='')
    proposers = models.ManyToManyField(Member)
    state = models.SmallIntegerField(choices=State.choices, null=True, blank=True)
    result = models.SmallIntegerField(choices=Result.choices, null=True, blank=True)
    url = models.URLField()


class BillProcessStep(models.Model):
    # TODO: Add more types

    class StepTypes(DjangoChoices):
        registry = ChoiceItem(0, "Podateľňa")
        chair_decision = ChoiceItem(1, "Rozhodnutie predsedu NR SR")
        reading_1 = ChoiceItem(2, "I. čítanie")
        reading_2 = ChoiceItem(3, "II. čítanie")
        reading_3 = ChoiceItem(4, "III. čítanie")
        coordinator_discussion = ChoiceItem(5, "Rokovanie gestorského výboru")
        committees_discussion = ChoiceItem(6, "Rokovanie výborov")
        redaction = ChoiceItem(7, "Redakcia")

    class ResultTypes(DjangoChoices):
        chair_decision = ChoiceItem(0, "Zapísané rozhodnutie predsedu NR SR")
        preparing_info = ChoiceItem(1, "Príprava informácie k NZ")
        taken_back = ChoiceItem(2, "NZ vzal navrhovateľ späť")
        wont_continue = ChoiceItem(3, "NR SR nebude pokračovať v rokovaní o návrhu zákona")
        published = ChoiceItem(4, "Zákon vyšiel v Zbierke zákonov.")
        to_redaction = ChoiceItem(5, "NZ postupuje do redakcie")
        reading_1 = ChoiceItem(6, "NZ postúpil do I. čítania")
        reading_2 = ChoiceItem(7, "NZ postúpil do II. čítania")
        reading_3 = ChoiceItem(8, "NZ postúpil do III. čítania")
        committee_resolution_writing = ChoiceItem(9, "Zápis uznesenia / návrhu uznesenia výborov")
        wasnot_approved = ChoiceItem(10, "NZ nebol schválený")
        presidential_veto = ChoiceItem(11, "Zákon bol vrátený prezidentom.")

    STANDPOINT_DISCORDANT = 0
    STANDPOINT_CONFORMABLE = 1

    STANDPOINTS = (
        (STANDPOINT_CONFORMABLE, 'Súhlasný'),
        (STANDPOINT_DISCORDANT, 'Nesúhlasný')
    )
    external_id = models.PositiveIntegerField(unique=True)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    step_type = models.SmallIntegerField(choices=StepTypes.choices) # body label
    step_result = models.SmallIntegerField(choices=ResultTypes.choices)
    meeting_session = models.ForeignKey('Session', on_delete=models.CASCADE)
    meeting_resolution = models.PositiveIntegerField(null=True, blank=True)
    meeting_resolution_date = models.DateField(null=True, blank=True)
    committees_label = models.TextField(default='')
    slk_label = models.TextField(default='')
    coordinator_label = models.TextField(default='')
    coordinator_meeting_date = models.DateField(blank=True, null=True)
    coordinator_name = models.CharField(max_length=255, default='')
    discussed_label = models.CharField(max_length=255, default='')
    sent_standpoint = models.SmallIntegerField(choices=STANDPOINTS)
    sent_label = models.DateField(null=True, blank=True)
    act_num_label = models.CharField(max_length=12)

# class BillAmendment(models.Model):
#     bill_step = models.ForeignKey(BillProcessStep, on_delete=models.CASCADE)
#     date = models.DateField()
#     author = models.ForeignKey(Member, on_delete=models.CASCADE)


# class BillProcessStepAttachment(models.Model):

#     bill_process = models.ForeignKey(BillProcessStep, on_delete=models.CASCADE)
#     title = models.TextField(max_length=512, default='missing title')
#     url = models.URLField()
#     file = models.FilePathField(null=True, blank=True)
