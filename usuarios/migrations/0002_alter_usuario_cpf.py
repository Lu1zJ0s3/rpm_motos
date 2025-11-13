

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='cpf',
            field=models.CharField(blank=True, max_length=14, null=True, unique=True, verbose_name='CPF'),
        ),
    ]
