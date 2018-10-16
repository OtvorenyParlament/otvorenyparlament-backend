# Generated by Django 2.1.2 on 2018-10-16 18:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parliament', '0018_auto_20181016_2047'),
    ]

    operations = [
        migrations.RunSQL(sql="""
        CREATE UNIQUE INDEX session_program_unique_1 ON parliament_sessionprogram (session_id, text1, text2, text3, point, press_id);
        """,
        reverse_sql="""DROP INDEX session_program_unique_1"""),
        migrations.RunSQL(
            sql="""
            CREATE UNIQUE INDEX session_program_unique_2 ON parliament_sessionprogram (session_id, text1, text2, text3, point)
            WHERE press_id IS NULL;
            """,
            reverse_sql="""DROP INDEX session_program_unique_2"""
        ),
        migrations.RunSQL(
            sql="""
            CREATE UNIQUE INDEX session_program_unique_3 ON parliament_sessionprogram (session_id, text1, text2, text3, press_id)
            WHERE point IS NULL;
            """,
            reverse_sql="""DROP INDEX session_program_unique_3"""
        ),
        migrations.RunSQL(
            sql="""
            CREATE UNIQUE INDEX session_program_unique_4 ON parliament_sessionprogram (session_id, text1, text2, text3)
            WHERE press_id IS NULL AND point IS NULL;
            """,
            reverse_sql="""DROP INDEX session_program_unique_4"""
        )
    ]
