# Generated by Django 2.1.2 on 2018-11-01 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parliament', '0032_auto_20181031_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='press',
            name='press_type',
            field=models.SmallIntegerField(choices=[(0, 'Novela zákona'), (1, 'Návrh nového zákona'), (2, 'Iný typ'), (3, 'Petícia'), (4, 'Medzinárodná zmluva'), (5, 'Správa'), (6, 'Ústavný zákon'), (7, 'Informácia'), (8, 'Návrh zákona o štátnom rozpočte'), (9, 'Zákon vrátený prezidentom')], db_index=True),
        ),
    ]
