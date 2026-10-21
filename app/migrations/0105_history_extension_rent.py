from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0104_alter_history_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='extension_rent',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Extension Rent'),
        ),
    ]
