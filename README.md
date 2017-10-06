Engines:
Работоспособность протестирована на интерпритаторе - python3

Требования:
Компонентная система - esper
Графика - pyglet
Физика - pymunk

Рабочие элементы управления:
Перемещение по сцене - ПКМ
Зум - колесо мыши
Вращение сцены - СКМ
Вертикальная ориентация сцены - HOME
Перемещение перемещаемой сущности/создание цепи - ЛКМ

Запуск пиложения `python3 run.py` или `./run.py`

Компонентная система предполагает что каждая сущность (entity) системы составляется из компонентов.
За методы отвечают процессоры.

Все возможные компненты описаны в файлах `cmp_<componentName>.py`
Все процессоры описаны в файлах `prc_<pocessorName>.py`

Особенный процессор - фабрика файл `factory.py`. Как токовым процессором не является.
Имеет набор методов для потокового создания сущностей

Начало работы программы описана в файле `main.py`. Тестово можно вызывать суности отсюда, но в конечном
результате сущности должны создавать только на фабрике

Минимально необходимые компоненты для создания графических сущностей:
`Transform` - содержит данные для управлени характеристиками сущности (положение, размер, поворот и пр)
`Renderable` - содержит данные для отрисовки графического объекта

так же могут понадобиться `Joint` и `Segment`

Наиболее важный процессор - `EditorProcessor`
Этот процессор подписан на такие эффекты окна приложения как `on_mouse_press` и пр. где
происходит управление перемещением различных сущностей.

Фильтр сущностей:
Для того чтобы процессор мог управлять сущностью, необходимо запрасить из системы те компонеты из которых
эта сущность состоит:

Например:
Сущность узла состоит из компонент: Renderable, Transform и Joint
Другие сущности могут не содержать компоненты Joint
Поэтому, чтобы выбрать все компоненты-узлы необходимо в итераторе указать следующее:
```python
for ent, (tr, jnt, rend) in self.world.get_components(Transform, Joint, Renderable):
    code there
```
система цилически возвращает все сущености `ent` у которые присутствуюте ВСЕ три компоненты.
Сущности могут содержать и бОльшее число компонент, поэтому выбирать можно только необходимые
и достаточные для того чтобы корректно обрабатываеть данные.
В некоторых случаях необходимо создавать пустую компоненту, которая бы отличала один тип сущностей
от других

Все координаты объектов системы представлены объектом вектора `Vec2d`,
за исключением системных вызовов типа on_mouse_press. Которые так же упаковываются в вектор

Пример готового объекта:
Прототип сущности интегральной схемы представлен в классе фабрики - метод `create_instance`
с укзанием позиции нижней левой точки схемы.
Создание любого элемента необходимо начинать с получения новой сущности в системе `create_entity`
Класс Transform создает объект с якорной точкой (`anchor`) в центре объекта
Для наиболее удобного применения в прямоугольных формах точку следует смещать в координату (0, 0) -
нижний левый угол
сущность не будет воспроизводиться в системе пока ее компоненты не будут зарегистрированы методом
`add_component`





