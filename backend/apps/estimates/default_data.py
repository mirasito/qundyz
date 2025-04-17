from decimal import Decimal


def populate_default_stages(estimate):
    """
    Создаёт 7 стандартных этапов ремонта с заранее заданными работами и материалами.
    """
    from .models import Stage, Material, Work
    stage_data = [
        {
            "name": "Планирование",
            "materials": [],
            "works": [
                {"name": "Разработка дизайн-проекта", "hours": 20, "cost_per_hour": 8000},
            ],
        },
        {
            "name": "Демонтаж",
            "materials": [
                {"name": "Мешки для мусора", "quantity": 80, "unit": "шт", "price_per_unit": 100},
            ],
            "works": [
                {"name": "Снятие старых покрытий", "hours": 15, "cost_per_hour": 5000},
            ],
        },
        {
            "name": "Черновая отделка",
            "materials": [
                {"name": "Штукатурка", "quantity": 2500, "unit": "кг", "price_per_unit": 80},
                {"name": "Стяжка", "quantity": 8000, "unit": "кг", "price_per_unit": 55},
            ],
            "works": [
                {"name": "Черновая штукатурка", "hours": 25, "cost_per_hour": 4500},
            ],
        },
        {
            "name": "Стяжка",
            "materials": [
                {"name": "Пескобетон", "quantity": 7500, "unit": "кг", "price_per_unit": 50},
            ],
            "works": [
                {"name": "Укладка стяжки", "hours": 30, "cost_per_hour": 5000},
            ],
        },
        {
            "name": "Облицовка",
            "materials": [
                {"name": "Плитка", "quantity": 30, "unit": "м²", "price_per_unit": 4000},
            ],
            "works": [
                {"name": "Облицовка санузла", "hours": 20, "cost_per_hour": 6000},
            ],
        },
        {
            "name": "Чистовая отделка",
            "materials": [
                {"name": "Краска", "quantity": 25, "unit": "л", "price_per_unit": 3000},
                {"name": "Ламинат", "quantity": 50, "unit": "упаковка", "price_per_unit": 6000},
            ],
            "works": [
                {"name": "Окраска стен", "hours": 15, "cost_per_hour": 4000},
                {"name": "Укладка ламината", "hours": 20, "cost_per_hour": 5000},
            ],
        },
        {
            "name": "Мебелировка",
            "materials": [
                {"name": "Кухонный гарнитур", "quantity": 1, "unit": "компл", "price_per_unit": 250000},
            ],
            "works": [
                {"name": "Установка мебели", "hours": 16, "cost_per_hour": 6000},
            ],
        },
    ]

    for idx, stage in enumerate(stage_data, start=1):
        s = Stage.objects.create(
            estimate=estimate,
            name=stage["name"],
            order=idx,
            duration_days=1,
        )
        for m in stage["materials"]:
            Material.objects.create(stage=s, **m)
        for w in stage["works"]:
            Work.objects.create(stage=s, **w)


def generate_default_data_for_stage(stage, area=100, height=2.7):
    from .models import Stage, Material, Work
    
    name = stage.name.lower()
    materials = []
    works = []

    # Пример расчётов
    wall_area = area * height * 2.5
    floor_area = area

    if "планирование" in name:
        works.append(("Разработка дизайн-проекта", 20, 5000))

    elif "демонтаж" in name:
        materials.append(("Мешки для мусора", 80, "шт", 100))
        works.append(("Демонтаж покрытий", 24, 2000))

    elif "черновая отделка" in name:
        materials.append(("Штукатурка", wall_area * 8 / 25, "кг", 70))
        materials.append(("Грунтовка", wall_area / 10, "л", 900))
        works.append(("Штукатурные работы", 40, 2500))

    elif "стяжка" in name:
        materials.append(("Пескобетон", floor_area * 0.075, "мешков", 800))
        works.append(("Устройство стяжки", 16, 3000))

    elif "облицовка" in name:
        materials.append(("Керамическая плитка", 20, "м²", 2500))
        materials.append(("Клей плиточный", 5, "мешков", 2000))
        works.append(("Укладка плитки", 15, 4000))

    elif "чистовая отделка" in name:
        materials.append(("Краска для стен", 15, "л", 3500))
        materials.append(("Обои", 20, "рулонов", 2000))
        materials.append(("Ламинат", area / 2, "упаковок", 7000))
        works.append(("Поклейка обоев", 10, 4000))
        works.append(("Покраска стен", 10, 3500))
        works.append(("Укладка ламината", 15, 4500))

    elif "мебелировка" in name:
        materials.append(("Мебельный гарнитур", 1, "комплект", 300000))
        works.append(("Сборка и расстановка мебели", 16, 2500))

    for mat in materials:
        Material.objects.create(
            stage=stage,
            name=mat[0],
            quantity=mat[1],
            unit=mat[2],
            price_per_unit=Decimal(mat[3])
        )

    for work in works:
        Work.objects.create(
            stage=stage,
            name=work[0],
            hours=work[1],
            cost_per_hour=Decimal(work[2])
        )