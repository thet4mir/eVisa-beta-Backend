from django.db import migrations


def create_sample_faq_items(apps, schema_editor):
    Faq = apps.get_model('faq', 'Faq')

    items = [
        {
            "title": "Do I need an e-Visa if I am on a cruise ship?",
            "body": "Anim pariatur cliche reprehenderit, enim eiusmod high life accusamus terry richardson ad squid. Nihil anim keffiyeh helvetica, craft beer labore wes anderson cred nesciunt sapiente ea proident.",
        },
        {
            "title": "My child is included in my passport.Do I need to make a separate e-Visa application for her/him?",
            "body": "Anim pariatur cliche reprehenderit, enim eiusmod high life accusamus terry richardson ad squid. Nihil anim keffiyeh helvetica, craft beer labore wes anderson cred nesciunt sapiente ea proident.",
        },
        {
            "title": "What are the criteria for the validity of my supporting document (visa or residence permit from Schengen or from US, UK and Ireland)?",
            "body": "Anim pariatur cliche reprehenderit, enim eiusmod high life accusamus terry richardson ad squid. Nihil anim keffiyeh helvetica, craft beer labore wes anderson cred nesciunt sapiente ea proident.",
        },
        {
            "title": "Can the citiziens of all the countries eligible for e-Visa obtain a visa an arrival?",
            "body": "Anim pariatur cliche reprehenderit, enim eiusmod high life accusamus terry richardson ad squid. Nihil anim keffiyeh helvetica, craft beer labore wes anderson cred nesciunt sapiente ea proident.",
        },
        {
            "title": "How much is an e-Visa fee?",
            "body": "Anim pariatur cliche reprehenderit, enim eiusmod high life accusamus terry richardson ad squid. Nihil anim keffiyeh helvetica, craft beer labore wes anderson cred nesciunt sapiente ea proident.",
        },
        {
            "title": "How long will my e-Visa be valid for?",
            "body": "Anim pariatur cliche reprehenderit, enim eiusmod high life accusamus terry richardson ad squid. Nihil anim keffiyeh helvetica, craft beer labore wes anderson cred nesciunt sapiente ea proident.",
        },
        {
            "title": "Do I have to obtain a visa if I do not leave the international transit area?",
            "body": "Anim pariatur cliche reprehenderit, enim eiusmod high life accusamus terry richardson ad squid. Nihil anim keffiyeh helvetica, craft beer labore wes anderson cred nesciunt sapiente ea proident.",
        },
        {
            "title": "For how many people can i create a family application?",
            "body": "Anim pariatur cliche reprehenderit, enim eiusmod high life accusamus terry richardson ad squid. Nihil anim keffiyeh helvetica, craft beer labore wes anderson cred nesciunt sapiente ea proident.",
        },
        {
            "title": "Are there any criteria for family applications?",
            "body": "Anim pariatur cliche reprehenderit, enim eiusmod high life accusamus terry richardson ad squid. Nihil anim keffiyeh helvetica, craft beer labore wes anderson cred nesciunt sapiente ea proident.",
        },
        {
            "title": "How does a family application work?",
            "body": "Anim pariatur cliche reprehenderit, enim eiusmod high life accusamus terry richardson ad squid. Nihil anim keffiyeh helvetica, craft beer labore wes anderson cred nesciunt sapiente ea proident.",
        },
        {
            "title": "For how many people can i create a group application?",
            "body": "Anim pariatur cliche reprehenderit, enim eiusmod high life accusamus terry richardson ad squid. Nihil anim keffiyeh helvetica, craft beer labore wes anderson cred nesciunt sapiente ea proident.",
        }
    ]

    for sort_order, item in enumerate(items):
        Faq.objects.create(
            question=item['title'],
            answer=item['body'],
            is_active=True,
            sort_order=sort_order,
        )


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_sample_faq_items),
    ]
