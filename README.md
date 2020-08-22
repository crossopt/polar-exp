# polar-exp

Исследования декодирования полярных кодов с помощью belief propagation на примере binary erasure channel.

### Модель данных для кодирования:

#### Изначальные данные
Имеется n = 2^k переменных с индексами от 0 до 2^(k - 1). Значение каждой переменной равно либо 0, либо 1.

#### Полярное кодирование
Всего в кодировании k = log n шагов. На шаге i для всех индексов переменных a, b, различающихся только в i-ом бите, выполняются вычислительные элементы (a, b) -> (a xor b, b).

При этом с вероятностью p закодированные данные теряются при передаче через канал, и в таком случае вместо значения переменной передается '?'.

#### Frozen bits
np переменным с наименьшей вероятностью успешного декодирования из частично потерянных данных после приема изначально присваивается фиксированное значение. Такие переменные называются замороженными, или frozen.

#### Итоговые данные
На выходе имеются n = 2^k переменных, каждой из которых присвоено либо переданное значение, либо '?'. Матожидание количества потерянных значений равно np.

### Модель данных для декодирования:

#### Граф кодирования
Удобно рассматривать посчитанные при кодировании значения как вершины графа. Граф разделен на слои, соответствующие шагам кодирования, где в каждом слое ровно n вершин.

В таком графе будут ребра двух видов: горизонтальные и вертикальные.

- Вертикальные рёбра соединяют вершины, находящиеся в одном слое. Они соответствуют передаче переменной вычислительному элементу кодирования.

- Горизонтальные ребра соединяют вершины, находящиеся в соседних слоях. Они соответствуют передаче значения переменной на следующий шаг кодирования.

В таком графе у вершин, соответствующих изначальным переменным и итоговым переменным степень 1, а у всех остальных вершин степень 3. Из вершин степени 3 выходят два горизонтальных ребра и одно вертикальное.

#### Состояния '\*' и '?' 
Поскольку для анализа сходимости декодирования реальные значения кодов не важны, мы будем только различать состояния '\*' (значение известно) и '?' (значение неизвестно). До начала декодирования для изначальных данных известны np frozen bits, а для итоговых известны переменные с корректно переданными значениями. В нашей модели мы допускаем, что их n(1 - p).

Состояния соответствуют ребрам графа кодирования. На внешних ребрах, соединенных с изначальными и итоговыми переменными, состояния проставляются в соответствии с их значениями. На внутренних ребрах изначальное состояние равно '?'.

#### Типы внутренних вершин и правила декодирования
Внутренние вершины графа делятся на два типа: "верх" и "низ", в зависимости от того, как они были получены при кодировании.

- Узлы типа "верх" соответствуют значению, равному xor двух значений на предыдущем слое (вычислительный элемент передает в эту вершину значение для вычисления xor).

Из трех значений a, b, a xor b любые два определяют третье, поэтому при декодировании, если узлу типа "верх" инцидентны два ребра c меткой '\*', третьему можно тоже присвоить '\*'.

- Узлы типа "низ" соответствуют значению, равному значению на предыдущем слое (вычислительный элемент передает из этой вершины значение для вычисления xor).

Все значения в этой вершине одинаковы, значит одно любое определяет их все. Поэтому при декодировании, если узлу типа "низ" инцидентно ребро c меткой '\*', остальным можно тоже присвоить '\*'.

На основании этих двух правил можно декодировать код, то есть проставить всем ребрам графа значение метки '\*'. Мы стремимся исследовать сходимость этого процесса.

### Реализованные методы декодирования

#### Flooding

"Наивный" метод декодирования. Декодирование состоит из некоторого числа итераций. На каждой итерации параллельно применяются правила во всех внутренних вершинах.

#### Conventional scheduling

Декодирование состоит из некоторого числа итераций, а каждая итерация состоит из k шагов. На i-том шаге итерации параллельно применяются правила во всех вершинах i-того внутреннего слоя.

Этот метод работает лучше, чем flooding, но всё равно местами неэффективен и выполняет лишнюю работу. Например, неоптимально на первом шаге пытаться обновить значение внешнего ребра до обновления внутренних ребер на втором шаге.

#### Round-trip scheduling

Декодирование состоит из некоторого числа итераций, а каждая итерация состоит из 2k шагов. Сначала на каждом из i слоёв во всех вершинах слоя применяются правила для пропагации ребра из текущей вершины в вершину предыдущего слоя, а затем на каждом из i слоёв во всех вершинах слоя применяются правила для пропагации ребра из текущей вершины в вершину следующего слоя.

### Сравнение методов декодирования

#### Критерий завершения декодирования

Изначально предподсчитывается корректно декодированный граф и при декодировании в начале каждой итерации проверяется, что граф ещё не был корректно декодирован. Конечно, при реальном декодировании так сделать нельзя, но для исследования скорости и работы различных методов декодирования такой способ самый простой и удобный. 
