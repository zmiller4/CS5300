from django.db import migrations, models


THEATER_LAYOUT = {
    'A': 12,
    'B': 14,
    'C': 14,
    'D': 16,
    'E': 16,
    'F': 16,
    'G': 16,
    'H': 16,
}


def populate_seats(apps, schema_editor):
    Seat = apps.get_model('bookings', 'Seat')
    Booking = apps.get_model('bookings', 'Booking')
    # Clear existing bookings and seats
    Booking.objects.all().delete()
    Seat.objects.all().delete()
    # Create the standard theater layout
    for row_letter, seat_count in THEATER_LAYOUT.items():
        for num in range(1, seat_count + 1):
            Seat.objects.create(
                seat_number=f"{row_letter}{num}",
                row=row_letter,
                number=num,
            )


def reverse_populate(apps, schema_editor):
    Seat = apps.get_model('bookings', 'Seat')
    Seat.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0001_initial'),
    ]

    operations = [
        # Add new fields
        migrations.AddField(
            model_name='seat',
            name='row',
            field=models.CharField(default='A', max_length=1),
        ),
        migrations.AddField(
            model_name='seat',
            name='number',
            field=models.PositiveIntegerField(default=1),
        ),
        # Remove is_booked field
        migrations.RemoveField(
            model_name='seat',
            name='is_booked',
        ),
        # Add ordering
        migrations.AlterModelOptions(
            name='seat',
            options={'ordering': ['row', 'number']},
        ),
        # Populate seats
        migrations.RunPython(populate_seats, reverse_populate),
    ]
