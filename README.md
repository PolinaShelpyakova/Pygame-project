Автор проекта: Шельпякова Полина

Идея проекта:
Игра - тип приключение, вид сбоку, квест

Описание:
Задача проходить препятствия, взаимодействуя с предметами (ключи, ящики и т.д.)
В течение игры появиться способность уничтожать монстров, которые будут мешать Вам
в прохождении игры. Каждый уровень проработан логически, например, чтобы пройти
препятствие Вам понадобиться проделать ряд действий (подвинуть ящик, нажать кнопку и т.д.)
Герой идёт по платформе.

В уровне:
1. Ящик - его можно двигать героем, запрыгивать на него, используя как платформу.
Также ящиком можно зажать кнопку.
2. Лестница - чтобы героем взобраться или спуститься на какую-либо платформу.
3. Ключ - он просто исчезает и сверху помечается, что у игрока есть ключ,
им можно открыть либо дверь, либо сундук.
4. Магия - эта способность появляется в течение игры, при получении способности,
Вы может уничтожать монстров. (магия - ближний, дальний бой)
5. Бонусы: + урон, + жизни, лечение, восстановление маны, + маны
6. Монеты (очки)
7. Шипы, газ, кислоты, лава, лезвия (причиняет урон герою)
8. Платформы, двигающиеся платформы
9. Кнопка (что-то открывают)

Монстры:
1. Монстр, который бьёт вблизи. Урон высокий.
2. Монстр, который бьёт издалека. Урон небольшой.
3. Мностр, который бьёт издалека и телепортируется. Урон небольшой.
Монстры передвигаются по платформе пока герой не попал в радиус атаки.

Герой:
1. 
2. Идти (влево, вправо)
3. Прыжок
4. Толкать
5. Лазать (по лестнице)
6. Атака монстров (ближний, дальний бой)
7. Шкала жизни и маны

Очки:
Очки будут начисляться за собранные в уровне монеты, уничтоженных монстров.

Интерфейс меню:
1. Начать игру
(открывается последний уровень, который Вы проходили)
2. Выбрать уровень
(Можно выбирать только те уровни, что игрок уже прошёл или проходит на данный момент)
Откроется карта уровней.
4. Настройки
(Редактировать звук, музыка)
5. Таблица лидеров (В БД имя, очки, уровень)

Интерфейс финального окна (когда кончились жизни):
1. Вернуться в меню
2. Начать уровень заново
3. В этом окне сообщают очки собраные в этом уровне.
Интерфейс финального окна (когда прошёл уровень):
4. Добавляется только кнопка (перейти на след. уровень)

Регистрация:
При нажатии на кнопку начать игру или выбора уровня будет открываться окно с регистрацией.
Нужно ввести имя. Если в БД есть ведённое имя, Вы вошли. Иначе создаётся новый аккаунт.

Технологии:
1. В БД хранятся логин, очки и уровень игрока.
2. Подсчёт результатов во время прохождения уровня.
3. Спрайты: герой, другие предметы для взаимодействия.
4. Анимация: герой ходит.
5. Стартовое оконо: меню.
6. Финальное окно: окно после уровня.
7. Несколько уровней.
8. Collide: взаимодействие с предметами героем, нарпример толкание ящика.
