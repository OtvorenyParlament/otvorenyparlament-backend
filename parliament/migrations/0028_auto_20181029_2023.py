# Generated by Django 2.1.2 on 2018-10-29 19:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parliament', '0027_auto_20181027_1837'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.PositiveIntegerField()),
                ('delivered', models.DateField()),
                ('proposer_nonmember', models.CharField(default='', max_length=255)),
                ('current_state', models.CharField(choices=[('evidence', 'Evidencia'), ('closedtask', 'Uzavretá úloha'), ('reading_1', 'I. čítanie'), ('reading_2', 'II. čítanie'), ('reading_3', 'III. čítanie'), ('redaction', 'Redakcia'), ('committeediscussion', 'Rokovanie výboru'), ('standpoint', 'Stanovisko k NZ'), ('councildiscussion', 'Rokovanie NR SR'), ('coordinatordiscussion', 'Rokovanie gestorského výboru')], max_length=32)),
                ('current_result', models.CharField(choices=[('wontcontinue', 'NR SR nebude pokračovať v rokovaní o návrhu zákona'), ('resolutionwriting', 'Zápis uznesenia NR SR'), ('inredaction', 'NZ postúpil do redakcie'), ('takenback', 'NZ vzal navrhovateľ späť'), ('reading_2', 'NZ postúpil do II. čítania'), ('committeesreport', 'Zápis spoločnej správy výborov'), ('wasnotapproved', 'NZ nebol schválený'), ('infoready', 'Pripravená informácia k NZ'), ('published', 'Zákon vyšiel v Zbierke zákonov'), ('vetopres', 'Zákon bol vrátený prezidentom'), ('comreswriting', 'Zapísané uznesenie výboru')], max_length=32)),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='BillProcessStep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.PositiveIntegerField()),
                ('step_type', models.CharField(choices=[('registry', 'Podateľňa'), ('chairdecision', 'Rozhodnutie predsedu NR SR'), ('reading1', 'I. čítanie'), ('reading2', 'II. čítanie'), ('reading3', 'III. čítanie'), ('coordinatordiscussion', 'Rokovanie gestorského výboru'), ('committeesdiscussion', 'Rokovanie výborov'), ('redaction', 'Redakcia')], max_length=24)),
                ('step_result', models.CharField(choices=[('chairdecision', 'Zapísané rozhodnutie predsedu NR SR'), ('preparinginfo', 'Príprava informácie k NZ'), ('takenback', 'NZ vzal navrhovateľ späť'), ('wontocntinue', 'NR SR nebude pokračovať v rokovaní o návrhu zákona'), ('published', 'Zákon vyšiel v Zbierke zákonov.'), ('toredaction', 'NZ postupuje do redakcie'), ('reading3', 'NZ postúpil do III. čítania'), ('commresolutionwriting', 'Zápis uznesenia / návrhu uznesenia výborov'), ('wasnotapproved', 'NZ nebol schválený'), ('presidentialveto', 'Zákon bol vrátený prezidentom.')], max_length=64)),
                ('meeting_resolution', models.PositiveIntegerField(blank=True, null=True)),
                ('meeting_resolution_date', models.DateField(blank=True, null=True)),
                ('committees_label', models.TextField(default='')),
                ('slk_label', models.TextField(default='')),
                ('coordinator_label', models.TextField(default='')),
                ('coordinator_meeting_date', models.DateField(blank=True, null=True)),
                ('coordinator_name', models.CharField(default='', max_length=255)),
                ('discussed_label', models.CharField(default='', max_length=255)),
                ('sent_standpoint', models.CharField(choices=[('conformable', 'Súhlasný'), ('discordant', 'Nesúhlasný')], max_length=12)),
                ('sent_label', models.DateField(blank=True, null=True)),
                ('act_num_label', models.CharField(max_length=12)),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parliament.Bill')),
                ('meeting_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parliament.Session')),
            ],
        ),
        migrations.AlterField(
            model_name='press',
            name='press_type',
            field=models.CharField(choices=[('other', 'Other type'), ('intag', 'International agreement'), ('petition', 'Petition'), ('information', 'Information'), ('bill', 'Bill'), ('report', 'Report')], db_index=True, max_length=24),
        ),
        migrations.AddField(
            model_name='bill',
            name='press',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parliament.Press'),
        ),
        migrations.AddField(
            model_name='bill',
            name='proposers',
            field=models.ManyToManyField(to='parliament.Member'),
        ),
    ]
