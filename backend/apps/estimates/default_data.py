from decimal import Decimal

def populate_default_stages(estimate):
    from .models import Stage, Material, Work
    stages = [
        {
            "name": "Планирование",
            "materials": [
                {"name": "Бумага, распечатки", "quantity": 10, "unit": "листов", "price_per_unit": 50},
                {"name": "ПО для 3D-моделирования", "quantity": 1, "unit": "лицензия", "price_per_unit": 30000},
            ],
            "works": [
                {"name": "Дизайн-проект", "hours": 30, "cost_per_hour": 10000},
                {"name": "Согласование перепланировок", "hours": 8, "cost_per_hour": 6000},
            ],
        },
        {
            "name": "Демонтаж",
            "materials": [
                {"name": "Мешки для мусора", "quantity": 100, "unit": "шт", "price_per_unit": 120},
                {"name": "Пленка защитная", "quantity": 60, "unit": "м²", "price_per_unit": 80},
            ],
            "works": [
                {"name": "Демонтаж покрытий", "hours": 20, "cost_per_hour": 5000},
                {"name": "Вывоз мусора", "hours": 6, "cost_per_hour": 3000},
            ],
        },
        {
            "name": "Перепланировка и инженерия",
            "materials": [
                {"name": "Газоблоки", "quantity": 180, "unit": "шт", "price_per_unit": 450},
                {"name": "Электрокабель", "quantity": 300, "unit": "м", "price_per_unit": 150},
                {"name": "Подрозетники", "quantity": 35, "unit": "шт", "price_per_unit": 80},
                {"name": "Трубы PPR", "quantity": 30, "unit": "м", "price_per_unit": 180},
            ],
            "works": [
                {"name": "Возведение перегородок", "hours": 24, "cost_per_hour": 5500},
                {"name": "Монтаж электропроводки", "hours": 18, "cost_per_hour": 6000},
                {"name": "Установка труб", "hours": 14, "cost_per_hour": 5500},
            ],
        },
        {
            "name": "Черновая отделка",
            "materials": [
                {"name": "Пескобетон", "quantity": 8500, "unit": "кг", "price_per_unit": 50},
                {"name": "Штукатурка", "quantity": 2500, "unit": "кг", "price_per_unit": 70},
                {"name": "Гидроизоляция", "quantity": 20, "unit": "кг", "price_per_unit": 900},
            ],
            "works": [
                {"name": "Стяжка пола", "hours": 28, "cost_per_hour": 6000},
                {"name": "Штукатурные работы", "hours": 32, "cost_per_hour": 5000},
                {"name": "Гидроизоляция", "hours": 10, "cost_per_hour": 4500},
            ],
        },
        {
            "name": "Установка окон и дверей",
            "materials": [
                {"name": "Монтажная пена", "quantity": 10, "unit": "баллон", "price_per_unit": 1200},
                {"name": "Межкомнатные двери", "quantity": 6, "unit": "шт", "price_per_unit": 45000},
            ],
            "works": [
                {"name": "Установка дверей", "hours": 12, "cost_per_hour": 5500},
                {"name": "Монтаж окон", "hours": 10, "cost_per_hour": 6000},
            ],
        },
        {
            "name": "Чистовая отделка",
            "materials": [
                {"name": "Краска", "quantity": 25, "unit": "л", "price_per_unit": 3500},
                {"name": "Обои", "quantity": 20, "unit": "рулонов", "price_per_unit": 2500},
                {"name": "Ламинат", "quantity": 55, "unit": "упаковка", "price_per_unit": 7000},
            ],
            "works": [
                {"name": "Окраска стен", "hours": 16, "cost_per_hour": 5000},
                {"name": "Поклейка обоев", "hours": 10, "cost_per_hour": 4500},
                {"name": "Укладка ламината", "hours": 15, "cost_per_hour": 6000},
            ],
        },
        {
            "name": "Мебелировка и декор",
            "materials": [
                {"name": "Кухонный гарнитур", "quantity": 1, "unit": "компл", "price_per_unit": 300000},
                {"name": "Диван", "quantity": 1, "unit": "шт", "price_per_unit": 200000},
                {"name": "Шторы и декор", "quantity": 5, "unit": "компл", "price_per_unit": 30000},
            ],
            "works": [
                {"name": "Монтаж мебели", "hours": 18, "cost_per_hour": 6000},
                {"name": "Финальная уборка", "hours": 8, "cost_per_hour": 4000},
            ],
        }
    ]
    for idx, stage in enumerate(stages, start=1):
        s = Stage.objects.create(estimate=estimate, name=stage["name"], order=idx, duration_days=1)
        for m in stage["materials"]:
            Material.objects.create(stage=s, **m)
        for w in stage["works"]:
            Work.objects.create(stage=s, **w)